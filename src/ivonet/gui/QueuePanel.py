#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Yup the Queue Panel. 
"""

import wx

from ivonet.events import ee


class QueuePanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.count = 0

        hs_queue = wx.BoxSizer(wx.HORIZONTAL)

        vs_queue = wx.BoxSizer(wx.VERTICAL)
        hs_queue.Add(vs_queue, 1, wx.EXPAND, 0)

        self.lc_queue = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.lc_queue.AppendColumn("Audiobook", format=wx.LIST_FORMAT_LEFT, width=200)
        self.lc_queue.AppendColumn("Progress", format=wx.LIST_FORMAT_LEFT, width=650)
        self.lc_queue.AppendColumn("Status", format=wx.LIST_FORMAT_LEFT, width=100)
        vs_queue.Add(self.lc_queue, 1, wx.EXPAND, 0)

        self.progress = wx.Gauge(self, -1, 100, (110, 50), (250, -1))
        vs_queue.Add(self.progress, 0, wx.EXPAND, 0)

        # TODO TEMP Code while progressbar not yet implemented
        self.Bind(wx.EVT_TIMER, self.timer_handler)
        self.timer = wx.Timer(self)
        ee.on("processing.start", self.on_start)
        ee.on("processing.stop", self.on_stop)
        # /TEMP Code while progressbar not yet implemented

        self.SetSizer(hs_queue)
        self.Layout()

    # noinspection PyUnusedLocal
    def on_start(self, event):
        self.timer.Start(100)

    # noinspection PyUnusedLocal
    def on_stop(self, event):
        self.timer.Stop()
        self.count = 0
        self.progress.SetValue(self.count)

    # noinspection PyUnusedLocal
    def timer_handler(self, event):
        self.count = self.count + 1

        if self.count >= 100:
            self.count = 0

        self.progress.SetValue(self.count)
