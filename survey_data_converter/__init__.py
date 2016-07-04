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

"""SurveyDataConverted __init__ file.

Responsible on how the package looks from the outside.

Example:
    In order to load the GUI from a python script.

        import survey_data_converter

        survey_data_converter.main()

"""

from __future__ import unicode_literals

import sys

try:
    import wx
except ImportError as error:
    print(error)
    sys.exit(1)

# For package use
from .version import __version__
from .info import (
    __author__,
    __appname__,
    __contact__,
    __license__,
    __projecturl__,
    __licensefull__,
    __description__,
    __descriptionfull__,
)

from .main_frame import MainFrame


def main():
    """The real main. Creates and calls the main app windows. """
    app = wx.App(
        False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = MainFrame()  # A Frame is a top-level window.
    frame.Show(True)  # Show the frame.
    app.MainLoop()
