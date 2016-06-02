#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#czaf   (m, 360)
#
#[1]: 2015/01/04     0.00  "Arek distox\rMarta dog\rIda plan"
#
#
#     1.0                   0.000    0.00    0.00
#     1.0        1.2        2.193  181.76    1.93  [1]  ; comment
#     1.0                   2.183  177.04   32.84  ; comment
#     1.0                   2.022  179.02   57.35  
#     1.0                   2.154  160.44  -17.33  [1]

import string
import sys
import re
from survey_reader import *

class PocketTopoSurveyReader(SurveyReader):
  TYPICAL_STRING="(m, 360)"

  def __init__(self, file_path):
    SurveyReader.__init__(self, file_path)

  @classmethod
  def can_read_file(cls, file_path):
    f = open(file_path, 'rb')
    first_line = f.readline()
    f.close()
    first_line = first_line.strip()
    index = first_line.rfind(cls.TYPICAL_STRING)
    if index == -1:
      return False
    if index + len(cls.TYPICAL_STRING) == len(first_line):
      return True
    return False

def _read_data(self, file_path):
  print "arek"
  with open(file_path, 'rb') as f:
    for i, line in enumerate(f):
      if i == 0 or len(line) == 0:
        continue
      data = self._read_data_line(line)
      if data is None:
        self._survey_comment += line + "\n"
      pass

def _read_data_line(self, line):
  return None