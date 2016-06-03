#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from abc import ABCMeta

from ..data import *

class SurveyReader(object):
    __metaclass__ = ABCMeta

    def __new__(cls, file_path):
        reader_classes = cls.__subclasses__()
        for reader_class in reader_classes:
            if reader_class.can_read_file(file_path):
                return object.__new__(reader_class, file_path)
        return None

    def __init__(self, file_path):
        super(SurveyReader, self).__init__()
        self.survey = Survey()
        self.survey.trips.append(Trip())
        self._read_data(file_path)

    @classmethod
    def can_read_file(cls, file_path):
        raise NotImplementedError

    def _read_data(self, file_path):
        raise NotImplementedError

    def _trip_with_name(self, trip_name):
        for trip in self.survey.trips:
            if trip.name == trip_name:
                return trip
        return None
