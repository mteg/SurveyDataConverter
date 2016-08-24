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

from abc import ABCMeta

from ..data import *
import math


class SurveyWriter(object):
    __metaclass__ = ABCMeta

    def __init__(self, survey_reader, file_path, header, footer = ""):
        super(SurveyWriter, self).__init__()
        self._header = header.strip()
        self._footer = footer.strip()
        self._survey_reader = survey_reader
        self._write_data(file_path)

    
    def deduplicate(self, trip_data):
	p = DataLine()
        for data in trip_data:
            if p.toSt and data.toSt and p.toSt == data.toSt:
                have_duplicates = True
                break
            p = data


        if not have_duplicates:
            return trip_data

        self.__previous_data = DataLine()
        self.__tape = []
        self.__compass = []
        self.__clino = []
        self.__comments = []
        
        new_data = []

        for data in trip_data:
            if not data.toSt or (
                            data.fromSt !=
                            self.__previous_data.fromSt or data.toSt != self.__previous_data.toSt):
		if len(self.__tape):
	                new_data.append(self.average_shot())
            
            self.__previous_data = data

            if data.toSt:
                self.__tape.append(data.tape)
                self.__compass.append(data.compass)
                self.__clino.append(data.clino)
                self.__comments.append(data.comment)
            else:
                new_data.append(data)
            
        if len(self.__tape):
            new_data.append(self.average_shot())
        
        return new_data
        
    def average_shot(self):
        calculated_tape = sum(self.__tape) / len(self.__tape)
        if calculated_tape == 0:
	    calculated_clino = 0
            calculated_compass = 0
	else:
            calculated_clino = sum(self.__clino) / len(self.__clino)
            x = 0
            y = 0
            for angle in self.__compass:
                x += math.cos(math.radians(angle))
                y += math.sin(math.radians(angle))
            calculated_compass = math.degrees(math.atan2(y, x)) % 360
            if calculated_compass == 360: calculated_compass = 0

	data_line = DataLine()
	data_line.fromSt = self.__previous_data.fromSt
	data_line.toSt = self.__previous_data.toSt
	data_line.tape = calculated_tape
	data_line.compass = calculated_compass
	data_line.clino = calculated_clino
	data_line.comment = ' | '.join(self.__comments)

        self.__tape = []
        self.__compass = []
        self.__clino = []
	self.__comments = []
	
	return data_line
        
        


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
