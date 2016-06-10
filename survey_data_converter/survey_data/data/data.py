#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class DataLine(object):
    def __init__(self):
        super(DataLine, self).__init__()
        self.fromSt = ""
        self.toSt = ""
        self.clino = 0
        self.compass = 0
        self.tape = 0
        self.comment = ""

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return  self.fromSt == other.fromSt && self.toSt == other.toSt

class Trip(object):
    def __init__(self):
        super(Trip, self).__init__()
        self.data = []
        self.comment = ""
        self.date = None
        self.name = ""
        self.declination = 0
        self.splays_count = 0
        self.shots_count = 0

    @property
    def last_dataline(self):
        if len(self.data):
            return self.data[-1]
        return Trip()


class Survey(object):
    def __init__(self):
        # type: () -> object
        super(Survey, self).__init__()
        self.name = ""
        self.trips = []
