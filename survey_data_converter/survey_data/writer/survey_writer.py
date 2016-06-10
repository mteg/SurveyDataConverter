#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from abc import ABCMeta

from ..data import *


class SurveyWriter(object):
    __metaclass__ = ABCMeta

    def __init__(self, survey, file_path):
        super(SurveyWriter, self).__init__()
        self.survey = survey
        self._write_data(file_path)

        raise NotImplementedError

    @classmethod
    def supported_files(cls):
        writer_classes = cls.__subclasses__()
        supported_files = []
        for writer_class in writer_classes:
            supported_files.append(
                    [writer_class.file_type(), writer_class.file_extension()])
        return supported_files

    @classmethod
    def file_type(cls):
        raise NotImplementedError

    @classmethod
    def file_extension(cls):
        raise NotImplementedError

    def _write_data(self, file_path):
        raise NotImplementedError
