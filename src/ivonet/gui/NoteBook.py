#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx

from ivonet.events import _


class NoteBook(wx.Notebook):
    def __init__(self, parent, note_id, size=(21, 21), style=wx.BK_DEFAULT):
        super().__init__(parent, id=note_id, size=size, style=style)

        win =

        _("Initializing Notebook")
