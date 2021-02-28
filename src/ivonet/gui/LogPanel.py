#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The Log Screen
"""

import time
import wx

from ivonet.events import ee, log


class LogPanel(wx.Panel):
    """All logging events will land here."""

    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        ee.on("log", self.on_log)

        vs_log = wx.BoxSizer(wx.VERTICAL)

        hs_log = wx.BoxSizer(wx.HORIZONTAL)
        vs_log.Add(hs_log, 1, wx.EXPAND, 0)

        self.tc_log = wx.TextCtrl(self, wx.ID_ANY, "",
                                  style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_WORDWRAP)
        self.tc_log.SetFont(
            wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Courier New"))
        hs_log.Add(self.tc_log, 1, wx.EXPAND, 0)

        self.SetSizer(vs_log)

        self.Layout()

        self.Bind(wx.EVT_TEXT_MAXLEN, self.on_log_max_len, self.tc_log)

    def on_log_max_len(self, event):
        log("Event handler 'on_log_max_len' not implemented!")
        event.Skip()

    def on_log(self, *args):
        message = " ".join([str(x) for x in args])
        self.tc_log.AppendText("{timestamp} - {message}\n".format(timestamp=time.strftime('%X'),
                                                                  message=message))
