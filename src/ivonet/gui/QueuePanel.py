#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-04 22:53:09$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Yup the Queue Panel Scrollable window. 
"""

import wx
import wx.lib.newevent

from ivonet.events import ee
from ivonet.gui.AudiobookEntryPanel import AudiobookEntry
from ivonet.model.Project import Project


class QueuePanel(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.SetScrollRate(10, 10)
        self.queue = []
        # TODO Save Queue and state on exit if processing not yet done?

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh, self.refresh_timer)
        self.refresh_timer.Start(1000)

        self.Layout()
        ee.on("queue.project", self.ee_add_project)

    # noinspection PyUnusedLocal
    def on_refresh(self, event):
        self.Refresh()
        self.Layout()

    def ee_add_project(self, project: Project):
        book = AudiobookEntry(self, project)
        self.sizer.Prepend(book, 0, wx.ALL | wx.EXPAND, 0)
        self.Layout()
        self.queue.append(book)
        book.start()

    def remove(self, entry: AudiobookEntry):
        self.queue.remove(entry)
        entry.Destroy()
