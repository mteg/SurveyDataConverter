#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""SurveyDataConverted __init__ file.

Responsible on how the package looks from the outside.

Example:
    In order to load the GUI from a python script.

        import survey_data_converter

        survey_data_converter.main()

"""

from __future__ import unicode_literals

import sys

import gettext

try:
    import wx
except ImportError as error:
    print error
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
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = MainFrame() # A Frame is a top-level window.
    frame.Show(True)     # Show the frame.
    app.MainLoop()
