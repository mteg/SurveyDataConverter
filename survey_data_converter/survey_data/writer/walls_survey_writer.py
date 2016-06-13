#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from survey_writer import *
import StringIO


class WallsSurveyWriter(SurveyWriter):
    def __init__(self, survey, file_path, source_file_name):
        super(WallsSurveyWriter, self).__init__(survey, file_path, source_file_name)

    @classmethod
    def file_type(cls):
        return "Walls Survey"

    @classmethod
    def file_extension(cls):
        return "srv"

    def _write_data(self, file_path):
        f = open(file_path, 'w')
        if self.survey.name:
            f.write(";%s\n" % self.survey.name)
        f.write(";%s\n\n" % self._source_file_name)

        if self.survey.name:
            f.write(";#PREFIX %s\n" % self.survey.name)
        f.write("#UNITS D=M A=G V=G Order=DAV\n\n")
        for trip in self.survey.trips:
            if trip.shots_count == 0:
                continue

            if trip.date:
                date_string = trip.date.strftime("%Y-%m-%d")
                f.write("#DATE %s\n\n" % date_string)
            else:
                f.write(";#DATE MISSING!!!\\n\n")

            if trip.comment:
                f.write(";Comment from file:\n")
                comment = StringIO.StringIO(trip.comment)
                for comment_line in comment:
                    f.write(";%s\n" % comment_line)
                f.write("\n")

            for data in trip.data:
                toSt  = data.toSt
                if not toSt:
                    toSt = "-"
                f.write("%s\t%s\t%0.3f\t%0.2f\t%0.2f" % (data.fromSt, toSt, data.tape, data.compass, data.clino))
                if data.comment:
                    f.write("\t;%s\n" % data.comment)
                else:
                    f.write("\n")
        f.close()
