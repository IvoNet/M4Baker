#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import wx


class QueuePanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        hs_queue = wx.BoxSizer(wx.HORIZONTAL)

        vs_queue = wx.BoxSizer(wx.VERTICAL)
        hs_queue.Add(vs_queue, 1, wx.EXPAND, 0)

        self.lc_queue = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.lc_queue.AppendColumn("Audiobook", format=wx.LIST_FORMAT_LEFT, width=200)
        self.lc_queue.AppendColumn("Progress", format=wx.LIST_FORMAT_LEFT, width=650)
        self.lc_queue.AppendColumn("Status", format=wx.LIST_FORMAT_LEFT, width=100)
        vs_queue.Add(self.lc_queue, 1, wx.EXPAND, 0)

        self.SetSizer(hs_queue)

        self.Layout()
