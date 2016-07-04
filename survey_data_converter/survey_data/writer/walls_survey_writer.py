#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Arkadiusz Młynarczyk
#
# This file is part of SurveyDataConverter
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from survey_writer import *
import StringIO
import math
import os


class WallsSurveyWriter(SurveyWriter):
    def __init__(self, survey_reader, file_path, header, footer = ""):
        super(WallsSurveyWriter, self).__init__(survey_reader, file_path,
                                                header, footer)

    @classmethod
    def file_type(cls):
        return "Walls"

    @classmethod
    def file_extension(cls):
        return "srv"

    def _write_data(self, file_path):
        f = open(file_path, 'w')
        first_line = os.path.splitext(os.path.basename(self._survey_reader.file_path))[0]
        if self._survey_reader.survey.name:
            first_line = self._survey_reader.survey.name
        f.write(";%s\n" % first_line)

        if self._header:
            f.write("\n")
            header_lines = self._header.splitlines()
            for header_line in header_lines:
                f.write(";%s\n" % header_line.strip())
            f.write("\n")

        f.write(";Data imported from: %s (%s)\n\n" % (os.path.basename(self._survey_reader.file_path), self._survey_reader.file_type()))


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
                f.write(";#DATE <YYYY-MM-DD>\n\n")

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

        if self._footer:
            f.write("\n;%s\n" % self._footer)

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
