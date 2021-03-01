#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-02 00:02:09$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The Menubar
"""

import os

import wx

# File Menu
import ivonet
from ivonet.events import log, ee, _

FILE_MENU_PROCESS = wx.NewIdRef()
FILE_MENU_STOP_PROCESS = wx.NewIdRef()
FILE_MENU_TO_DIR = wx.NewIdRef()


class MenuBar(wx.MenuBar):
    """The Application menu."""
    def __init__(self, parent, style=0):
        super().__init__(style)
        self.parent = parent

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_NEW, "New \tCTRL-N")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_OPEN, "Open... \tCTRL-O")
        file_menu.Append(wx.ID_SAVE, "Save... \tCTRL-S")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_PROCESS, "Process\tCTRL-P")
        file_menu.Append(FILE_MENU_STOP_PROCESS, "Stop Processing\tCTRL-E")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_TO_DIR, "Select output folder\tCTRL-D")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "Quit\tCTRL-Q")

        self.file_history = wx.FileHistory()
        self.file_history.UseMenu(file_menu)
        self.Bind(wx.EVT_MENU_RANGE, self.on_file_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)

        self.Append(file_menu, "&File")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT)

        self.Append(help_menu, "&Help")
        ee.on("project.history", self.ee_project_history)
        ee.on("project.load_history_file", self.ee_load_history_file)

        # Create event handlers
        menu_handlers = [
            (FILE_MENU_PROCESS, self.parent.on_process),
            (FILE_MENU_STOP_PROCESS, self.parent.on_stop_process),
            (wx.ID_NEW, self.parent.on_clear),
            (FILE_MENU_TO_DIR, self.parent.on_select_dir),
            (wx.ID_OPEN, self.parent.on_open_project),
            (wx.ID_SAVE, self.parent.on_save_project),
            (wx.ID_EXIT, self.parent.on_exit),
            (wx.ID_ABOUT, self.parent.on_about),
        ]
        for menu_id, handler in menu_handlers:
            self.parent.Bind(wx.EVT_MENU, handler, id=menu_id)

    def on_file_history(self, event):
        """Handler for the event on file history selection in the file menu"""
        file_num = event.GetId() - wx.ID_FILE1
        path = self.file_history.GetHistoryFile(file_num)
        ee.emit("project.open", path)
        self.ee_project_history(path)
        log(f"You selected {path}")

    def ee_project_history(self, path):
        """handler for the 'project.history' event.
        it will add it to the history (again) for the ranking and then save
        to settings so it can be reloaded on restart.
        """
        self.file_history.AddFileToHistory(path)
        self.save_history()

    def save_history(self):
        """Saves the recent file history to disk"""
        _("save_history")
        history_config = wx.FileConfig()
        self.file_history.Save(history_config)
        with open(ivonet.HISTORY_FILE, "wb") as fo:
            history_config.Save(fo)

    def ee_load_history_file(self):
        """Loads last file history settings from disk"""
        # TODO AutoSave option exists. should I use it?
        _("ee_load_history_file")
        if os.path.isfile(ivonet.HISTORY_FILE):
            history_config = wx.FileConfig(localFilename=ivonet.HISTORY_FILE,
                                           style=wx.CONFIG_USE_LOCAL_FILE)
            self.file_history.Load(history_config)
