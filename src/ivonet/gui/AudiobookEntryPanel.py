#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-10 13:09:17$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import time

import wx
import wx.lib.newevent
from wx._core import CommandEvent

from ivonet.events import log, dbg
from ivonet.events.custom import EVT_PROCESS_DONE, EVT_PROCESS_ERROR, ProcessExceptionEvent, ProcessCleanEvent, \
    ProcessCancelledEvent
from ivonet.io.save import save_project
from ivonet.model.Project import Project
from ivonet.threading.ProjectConverterWorker import ProjectConverterWorker


class AudiobookEntry(wx.Panel):
    def __init__(self, parent, project: Project, panel_id=wx.ID_ANY):
        wx.Panel.__init__(self, parent.queue_window, panel_id, style=wx.BORDER_SIMPLE)
        self.parent = parent
        self.start_time = time.perf_counter()
        self.stage = 0  # used for the progressbar based on the different conversion stages
        self.project = project
        self.running = False

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((10, 10), 0, 0, 0)

        self.filename = wx.StaticText(self, wx.ID_ANY,
                                      project.title)  #
        self.filename.SetToolTip(str(project))
        sizer.Add(self.filename, 5, wx.ALIGN_CENTER_VERTICAL, 0)

        self.elapsed = wx.StaticText(self, wx.ID_ANY, "00:00:00")
        sizer.Add(self.elapsed, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_time_indicator, self.refresh_timer)

        self.progress = wx.Gauge(self, wx.ID_ANY, range=600, size=(300, 21), style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer.Add(self.progress, 3, wx.ALIGN_CENTER_VERTICAL, 0)

        self.stop_button = wx.Button(self, wx.ID_ANY, "x")
        self.stop_button.SetMinSize((24, 24))
        sizer.Add(self.stop_button, 0, wx.EXPAND, 0)
        self.Bind(wx.EVT_BUTTON, self.on_stopped, self.stop_button)
        self.Bind(EVT_PROCESS_DONE, self.on_done)
        self.Bind(EVT_PROCESS_ERROR, self.on_error)

        sizer.Add((10, 10), 0, 0, 0)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LEFT_DCLICK, self.on_save, self)
        self.Layout()
        self.process = ProjectConverterWorker(self, self.project)

    def start(self):
        self.refresh_timer.Start(1000)
        self.process.start()
        self.running = True

    def update(self, percent):
        self.progress.SetValue(int(self.stage * 100 + percent))

    def stop(self):
        self.process.stop()
        self.refresh_timer.Stop()
        self.running = False

    def on_stopped(self, event: CommandEvent):
        if self.running:
            self.stop()
            self.filename.SetForegroundColour(wx.RED)
            self.Refresh()
            wx.PostEvent(self.parent, ProcessCancelledEvent(obj=self))
        else:
            wx.PostEvent(self.parent, ProcessCleanEvent(obj=self))
        event.StopPropagation()

    def on_done(self, event):
        self.stop()
        self.filename.SetForegroundColour(wx.GREEN)
        event.Skip()

    def on_error(self, event: ProcessExceptionEvent):
        log("Processing stopped because an error occurred:", event.project.title)
        dbg("Processing error", str(event.cmd))
        self.filename.SetForegroundColour(wx.RED)
        self.Refresh()
        self.stop()

    def on_time_indicator(self, event):
        self.elapsed.SetLabel(time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - self.start_time)))
        event.Skip()

    def on_save(self, event):
        dbg("on_save event!")
        save_project(self.parent, self.project)
        event.Skip()
