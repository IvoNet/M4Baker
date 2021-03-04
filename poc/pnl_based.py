#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 03/03/2021 22:04$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx
import wx.lib.scrolledpanel as scrolled


class DownloadPanel(wx.Panel):

    def __init__(self, parent, filename, size):
        wx.Panel.__init__(self, parent)

        self.size = size

        self.f = wx.StaticText(self, -1, filename)
        self.p = wx.Gauge(self, -1, size, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        b = wx.Button(self, -1, "Cancel")

        sz = wx.BoxSizer(wx.HORIZONTAL)
        sz.Add(self.f, 0, wx.ALL, 5)
        sz.Add(self.p, 1, wx.ALL | wx.EXPAND, 5)
        sz.Add(b, 0, wx.ALL, 5)

        self.SetSizer(sz)

        self.Bind(wx.EVT_BUTTON, self.OnCancel, b)

    def UpdateProgress(self, s):
        self.p.SetValue(s)

    def OnCancel(self, e):
        pass
        # do whatever you need to do to cancel.


class DownloadContainer(scrolled.ScrolledPanel):

    def __init__(self, parent, id=wx.ID_ANY, style=wx.TAB_TRAVERSAL, ):
        super().__init__(parent, id=id, style=style)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def AddDownload(self, filename, size):
        d = DownloadPanel(self, filename, size)
        self.sizer.Prepend(d, 0, wx.ALL, 2)
        self.Layout()
        return d  # for later calls to d.UpdateProgress(...)


class MyFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "UltimateListCtrl Demo")

        list = DownloadContainer(self)

        list.AddDownload("Filename.m4b", 100)
        list.AddDownload("Filename.m4b", 100)
        list.AddDownload("Filename.m4b", 50)
        list.AddDownload("Filename.m4b", 100)
        list.AddDownload("Filename.m4b", 100)
        list.AddDownload("Filename.m4b", 100)
        list.AddDownload("Filename.m4b", 10)
        list.AddDownload("Filename.m4b", 100)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list, 1, wx.EXPAND)
        self.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
