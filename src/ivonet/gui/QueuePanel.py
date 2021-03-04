#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-04 22:53:09$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Yup the Queue Panel. 
"""

import wx

from ivonet.events import ee
from ivonet.model.Project import Project


class AudiobookEntry(wx.Panel):
    def __init__(self, parent, project: Project, panel_id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, panel_id, style=wx.BORDER_SIMPLE)
        self.parent = parent

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((10, 10), 0, 0, 0)

        self.filename = wx.StaticText(self, wx.ID_ANY,
                                      project.title)  # TODO Final m4b name here based on convention I use in cli
        # TODO Tooltip with with complete representation of the book?
        sizer.Add(self.filename, 5, wx.ALIGN_CENTER_VERTICAL, 0)

        self.elapsed = wx.StaticText(self, wx.ID_ANY,
                                     project.artist)  # TODO Timer functionality here iso artist (just placeholder)
        sizer.Add(self.elapsed, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.progress = wx.Gauge(self, wx.ID_ANY, 100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer.Add(self.progress, 3, wx.ALIGN_CENTER_VERTICAL, 0)

        self.stop_button = wx.Button(self, wx.ID_ANY, "x")
        self.stop_button.SetMinSize((24, 34))
        sizer.Add(self.stop_button, 0, wx.EXPAND, 0)
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.stop_button)

        sizer.Add((10, 10), 0, 0, 0)
        self.SetSizer(sizer)

        self.Layout()

    def update(self, percent):
        self.progress.SetValue(percent)

    def on_stop(self, event):
        # TODO Add functionality to this kill button
        #  - Stop the processing of the worker thread
        #  - Kill this panel
        self.Destroy()


class QueuePanel(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.SetScrollRate(10, 10)
        self.queue = []
        # TODO Add Queue functionality
        #  - Add to Queue
        #  - Save the queue on application quit?
        #  - Stop processing
        #  - Restart processing?
        #  etc

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh, self.refresh_timer)
        self.refresh_timer.Start(1000)

        self.Layout()
        ee.on("queue.project", self.ee_add_project)

    def ee_add_project(self, project: Project):
        book = AudiobookEntry(self, project)
        self.sizer.Add(book, 0, wx.ALL | wx.EXPAND, 0)
        self.Layout()
        self.queue.append(project)
        # ee.emit("queue.add", project)  # TODO Add functionality to this event

    # noinspection PyUnusedLocal
    def on_refresh(self, event):
        self.Refresh()
        self.Layout()
