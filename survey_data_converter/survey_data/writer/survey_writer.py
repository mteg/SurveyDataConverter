#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from abc import ABCMeta

from ..data import *


class SurveyWriter(object):
    __metaclass__ = ABCMeta

    def __init__(self, survey_reader, file_path, header, footer = ""):
        super(SurveyWriter, self).__init__()
        self._header = header.strip()
        self._footer = footer.strip()
        self._survey_reader = survey_reader
        self._write_data(file_path)

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
