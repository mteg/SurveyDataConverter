#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# czaf   (m, 360)
# or (still first line)
# (m, 360)
#
# [1]: 2015/01/04     0.00  "Arek distox\rMarta dog\rIda plan"
# [2]: 2015/01/04     5.00
#
#
#     1.0                   0.000    0.00    0.00 "comment"
#     1.0        1.2        2.193  181.76    1.93  [1] "comment"
#     1.0                   2.022  179.02   57.35  
#     1.0                   2.154  160.44  -17.33  [1]
#     1.0                   2.154  160.44  -17.33  [1] "comment"
#     1.0        1.2        2.154  160.44  -17.33  [1]

import datetime
import shlex

from survey_reader import *


class PocketTopoSurveyReader(SurveyReader):
    TYPICAL_STRING = "(m, 360)"

    def __init__(self, file_path):
        super(PocketTopoSurveyReader, self).__init__(file_path)

    @classmethod
    def can_read_file(cls, file_path):
        f = open(file_path, 'rb')
        first_line = f.readline()
        f.close()
        first_line = first_line.strip()
        if first_line.endswith(cls.TYPICAL_STRING):
            return True
        else:
            return False

    @classmethod
    def file_type(cls):
        return "txt"

    @classmethod
    def file_extension(cls):
        return "PocketTopo txt"

    def _read_data(self, file_path):
        state = 0
        with open(file_path, 'rb') as f:
            for line in f.readlines():
                line = line.strip()
                data = shlex.split(line)
                if len(data) == 0:
                    continue
                if state == 0:
                    if len(data) > 1:
                        self.survey.name = data[0]
                    state = 1
                    continue
                if state == 1:
                    # This is a data line, we will skip parsin
                    if not data[0].startswith("["):
                        state = 2
                    else:
                        trip = Trip()
                        trip.name = self.__trip_name_from_string(data[0])
                        trip.date = datetime.datetime.strptime(data[1],
                                                               "%Y/%m/%d")
                        trip.declination = float(data[2])
                        if len(data) > 3:
                            trip.comment = data[3]
                        self.survey.trips.append(trip)
                        continue
                if state == 2:
                    data_line = DataLine()
                    trip_name = ""
                    non_data_idx = 6
                    if data[-1].startswith("["):
                        trip_name = self.__trip_name_from_string(data[-1])
                        non_data_idx = min(non_data_idx, len(data) - 1)
                    elif data[-2].startswith("["):
                        trip_name = self.__trip_name_from_string(data[-2])
                        data_line.comment = data[-1]
                        non_data_idx = min(non_data_idx, len(data) - 2)
                    else:
                        if len(data) > 5:
                            data_line.comment = data[-1]
                            non_data_idx = min(non_data_idx, len(data) - 1)
                        elif len(data) == 5:
                            if not data[4].startswith("0.0") and data[
                                4].endswith(
                                    "0"):
                                data_line.comment = data[4]
                                non_data_idx = min(non_data_idx, 4)
                    non_data_idx = min(non_data_idx, len(data))
                    if (non_data_idx == 5):
                        data_line.toSt = data[1]
                    data_line.fromSt = data[0]
                    data_line.tape = float(data[non_data_idx - 3])
                    data_line.compass = float(data[non_data_idx - 2])
                    data_line.clino = float(data[non_data_idx - 1])

                    is_splay = not data_line.toSt;

                    if data_line.tape == 0 and is_splay:
                        continue

                    trip = self._trip_with_name(trip_name)
                    if trip is not None:
                        trip.data.append(data_line)
                        if is_splay:
                            trip.splays_count += 1
                        elif data_line != trip.last_dataline:
                            trip.shots_count += 1
                    continue
        return self.survey

    def __trip_name_from_string(self, trip_string):
        return trip_string.strip('[]')

    def _read_data_line(self, line):
        return None
