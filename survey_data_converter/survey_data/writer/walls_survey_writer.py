#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from survey_writer import *


class WallsSurveyWriter(SurveyWriter):
    def __init__(self, survey, file_path):
        super(WallsSurveyWriter, self).__init__(survey, file_path)

    @classmethod
    def file_type(cls):
        return "Walls Survey"

    @classmethod
    def file_extension(cls):
        return "srv"

    def _write_data(self, file_path):
        f = open(file_path, 'w')

        f.close()
