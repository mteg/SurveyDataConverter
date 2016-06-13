#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Unit=Meter
# From	 To	 Length	 Bearing	 Inc	 Comments
# 0	 1	 2.366	 1.4	 -15.5
# 1	 2	 5.254	 91.6	 16.6
# 2	 3	 2.187	 122.4	 -1.3
# 2	 2:A	 16.787	 57.2	 3.8
# 3	 4	 7.745	 351.0	 -74.3

import shlex
import datetime

from survey_reader import *


class CaveExplorerSurveyReader(SurveyReader):
    TYPICAL_STRING_1 = "Unit=Meter"
    TYPICAL_STRING_2 = "From	 To	 Length	 Bearing	 Inc	 Comments"

    def __init__(self, file_path):
        super(CaveExplorerSurveyReader, self).__init__(file_path)

    @classmethod
    def can_read_file(cls, file_path):
        f = open(file_path, 'rb')
        first_line = f.readline().strip()
        second_line = f.readline().strip()
        f.close()
        if first_line == cls.TYPICAL_STRING_1 and second_line == cls.TYPICAL_STRING_2:
            return True
        else:
            return False

    @classmethod
    def file_type(cls):
        return "CaveExplorer txt"

    @classmethod
    def file_extension(cls):
        return "txt"

    def _read_data(self, file_path):
        pass

