#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import os

import wx

import ivonet
from ivonet.book.meta import GENRES, CHAPTER_LIST
from ivonet.events import ee, _
from ivonet.image import IMAGE_TYPES

try:
    from ivonet.image.images import yoda
except ImportError:
    raise ImportError("The images file was not found. Did you forget to generate them?")


class CoverArtDropTarget(wx.FileDropTarget):
    """Listening to image drops on the target it is set to

    This FileDropTarget does not need any init parameters as it will only
    emit an event containing the image file name.

    This drop target will check if the file dropped is an image before
    emitting the event.

    The subscriber is responsible for processing the image.
    """

    def __init__(self):
        super().__init__()

    def OnDropFiles(self, x, y, filenames):
        ee.emit("log", "Cover art dropped")
        if len(filenames) > 1:
            ee.emit("log", "More than one cover art image was dropped. Taking only the first")
        split_filename = os.path.splitext(filenames[0])
        if len(split_filename) != 2:
            ee.emit("log", "The file dropped is probably not an image.")
            return False
        if split_filename[1] in IMAGE_TYPES:
            ee.emit("coverart.dnd", filenames[0])
        else:
            ee.emit("log", f"File {filenames[0]} is not an image.")
            return False
        return True


class AudiobookMetaDataPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        ee.on("coverart.dnd", self.on_conver_art)
        self.PhotoMaxSize = 350

        hs_left_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        fgs_lft_pnl_m4b_page = wx.FlexGridSizer(3, 1, 4, 0)
        hs_left_pnl_m4b_page.Add(fgs_lft_pnl_m4b_page, 1, wx.ALL | wx.EXPAND, 0)

        fgs_mp3_metadata = wx.FlexGridSizer(6, 2, 4, 16)
        fgs_lft_pnl_m4b_page.Add(fgs_mp3_metadata, 1, wx.EXPAND, 0)

        lbl_title = wx.StaticText(self, wx.ID_ANY, "Title")
        fgs_mp3_metadata.Add(lbl_title, 1, 0, 0)

        self.tc_title = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_title.SetToolTip("Title of the book")
        fgs_mp3_metadata.Add(self.tc_title, 0, wx.EXPAND, 0)

        lbl_artist = wx.StaticText(self, wx.ID_ANY, "Artist")
        fgs_mp3_metadata.Add(lbl_artist, 0, wx.EXPAND, 0)

        self.tc_artist = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_artist.SetToolTip("The author or album artist")
        fgs_mp3_metadata.Add(self.tc_artist, 0, wx.EXPAND, 0)

        lbl_grouping = wx.StaticText(self, wx.ID_ANY, "Grouping")
        fgs_mp3_metadata.Add(lbl_grouping, 1, 0, 0)

        self.tc_grouping = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_grouping.SetToolTip("Grouping e.g. series")
        fgs_mp3_metadata.Add(self.tc_grouping, 0, wx.EXPAND, 0)

        lbl_genre = wx.StaticText(self, wx.ID_ANY, "Genre")
        fgs_mp3_metadata.Add(lbl_genre, 0, 0, 0)

        self.cb_genre = wx.ComboBox(self, wx.ID_ANY,
                                    choices=GENRES,
                                    style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        self.cb_genre.SetToolTip("Select your genre")
        self.cb_genre.SetSelection(0)
        fgs_mp3_metadata.Add(self.cb_genre, 0, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

        label_1 = wx.StaticText(self, wx.ID_ANY, "Chapter text")
        fgs_mp3_metadata.Add(label_1, 0, 0, 0)

        self.tc_chapter_text = wx.TextCtrl(self, wx.ID_ANY, "Chapter")
        self.tc_chapter_text.SetToolTip("Text to use fore chapterisation")
        fgs_mp3_metadata.Add(self.tc_chapter_text, 0, wx.EXPAND, 0)

        lbl_chapterisation = wx.StaticText(self, wx.ID_ANY, "Chapters")
        fgs_mp3_metadata.Add(lbl_chapterisation, 1, 0, 0)

        self.cb_chapterisation = wx.ComboBox(self, wx.ID_ANY,
                                             choices=CHAPTER_LIST,
                                             style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SIMPLE)
        self.cb_chapterisation.SetToolTip("Choose which chapterisation method is preferred")
        self.cb_chapterisation.SetSelection(0)
        fgs_mp3_metadata.Add(self.cb_chapterisation, 0, wx.EXPAND, 0)

        vs_mp3_metadata_1 = wx.BoxSizer(wx.VERTICAL)
        fgs_lft_pnl_m4b_page.Add(vs_mp3_metadata_1, 1, wx.EXPAND, 0)

        vs_track_year_comment = wx.BoxSizer(wx.VERTICAL)
        vs_mp3_metadata_1.Add(vs_track_year_comment, 1, wx.EXPAND, 0)

        hs_track_year = wx.BoxSizer(wx.HORIZONTAL)
        vs_track_year_comment.Add(hs_track_year, 0, wx.ALL | wx.EXPAND, 0)

        lbl_track = wx.StaticText(self, wx.ID_ANY, "Track")
        hs_track_year.Add(lbl_track, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        hs_track_year.Add((60, 20), 0, 0, 0)

        self.sc_track = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=100)
        self.sc_track.SetToolTip("e.g. the series title")
        hs_track_year.Add(self.sc_track, 0, 0, 0)

        label_8 = wx.StaticText(self, wx.ID_ANY, "of")
        hs_track_year.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.sc_track_total = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=100)
        hs_track_year.Add(self.sc_track_total, 0, 0, 0)

        hs_track_year.Add((32, 20), 0, 0, 0)

        lbl_year = wx.StaticText(self, wx.ID_ANY, "Year")
        hs_track_year.Add(lbl_year, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.tc_year = wx.TextCtrl(self, wx.ID_ANY, "")
        self.tc_year.SetToolTip("Publication year")
        hs_track_year.Add(self.tc_year, 1, wx.EXPAND, 0)

        vs_comment = wx.BoxSizer(wx.VERTICAL)
        vs_track_year_comment.Add(vs_comment, 0, wx.EXPAND, 0)

        vs_comment_1 = wx.BoxSizer(wx.VERTICAL)
        vs_comment.Add(vs_comment_1, 2, wx.ALL | wx.EXPAND, 0)

        lbl_comment = wx.StaticText(self, wx.ID_ANY, "Comment")
        vs_comment_1.Add(lbl_comment, 0, wx.LEFT, 0)

        self.tc_comment = wx.TextCtrl(self, wx.ID_ANY, ivonet.TXT_COMMENT, style=wx.TE_MULTILINE)
        self.tc_comment.SetToolTip("Add your comments here")
        vs_comment_1.Add(self.tc_comment, 2, wx.EXPAND, 0)

        vs_mp3_metadata_2 = wx.BoxSizer(wx.VERTICAL)
        fgs_lft_pnl_m4b_page.Add(vs_mp3_metadata_2, 1, wx.EXPAND, 0)

        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        vs_mp3_metadata_2.Add(sizer_17, 1, wx.ALL | wx.EXPAND, 0)

        label_11 = wx.StaticText(self, wx.ID_ANY, "Cover art")
        sizer_17.Add(label_11, 0, 0, 0)

        self.pnl_cover_art = wx.Panel(self, wx.ID_ANY)

        sizer_17.Add(self.pnl_cover_art, 1, wx.ALL | wx.EXPAND, 0)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.cover_art = wx.StaticBitmap(self.pnl_cover_art, wx.ID_ANY,
                                         yoda.GetBitmap())
        self.cover_art.SetDropTarget(CoverArtDropTarget())
        self.cover_art.SetToolTip("Drag and drop Cover Art here")

        sizer_1.Add(self.cover_art, 1, wx.EXPAND, 0)

        self.pnl_cover_art.SetSizer(sizer_1)

        fgs_mp3_metadata.AddGrowableCol(1)

        fgs_lft_pnl_m4b_page.AddGrowableRow(2)

        self.SetSizer(hs_left_pnl_m4b_page)

        self.Layout()

        self.Bind(wx.EVT_TEXT, self.on_title, self.tc_title)
        self.Bind(wx.EVT_TEXT, self.on_artist, self.tc_artist)
        self.Bind(wx.EVT_TEXT, self.on_grouping, self.tc_grouping)
        self.Bind(wx.EVT_COMBOBOX, self.on_genre, self.cb_genre)
        self.Bind(wx.EVT_TEXT, self.on_chapter_text, self.tc_chapter_text)
        self.Bind(wx.EVT_COMBOBOX, self.on_chapter_method, self.cb_chapterisation)
        self.Bind(wx.EVT_SPINCTRL, self.on_track, self.sc_track)
        self.Bind(wx.EVT_SPINCTRL, self.on_track_total, self.sc_track_total)
        self.Bind(wx.EVT_TEXT, self.on_year, self.tc_year)
        self.Bind(wx.EVT_TEXT, self.on_comment, self.tc_comment)

        ee.on("track.title", self.on_title)
        # ee.on()

    def on_conver_art(self, image):
        ee.emit("log", f"Setting cover art to: {image}")
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        width = img.GetWidth()
        height = img.GetHeight()
        if width > height:
            new_width = self.PhotoMaxSize
            new_height = self.PhotoMaxSize * height / width
        else:
            new_height = self.PhotoMaxSize
            new_width = self.PhotoMaxSize * width / height
        img = img.Scale(new_width, new_height)

        self.cover_art.SetBitmap(wx.Bitmap(img))
        self.cover_art.Center()
        self.pnl_cover_art.Refresh()

    def on_title(self, event):
        ee.emit("log", "Event handler 'on_title' not implemented!")
        event.Skip()

    def on_artist(self, event):
        ee.emit("log", "Event handler 'on_artist' not implemented!")
        event.Skip()

    def on_grouping(self, event):
        ee.emit("log", "Event handler 'on_grouping' not implemented!")
        event.Skip()

    def on_genre(self, event):
        ee.emit("log", "Event handler 'on_genre' not implemented!")
        _("Event handler 'on_genre' not implemented!")
        event.Skip()

    def on_chapter_text(self, event):
        ee.emit("log", "Event handler 'on_chapter_text' not implemented!")
        event.Skip()

    def on_chapter_method(self, event):
        ee.emit("log", "Event handler 'on_chapter_method' not implemented!")
        event.Skip()

    def on_track(self, event):
        ee.emit("log", "Event handler 'on_track' not implemented!")
        event.Skip()

    def on_track_total(self, event):
        ee.emit("log", "Event handler 'on_track_total' not implemented!")
        event.Skip()

    def on_year(self, event):
        ee.emit("log", "Event handler 'on_year' not implemented!")
        event.Skip()

    def on_comment(self, event):
        ee.emit("log", "Event handler 'on_comment' not implemented!")
        event.Skip()

# end of class AudiobookMetaDataPanel
