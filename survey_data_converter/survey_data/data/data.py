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


class Trip(object):
    def __init__(self):
        super(Trip, self).__init__()
        self.data = []
        self.comment = ""
        self.date = None
        self.name = ""
        self.declination = 0


class Survey(object):
    def __init__(self):
        # type: () -> object
        super(Survey, self).__init__()
        self.name = ""
        self.trips = []
