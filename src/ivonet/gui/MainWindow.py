#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import ivonet
from ivonet.events import ee, _
from ivonet.gui.MenuBar import MenuBar
from ivonet.image.IvoNetArtProvider import IvoNetArtProvider
from ivonet.image.images import yoda
from ivonet.sys.application import data_directory


class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        """Initialize the gui here"""
        super(MainWindow, self).__init__(*args, **kw)

        wx.ArtProvider.Push(IvoNetArtProvider())

        self.__make_toolbar()
        self.SetMenuBar(MenuBar(self))

        self.CreateStatusBar()
        self.SetStatusText("M4Baker (c) 2021 by IvoNet.nl")

        self.init()

    def init(self):
        # Register events
        ee.on("log", self.on_log)

        _("MainWindows initialized")

    def __make_toolbar(self):
        """Toolbar"""
        tool_bar_size = (48, 48)
        tool_bar = self.CreateToolBar((wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT))
        tool_bar.SetToolBitmapSize(tool_bar_size)

        # Define new tool bar buttons here (
        tool_buttons = [
            ("process", "Start processing", self.on_process),
            ("stop", "Stop processing", self.on_stop_process),
            ("log", "Show Log", self.on_show_log),
        ]
        for art_id, value in enumerate(tool_buttons, start=1):
            label, short_help, func = value
            bmp = wx.ArtProvider.GetBitmap("{prefix}{label}".format(prefix=ivonet.ART_PREFIX, label=label.upper()),
                                           wx.ART_TOOLBAR, tool_bar_size)
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
        _("TODO: on_process")

    # noinspection PyUnusedLocal
    def on_stop_process(self, event):
        _("TODO: on_stop_process")

    # noinspection PyUnusedLocal
    def on_select_dir(self, event):
        _("TODO: on_select_dir -> " + data_directory())

    # noinspection PyUnusedLocal
    def on_clear(self, event):
        _("TODO: on_clear")

    # noinspection PyUnusedLocal
    def on_show_log(self, event):
        _("TODO: on_show_log")

    @staticmethod
    def on_log(*args):
        print(" ".join(args))
