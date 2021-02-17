#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(self, parent, title, size=(640,480))


def main():
    app = wx.App(False)
    frame = MainWindow(None, "B4Baker")
    app.MainLoop()


if __name__ == '__main__':
    main()
