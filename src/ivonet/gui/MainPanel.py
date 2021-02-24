#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import wx

from ivonet.gui.NoteBook import NoteBook


class MainPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)

        sizer_main_panel = wx.BoxSizer(wx.VERTICAL)

        self.main_notebook = NoteBook(self, wx.ID_ANY)
        sizer_main_panel.Add(self.main_notebook, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(sizer_main_panel)

        self.Layout()
