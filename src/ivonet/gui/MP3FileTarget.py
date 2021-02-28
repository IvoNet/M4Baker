#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 16:36:23$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
MP3 File Drag and Drop code
"""

import wx
import wx.adv

from ivonet.events import log, ee, _
from ivonet.model.Track import Track


class MP3DropTarget(wx.FileDropTarget):

    def __init__(self, target):
        super().__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        log("MP3 Files dropped")

        for name in filenames:
            if name.lower().endswith(".mp3") and name not in self.target.GetStrings():
                Track(name, silent=False)
                self.target.append(name)
            else:
                log(f"Dropped file '{name}' is not an mp3 file or not unique in the list.")
        return True


# TODO re-evaluate this inspection later...
# noinspection PyMethodMayBeStatic
class MP3ListBox(wx.adv.EditableListBox):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetStrings([])
        self.SetDropTarget(MP3DropTarget(self))
        self.SetToolTip("Drag and Drop MP3 files here")
        self.del_button = self.GetDelButton()
        self.GetDownButton().Bind(wx.EVT_LEFT_DOWN, self.tracks_changed)
        # self.GetDownButton().Bind(wx.EVT_LEFT_DOWN, self.on_move_down)

        self.GetUpButton().Bind(wx.EVT_LEFT_DOWN, self.tracks_changed)
        # self.GetUpButton().Bind(wx.EVT_LEFT_DOWN, self.on_move_up)

        # self.GetDelButton().Bind(wx.EVT_LEFT_DOWN, self.on_delete)

        self.GetListCtrl().Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_selected)
        self.GetListCtrl().Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_selected_right_click)

        self.GetListCtrl().Bind(wx.EVT_LIST_DELETE_ITEM, self.tracks_changed)
        self.GetListCtrl().Bind(wx.EVT_LIST_INSERT_ITEM, self.tracks_changed)
        # self.GetListCtrl().Bind(wx.EVT_LIST_DELETE_ITEM, self.on_delete)
        # self.GetListCtrl().Bind(wx.EVT_LIST_INSERT_ITEM, self.on_insert_item)

    def append(self, line):
        lines = list(self.GetStrings())
        lines.append(line)
        self.SetStrings(lines)
        # ee.emit("mp3.added", line)

    def clear(self):
        self.SetStrings([])

    def tracks_changed(self, event):
        ee.emit("project.tracks", self.GetStrings())
        # TODO This event is too early! the change takes place after
        #  this event in the propagaton. How to fix?!
        event.Skip()

    def on_selected(self, event):
        _(f"Item selected [{event.GetItem().GetText()}]")
        event.Skip()

    def on_selected_right_click(self, event):
        _("TODO on_selected_right_click")
        event.Skip()


class MP3FileTarget(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        hs_right_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        bs_right_pnl_m4b_page = wx.BoxSizer(wx.VERTICAL)
        hs_right_pnl_m4b_page.Add(bs_right_pnl_m4b_page, 1, wx.EXPAND, 0)

        self.mp3_list_box = MP3ListBox(self, wx.ID_ANY, "Drag and Drop mp3 files below...",
                                       style=wx.adv.EL_ALLOW_DELETE)

        bs_right_pnl_m4b_page.Add(self.mp3_list_box, 1, wx.EXPAND, 0)

        self.SetSizer(hs_right_pnl_m4b_page)

        self.Layout()
        # ee.on("audiobook.track", self.ee_on_track)
        ee.on("project.new", self.ee_on_new_audiobook)

    def ee_on_track(self, track: Track):
        self.mp3_list_box.append(track.mp3)

    def ee_on_new_audiobook(self, project):
        self.mp3_list_box.clear()
