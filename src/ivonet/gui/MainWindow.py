#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-04 22:53:22$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The Main Application Window
"""

import ast
import os
import pickle
from configparser import ConfigParser

import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import ivonet
from ivonet.events import ee, dbg, log
from ivonet.gui.MainPanel import MainPanel
from ivonet.gui.MenuBar import MenuBar, FILE_MENU_QUEUE
from ivonet.image.IvoNetArtProvider import IvoNetArtProvider
from ivonet.model.Project import Project

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

        self.project = Project()
        wx.ArtProvider.Push(IvoNetArtProvider())

        self.SetSize((1024, 768))
        self.SetMinSize((1024, 768))

        self.__make_toolbar()
        self.SetMenuBar(MenuBar(self))

        self.CreateStatusBar()
        self.SetStatusText(ivonet.TXT_COPYRIGHT)

        self.status_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_clear_status, self.status_timer)

        # This timer checks every half second if the project has
        # enough information to enable queue
        self.verify_project_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_verify_project, self.verify_project_timer)
        self.verify_project_timer.Start(500)

        self.main_panel = MainPanel(self, wx.ID_ANY)
        self.load_settings()
        self.Layout()
        self.init()

    def init(self):
        # Remove old log file if still exists
        if os.path.isfile(ivonet.LOG_FILE):
            os.remove(ivonet.LOG_FILE)

        # Tell the world we started anew
        self.new_project()

        # Register events
        ee.on("status", self.ee_on_status)
        ee.on("project.open", self.ee_project_open)

    def new_project(self):
        ee.emit("project.new", self.project)
        # dbg(self.project)
        log("Starting new project or loading one")

    # noinspection PyUnusedLocal
    def on_verify_project(self, event):
        """Handler for the 'verify_project_timer' event
        It feels a bit like a hack but the cleanest I could think of for now.
        """
        enable_disable = self.project.verify()
        self.GetToolBar().EnableTool(ivonet.TOOLBAR_ID_QUEUE, enable_disable)
        self.GetMenuBar().Enable(FILE_MENU_QUEUE, enable_disable)
        # dbg("on_verify_project:", enable_disable)

    def __make_toolbar(self):
        """Toolbar"""
        tool_bar_size = (256, 256)
        tool_bar = self.CreateToolBar((wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT))
        tool_bar.SetToolBitmapSize(tool_bar_size)

        tool_buttons = [
            (ivonet.TOOLBAR_ID_OPEN_PROJECT, "open", "Open project", self.on_open_project, True),
            (ivonet.TOOLBAR_ID_SAVE_PROJECT, "save", "Save project", self.on_save_project, True),
            (ivonet.TOOLBAR_ID_SEPARATOR, None, None, None, False),
            (ivonet.TOOLBAR_ID_QUEUE, "queue", "Queue for processing", self.on_queue, False),
        ]
        for art_id, label, short_help, func, enabled in tool_buttons:
            if art_id <= 0:
                tool_bar.AddSeparator()
            else:
                bmp = wx.ArtProvider.GetBitmap("{prefix}{label}".format(
                    prefix=ivonet.ART_PREFIX,
                    label=label.upper()),
                    wx.ART_TOOLBAR, tool_bar_size)
                tool_bar.AddTool(art_id, label.capitalize(), bmp, short_help, wx.ITEM_NORMAL)
                self.Bind(wx.EVT_TOOL, func, id=art_id)
                tool_bar.EnableTool(art_id, enabled)

        tool_bar.Realize()

    # noinspection PyUnusedLocal
    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.save_settings()
        self.verify_project_timer.Stop()
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
    def on_queue(self, event):
        status("Processing...")
        # TODO Clean project on process (will also disable the process button)
        #  Disables the process button
        ee.emit("queue.project", self.project)
        self.on_clear(None)
        log("Queued audiobook for processing")

    # noinspection PyUnusedLocal
    @staticmethod
    def on_select_dir(event):
        status("Select directory")
        # TODO implement me or design something better like a global settings thingy to be saved on exit or sumsuch
        dbg("TODO: on_select_dir")

    # noinspection PyUnusedLocal
    def on_open_project(self, event):
        status("Open Project")
        open_dlg = wx.FileDialog(
            self,
            message="Choose a file...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=ivonet.FILE_WILDCARD,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
        )
        if open_dlg.ShowModal() == wx.ID_OK:
            path = open_dlg.GetPath()
            log(f"Opening file: {path}")
            self.ee_project_open(path)
            ee.emit("project.history", path)
        open_dlg.Destroy()

    def ee_project_open(self, path):
        """Handler for th 'project.open' event and the Project open dialog"""
        with open(path, 'rb') as fi:
            self.project = pickle.load(fi)
            self.new_project()

    # noinspection PyUnusedLocal
    def on_save_project(self, event):
        status("Save Project")
        filename = self.project.title or "Untitled"
        filename += ".ivo"
        base_dir = None
        if self.project.name:
            base_dir, filename = os.path.split(self.project.name)
        elif self.project.tracks:
            base_dir = os.path.split(self.project.tracks[0])[0]

        default_dir = os.environ["HOME"] or os.getcwd()

        # TODO use with... https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        save_dlg = wx.FileDialog(
            self,
            message="Save file as ...",
            defaultDir=default_dir,
            defaultFile=f"{filename}",
            wildcard=ivonet.FILE_WILDCARD,
            style=wx.FD_SAVE
        )

        save_dlg.SetFilterIndex(0)
        if base_dir:
            save_dlg.SetDirectory(base_dir)

        if save_dlg.ShowModal() == wx.ID_OK:
            path = save_dlg.GetPath()
            if not path.endswith(".ivo"):
                path += ".ivo"
            with open(path, 'wb') as fo:
                self.project.name = path
                pickle.dump(self.project, fo)
            ee.emit("project.history", path)
            log(f'Saved to: {path}')

        save_dlg.Destroy()

    # noinspection PyUnusedLocal
    def on_clear(self, event):
        status("Starting new project")
        self.project = Project()
        self.new_project()

    def ee_on_status(self, msg):
        self.SetStatusText(msg)
        if not self.status_timer.IsRunning():
            self.status_timer.Start(2000)

    # noinspection PyUnusedLocal
    def on_clear_status(self, event):
        self.SetStatusText(ivonet.TXT_COPYRIGHT)
        if self.status_timer.IsRunning():
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
        ee.emit("project.load_history_file")
