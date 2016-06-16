#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import shlex
import datetime
import struct
import time

from survey_reader import *


import ReadTop as rt


class PocketTopoTopReader(SurveyReader):
    def __init__(self, file_path):
        super(PocketTopoTopReader, self).__init__(file_path)

    @classmethod
    def can_read_file(cls, file_path):
        with open(file_path, "rb") as tfile:
            if tfile.read(3) == b'Top':
                return True
            return False

    @classmethod
    def file_type(cls):
        return "PocketTopo top"

    @classmethod
    def file_extension(cls):
        return "top"

    def _read_data(self, file_path):
        data = rt.readfile(file_path, False, False)
        # {'trips': trips, 'shots': shots, 'ref': references}
        trip_idx = 0
        for rtrip in data['trips']:
            #{'date': tdate, 'comment': comment, 'dec': dec}
            trip = Trip()
            if 'comment' in rtrip and rtrip['comment']:
                trip.comment = rtrip['comment'].strip()
            if 'date' in rtrip and rtrip['date']:
                trip.date = datetime.datetime.fromtimestamp(time.mktime(rtrip['date']))
            if 'dec' in rtrip and rtrip['dec']:
                trip.declination = rtrip['dec']
            self.survey.trips[trip_idx] = trip
            trip_idx += 1
        for rshoot in data['shots']:
            # {'from', 'to', 'tape', 'compass', 'clino', 'trip', 'direction', 'comment'}
            if not 'trip' in rshoot or rshoot['trip'] < 0: continue
            trip = self.survey.trips[rshoot['trip']]
            data_line = DataLine()
            if 'from' in rshoot:
                data_line.fromSt = rshoot['from']
            if 'to' in rshoot and rshoot['to'] != "-":
                data_line.toSt = rshoot['to']
            if 'compass' in rshoot:
                data_line.compass = round(rshoot['compass'], 2)
            if 'clino' in rshoot:
                data_line.clino = round(rshoot['clino'], 2)
            if 'tape' in rshoot:
                data_line.tape = round(rshoot['tape'], 3)
            if 'comment' in rshoot:
                data_line.comment = rshoot['comment']
            is_splay = not data_line.toSt
            if is_splay:
                trip.splays_count += 1
            elif data_line != trip.last_dataline:
                trip.shots_count += 1
            trip.data.append(data_line)
        return self.survey
