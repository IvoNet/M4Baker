#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 15:21:03$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The Main Application Panel
"""

import ast
import os
from configparser import ConfigParser

import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import ivonet
from ivonet.events import ee, _, log
from ivonet.gui.MainPanel import MainPanel
from ivonet.gui.MenuBar import MenuBar
from ivonet.image.IvoNetArtProvider import IvoNetArtProvider
from ivonet.model.Audiobook import Audiobook

try:
    from ivonet.image.images import yoda
except ImportError:
    raise ImportError("The images file was not found. Did you forget to generate them?")


def status(msg):
    """Emits a status bar event message."""
    ee.emit("status", msg)


class MainFrame(wx.Frame):
    """The main application Frame holding all the other panels"""

    def __init__(self, *args, **kw):
        """Initialize the gui here"""
        super().__init__(*args, **kw)

        self.audiobook = Audiobook()

        self.SetSize((1024, 768))
        self.SetMinSize((1024, 768))

        wx.ArtProvider.Push(IvoNetArtProvider())

        self.__make_toolbar()
        self.SetMenuBar(MenuBar(self))

        self.CreateStatusBar()
        self.SetStatusText(ivonet.TXT_COPYRIGHT)

        self.status_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.clear_status, self.status_timer)

        self.main_panel = MainPanel(self, wx.ID_ANY)
        self.load_settings()
        self.Layout()
        self.init()
        _("MainFrame initialized")

    def init(self):
        # Register events
        ee.on("status", self.on_status)
        ee.on("audiobook.mp3s", self.audiobook.add_all)
        ee.on("audiobook.grouping", self.audiobook.set_grouping)
        ee.on("audiobook.title", self.audiobook.set_title)
        ee.on("audiobook.artist", self.audiobook.set_artist)
        ee.on("audiobook.disc", self.audiobook.set_disc)
        ee.on("audiobook.disc_total", self.audiobook.set_disc_total)
        ee.on("audiobook.comment", self.audiobook.set_comment)
        ee.on("audiobook.year", self.audiobook.set_year)

    def __make_toolbar(self):
        """Toolbar"""
        tool_bar_size = (256, 256)
        tool_bar = self.CreateToolBar((wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT))
        tool_bar.SetToolBitmapSize(tool_bar_size)

        tool_buttons = [
            ("process", "Start processing", self.on_process),
            ("stop", "Stop processing", self.on_stop_process),
            ("clear", "Clean Audiobook", self.on_clear),
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
        self.save_settings()
        self.Close(True)

    # noinspection PyUnusedLocal
    def on_about(self, event):
        """Display an About Dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName(ivonet.TXT_APP_NAME)
        info.SetVersion(ivonet.VERSION)
        info.SetCopyright(ivonet.TXT_COPYRIGHT)
        info.SetDescription(wordwrap(ivonet.TXT_ABOUT_DESCRIPTION, 350, wx.ClientDC(self)))
        info.SetWebSite(ivonet.TXT_URL_BLOG, ivonet.TXT_DESCRIPTION_BLOG)
        info.SetDevelopers(ivonet.DEVELOPERS)
        info.SetLicense(wordwrap(ivonet.TXT_LICENSE, 500, wx.ClientDC(self)))
        info.SetIcon(yoda.GetIcon())
        wx.adv.AboutBox(info, self)

    # noinspection PyUnusedLocal
    @staticmethod
    def on_process(event):
        status("Processing...")
        ee.emit("processing.start", event)
        log("Started processing")

    # noinspection PyUnusedLocal
    @staticmethod
    def on_stop_process(event):
        status("Stop processing")
        ee.emit("processing.stop", event)
        log("Stopped processing")

    # noinspection PyUnusedLocal
    @staticmethod
    def on_select_dir(event):
        status("Select directory")
        _("TODO: on_select_dir")

    # noinspection PyUnusedLocal
    def on_clear(self, event):
        status("Starting new Audiobook")
        log("Starting new Audiobook")
        self.audiobook = Audiobook()

    def on_status(self, msg):
        self.SetStatusText(msg)
        if not self.status_timer.IsRunning():
            _("Starting the StatusBar timer")
            self.status_timer.Start(3000)

    # noinspection PyUnusedLocal
    def clear_status(self, event):
        self.SetStatusText(ivonet.TXT_COPYRIGHT)
        if self.status_timer.IsRunning():
            _("Stopping the StatusBar timer")
            self.status_timer.Stop()

    def save_settings(self):
        """save_settings() -> Saves default settings to the application settings location"""
        ini = ConfigParser()
        ini.add_section("Settings")
        ini.set('Settings', 'screen_size', str(self.GetSize()))
        ini.set('Settings', 'screen_pos', str(self.GetPosition()))
        with open(ivonet.SETTINGS_FILE, "w") as fp:
            ini.write(fp)

    def load_settings(self):
        """Load_ settings() -> Loads and activates the settings saved by save_settings()"""
        if os.path.isfile(ivonet.SETTINGS_FILE):
            ini = ConfigParser()
            ini.read(ivonet.SETTINGS_FILE)
            self.SetSize(ast.literal_eval(ini.get('Settings', 'screen_size')))
            self.SetPosition(ast.literal_eval(ini.get('Settings', 'screen_pos')))
        else:
            self.Center()
