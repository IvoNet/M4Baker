#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx

from ivonet.gui import MainWindow


def main():
    app = wx.App(False)
    frame = MainWindow(None, title="B4Baker", size=(800, 600))
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
