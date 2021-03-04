#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 04/03/2021 19:23$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx


class AudiobookEntry(wx.Panel):
    def __init__(self, parent, audiobook, panel_id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, panel_id, style=wx.BORDER_SIMPLE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((10, 10), 0, 0, 0)

        self.filename = wx.StaticText(self, wx.ID_ANY, audiobook)
        sizer.Add(self.filename, 5, wx.ALIGN_CENTER_VERTICAL, 0)

        self.timer = wx.StaticText(self, wx.ID_ANY, "Time")
        sizer.Add(self.timer, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.progress = wx.Gauge(self, wx.ID_ANY, 100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer.Add(self.progress, 3, wx.ALIGN_CENTER_VERTICAL, 0)

        self.stop_button = wx.Button(self, wx.ID_ANY, "x")
        self.stop_button.SetMinSize((24, 34))
        sizer.Add(self.stop_button, 0, wx.EXPAND, 0)

        sizer.Add((10, 10), 0, 0, 0)
        self.SetSizer(sizer)

        self.Layout()

    def update(self, percent):
        self.progress.SetValue(percent)


# end of class AudiobookEntry

class QueuePanel(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.SetScrollRate(10, 10)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.sizer)

        self.Layout()

    def add_audiobook(self, audiobook):
        book = AudiobookEntry(self, audiobook)
        self.sizer.Add(book, 0, wx.ALL | wx.EXPAND, 0)
        self.Layout()
        return book


class QueueFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1024, 800))
        self.SetTitle("frame")

        self.queue = QueuePanel(self, wx.ID_ANY)
        self.Layout()

        self.queue.add_audiobook("1.m4b")
        self.queue.add_audiobook("2.m4b")
        self.queue.add_audiobook("3.m4b")


class QueueApp(wx.App):
    def OnInit(self):
        self.frame = QueueFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    QuePanel = QueueApp(0)
    QuePanel.MainLoop()
