#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Survey Data Converter __main__ file.

__main__ file is a python 'executable' file which calls the
survey_data_converter main() function in order to start the app.
"""

from __future__ import unicode_literals

import sys

if not __package__ and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    import os.path

    PATH = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(PATH)))

import survey_data_converter

if __name__ == '__main__':
    survey_data_converter.main()
