#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from survey_writer import *
import StringIO
import math
import os


class WallsSurveyWriter(SurveyWriter):
    def __init__(self, survey_reader, file_path):
        super(WallsSurveyWriter, self).__init__(survey_reader, file_path)

    @classmethod
    def file_type(cls):
        return "Walls Survey"

    @classmethod
    def file_extension(cls):
        return "srv"

    def _write_data(self, file_path):
        f = open(file_path, 'w')
        first_line = os.path.splitext(os.path.basename(self._survey_reader.file_path))[0]
        if self._survey_reader.survey.name:
            first_line = self._survey_reader.survey.name
        f.write(";%s\n" % first_line)
        f.write(";%s (%s)\n\n" % (os.path.basename(self._survey_reader.file_path), self._survey_reader.file_type()))

        f.write(";#PREFIX %s\n" % first_line)
        f.write("#UNITS D=M A=G V=G Order=DAV\n\n")
        for trip in self._survey_reader.survey.trips:

            if trip.shots_count == 0:
                continue

            have_duplicates = False
            p = DataLine()
            for data in trip.data:
                if p.toSt and data.toSt and p.toSt == data.toSt:
                    have_duplicates = True
                    break
                p = data

            if trip.date:
                date_string = trip.date.strftime("%Y-%m-%d")
                f.write("#DATE %s\n\n" % date_string)
            else:
                f.write(";#DATE MISSING!!!\n\n")

            if trip.comment:
                f.write(";Comment from file:\n")
                comment = StringIO.StringIO(trip.comment)
                for comment_line in comment:
                    f.write(";%s\n" % comment_line.strip())
                f.write("\n")

            if have_duplicates:
                self.__previous_data = DataLine()
                self.__tape = []
                self.__compass = []
                self.__clino = []

            for data in trip.data:
                prefix = ""
                if have_duplicates:
                    if not data.toSt or (
                                    data.fromSt !=
                                    self.__previous_data.fromSt or data.toSt
                                != self.__previous_data.toSt):
                        self.__write_calculated_shot(f)
                    self.__previous_data = data

                    if data.toSt and data.tape != 0:
                        self.__tape.append(data.tape)
                        self.__compass.append(data.compass)
                        self.__clino.append(data.clino)
                        prefix = ";"

                toSt = data.toSt
                if not toSt: toSt = "-"

                f.write(
                        "%s%s\t%s\t%0.3f\t%0.2f\t%0.2f" % (
                            prefix, data.fromSt, toSt, data.tape, data.compass,
                            data.clino))

                comment = data.comment
                comment = (" ".join(comment.splitlines())).strip()
                if data.tape == 0: comment = "Connecting shot; " + comment
                comment = comment.strip(' ;').strip()
                if comment:
                    f.write("\t;%s" % comment)
                f.write("\n")
            if have_duplicates: self.__write_calculated_shot(f)

        f.close()

    def __write_calculated_shot(self, f):
        if len(self.__tape) == 0:
            return
        calculated_tape = sum(self.__tape) / len(self.__tape)
        if calculated_tape == 0: return
        calculated_clino = sum(self.__clino) / len(self.__clino)
        x = 0
        y = 0
        for angle in self.__compass:
            x += math.cos(math.radians(angle))
            y += math.sin(math.radians(angle))
        calculated_compass = math.degrees(math.atan2(y, x)) % 360
        if calculated_compass == 360: calculated_compass = 0
        f.write(
            "%s\t%s\t%0.3f\t%0.2f\t%0.2f\t;Calculated from shots above\n" % (
                self.__previous_data.fromSt, self.__previous_data.toSt,
                calculated_tape, calculated_compass,
                calculated_clino))
        self.__tape = []
        self.__compass = []
        self.__clino = []
