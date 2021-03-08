#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The SplitterWindow containing the AudioBookMetadata and the MP3FilePanel panels.
aka the main part if the screen.
"""

import wx

from ivonet.gui.AudiobookMetaDataPanel import AudiobookMetaDataPanel
from ivonet.gui.MP3FilePanel import MP3FilePanel


class MetadataPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        vs_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        hs_m4bpage = wx.BoxSizer(wx.VERTICAL)
        vs_m4b_page.Add(hs_m4bpage, 1, wx.EXPAND, 0)

        self.sw_m4b_page = wx.SplitterWindow(self, wx.ID_ANY)
        self.sw_m4b_page.SetMinimumPaneSize(350)
        hs_m4bpage.Add(self.sw_m4b_page, 1, wx.EXPAND, 0)

        self.pnl_left_m4b_page = AudiobookMetaDataPanel(self.sw_m4b_page, -1)

        self.pnl_right_m4b_page = MP3FilePanel(self.sw_m4b_page, wx.ID_ANY)

        self.sw_m4b_page.SplitVertically(self.pnl_left_m4b_page, self.pnl_right_m4b_page, 352)

        self.SetSizer(vs_m4b_page)

        self.Layout()
