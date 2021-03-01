#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx

# File Menu
FILE_MENU_PROCESS = wx.NewIdRef()
FILE_MENU_NEW = wx.NewIdRef()
FILE_MENU_STOP_PROCESS = wx.NewIdRef()
FILE_MENU_OPEN = wx.NewIdRef()
FILE_MENU_SAVE = wx.NewIdRef()
FILE_MENU_TO_DIR = wx.NewIdRef()


class MenuBar(wx.MenuBar):
    def __init__(self, parent, style=0):
        super().__init__(style)
        self.parent = parent

        file_menu = wx.Menu()
        file_menu.Append(FILE_MENU_NEW, "New \tCTRL-N")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_OPEN, "Open... \tCTRL-O")
        file_menu.Append(FILE_MENU_SAVE, "Save... \tCTRL-S")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_PROCESS, "Process\tCTRL-P")
        file_menu.Append(FILE_MENU_STOP_PROCESS, "Stop Processing\tCTRL-E")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_TO_DIR, "Select output folder\tCTRL-D")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "Quit\tCTRL-Q")

        self.Append(file_menu, "&File")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT)

        self.Append(help_menu, "&Help")

        # Create event handlers
        menu_handlers = [
            (FILE_MENU_PROCESS, self.parent.on_process),
            (FILE_MENU_STOP_PROCESS, self.parent.on_stop_process),
            (FILE_MENU_NEW, self.parent.on_clear),
            (FILE_MENU_TO_DIR, self.parent.on_select_dir),
            (FILE_MENU_OPEN, self.parent.on_open_project),
            (FILE_MENU_SAVE, self.parent.on_save_project),
            (wx.ID_EXIT, self.parent.on_exit),
            (wx.ID_ABOUT, self.parent.on_about),
        ]
        for menu_id, handler in menu_handlers:
            self.parent.Bind(wx.EVT_MENU, handler, id=menu_id)


