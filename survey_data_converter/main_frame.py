#!/usr/bin/env python2 -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import wx
import wx.lib.agw.persist as PERSIST

from .info import (
    __appname__
)

from survey_data import SurveyReader

class MainFrame(wx.Frame):
    FRAME_STYLE = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    SURVEY_LABEL_TEXT = "Survey File:"
    SURVEY_FILE_CTRL_MESSAGE = "Select Survey Data File"
    SOURCE_FILE_CTRL_WILDCARD = "Supported files (" \
                                "*.the;*.txt)|*.the;*.txt|Therion file (" \
                                "*.the)|*.the|Text file (*.txt)|*.txt|All " \
                                "files (*.*)|*.*"

    ALERT_UNSUPPORTED_FILE_TYPE_CAPTION = "Unsupported file"
    ALERT_UNSUPPORTED_FILE_TYPE_MESSAGE = "Can't recognize this file as a " \
                                          "survey data, probably it isn't " \
                                          "supported yet."

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, wx.ID_ANY, __appname__,
                          style=self.FRAME_STYLE, name="MainFrame")
        self.__active = False
        self.SetMinClientSize(wx.Size(400, 0))

        self._panel = wx.Panel(self)

        self._source_file_label = wx.StaticText(self._panel,
                                                label=self.SURVEY_LABEL_TEXT)
        self._source_file_ctrl = wx.FilePickerCtrl(self._panel,
                                                   message=self.SURVEY_FILE_CTRL_MESSAGE,
                                                   wildcard=self.SOURCE_FILE_CTRL_WILDCARD)

        if sys.platform == "win32":
            self._source_file_ctrl.GetPickerCtrl().SetLabel("Browse...")

        self._add_sizers()

        self.Fit()
        self.Center()

        self._register_and_restore()

        self.Bind(wx.EVT_CLOSE, self._on_exit)
        self._source_file_ctrl.Bind(wx.EVT_FILEPICKER_CHANGED,
                                    self._on_file_selected)

    def _register_and_restore(self):
        mgr = PERSIST.PersistenceManager.Get()
        mgr.RegisterAndRestore(self)

    def _on_exit(self, event):
        mgr = PERSIST.PersistenceManager.Get()
        mgr.SaveAndUnregister()
        event.Skip()

    def _on_file_selected(self, event):
        survey_file_path = self._source_file_ctrl.GetPath()
        self._file_reader = SurveyReader(survey_file_path)
        export_possible = self._file_reader is not None
        self._toggle_export_interface(export_possible)
        if not export_possible:
            self._alert_unsupported_survey_file()
        event.Skip()

    def _add_sizers(self):
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        source_file_sizer = wx.BoxSizer(wx.HORIZONTAL)

        source_file_sizer.Add(self._source_file_label, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        source_file_sizer.AddSpacer(5)
        source_file_sizer.Add(self._source_file_ctrl, 1)

        vertical_sizer.Add(source_file_sizer, 0, wx.TOP | wx.BOTTOM | wx.EXPAND,
                           0)
        vertical_sizer.Add(wx.StaticLine(self._panel), 0,
                           wx.TOP | wx.BOTTOM | wx.EXPAND, 5)

        horizontal_sizer.Add(vertical_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self._panel.SetSizer(horizontal_sizer)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self._panel, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

    def _alert_unsupported_survey_file(self):
        alert = wx.MessageDialog(self, self.ALERT_UNSUPPORTED_FILE_TYPE_MESSAGE,
                                 self.ALERT_UNSUPPORTED_FILE_TYPE_CAPTION,
                                 wx.OK | wx.ICON_ERROR)
        alert.Center()
        alert.ShowModal()
        alert.Destroy()

    def _toggle_export_interface(self, active):
        if self.__active == active:
            return
        pass
