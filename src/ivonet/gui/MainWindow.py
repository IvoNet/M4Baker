#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import ivonet
from ivonet.gui import MenuBar
from ivonet.image.IvoNetArtProvider import IvoNetArtProvider
from ivonet.image.images import yoda


class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        self.on_init()

    def on_init(self):
        """Initializes the instance"""
        wx.ArtProvider.Push(IvoNetArtProvider())

        self.__make_toolbar()
        self.SetMenuBar(MenuBar(self))

        self.CreateStatusBar()
        self.SetStatusText("M4Baker (c) 2021 by IvoNet.nl")

    def __make_toolbar(self):
        """Toolbar"""
        tool_bar_size = (48, 48)
        tool_bar = self.CreateToolBar((wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT))
        tool_bar.SetToolBitmapSize(tool_bar_size)

        tool_buttons = [
            ("process", "Start processing", self.on_process),
            ("stop", "Stop processing", self.on_stop_process),
            ("log", "Show Log", self.on_show_log),
        ]
        for idx, value in enumerate(tool_buttons, start=1):
            label, short_help, func = value
            art_id = idx * 10
            bmp = wx.ArtProvider.GetBitmap("inART_{label}".format(label=label.upper()), wx.ART_TOOLBAR, tool_bar_size)
            tool_bar.AddTool(art_id, label.capitalize(), bmp, short_help, wx.ITEM_NORMAL)
            self.Bind(wx.EVT_TOOL, func, id=art_id)

        tool_bar.Realize()

    # noinspection PyUnusedLocal
    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    # noinspection PyUnusedLocal
    def on_about(self, event):
        """Display an About Dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName(ivonet.APP_NAME)
        info.SetVersion(ivonet.VERSION)
        info.SetCopyright(ivonet.COPYRIGHT)
        info.SetDescription(wordwrap(ivonet.ABOUT_DESCRIPTION, 350, wx.ClientDC(self)))
        info.SetWebSite(ivonet.BLOG, ivonet.BLOG_DESCRIPTION)
        info.SetDevelopers(ivonet.DEVELOPERS)
        info.SetLicense(wordwrap(ivonet.LICENSE, 500, wx.ClientDC(self)))
        info.SetIcon(yoda.GetIcon())
        wx.adv.AboutBox(info, self)

    # noinspection PyUnusedLocal
    def on_process(self, event):
        self.SetStatusText("TODO: on_process")

    # noinspection PyUnusedLocal
    def on_stop_process(self, event):
        self.SetStatusText("TODO: on_stop_process")

    # noinspection PyUnusedLocal
    def on_select_dir(self, event):
        self.SetStatusText("TODO: on_select_dir")

    # noinspection PyUnusedLocal
    def on_clear(self, event):
        self.SetStatusText("TODO: on_clear")

    # noinspection PyUnusedLocal
    def on_show_log(self, event):
        self.SetStatusText("TODO: on_show_log")
