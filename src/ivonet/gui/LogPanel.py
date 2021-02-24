#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import wx

from ivonet.events import ee


class LogPanel(wx.Panel):
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
        ee.emit("log", "Event handler 'on_log_max_len' not implemented!")
        event.Skip()

    def on_log(self, *args):
        msg = "{timestamp} - {message}\n".format(timestamp=time.strftime('%X'),
                                                 message=" ".join([str(x) for x in args]))
        self.tc_log.AppendText(msg)
