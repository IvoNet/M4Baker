#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import wx

from ivonet.gui.LogPanel import LogPanel
from ivonet.gui.MetadataPanel import MetadataPanel
from ivonet.gui.QueuePanel import QueuePanel


class NoteBook(wx.Notebook):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.NB_TOP
        wx.Notebook.__init__(self, *args, **kwds)

        self.nb_m4b_page = MetadataPanel(self, wx.ID_ANY)
        self.AddPage(self.nb_m4b_page, "Audio")

        self.main_notebook_Queue = QueuePanel(self, wx.ID_ANY)
        self.AddPage(self.main_notebook_Queue, "Queue")

        self.main_notebook_Log = LogPanel(self, wx.ID_ANY)
        self.AddPage(self.main_notebook_Log, "Log")
