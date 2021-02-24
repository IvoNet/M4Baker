#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import os

import wx

import ivonet
from ivonet.book.meta import GENRES, CHAPTER_LIST
from ivonet.events import ee, log
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
        log("Cover art dropped")
        if len(filenames) > 1:
            log("More than one cover art image was dropped. Taking only the first")
        split_filename = os.path.splitext(filenames[0])
        if len(split_filename) != 2:
            log("The file dropped is probably not an image.")
            return False
        if split_filename[1] in IMAGE_TYPES:
            ee.emit("coverart.dnd", filenames[0])
        else:
            log(f"File {filenames[0]} is not an image.")
            return False
        return True


# noinspection PyUnusedLocal
class AudiobookMetaDataPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

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

        hs_track_year = wx.BoxSizer(wx.HORIZONTAL)
        vs_track_year_comment.Add(hs_track_year, 0, wx.ALL | wx.EXPAND, 0)

        lbl_disc = wx.StaticText(self, wx.ID_ANY, "Disc")
        hs_track_year.Add(lbl_disc, 0, 0, 0)

        hs_track_year.Add((60, 20), 0, 0, 0)

        self.sc_disc = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=100)
        self.sc_disc.SetToolTip("which disk?")
        hs_track_year.Add(self.sc_disc, 0, 0, 0)

        label_8 = wx.StaticText(self, wx.ID_ANY, "of")
        hs_track_year.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.sc_disk_total = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=100)
        self.sc_disk_total.SetToolTip("Total number of discs for this book")
        hs_track_year.Add(self.sc_disk_total, 0, 0, 0)

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
        self.Bind(wx.EVT_SPINCTRL, self.on_disc, self.sc_disc)
        self.Bind(wx.EVT_SPINCTRL, self.on_disc, self.sc_disk_total)
        self.Bind(wx.EVT_TEXT, self.on_year, self.tc_year)
        self.Bind(wx.EVT_TEXT, self.on_comment, self.tc_comment)

        ee.on("coverart.dnd", self.ee_on_conver_art)
        ee.on("track.cover_art", self.ee_on_conver_art)

        ee.on("audiobook.new", self.reset_metadata)

        ee.on("track.title", self.ee_on_title)
        ee.on("track.artist", self.ee_on_artist)
        ee.on("track.disc", self.ee_on_disc)
        ee.on("track.disc_total", self.ee_on_disc_total)
        ee.on("track.genre", self.ee_on_genre)
        ee.on("track.comment", self.ee_on_comment)
        ee.on("track.year", self.ee_on_year)
        ee.on("track.album", self.ee_on_title)
        # TODO remove me
        # ee.on("track.albumartist", self.on_title)
        # ee.on("track.bitrate", self.on_title)
        # ee.on("track.duration", self.on_duration)
        # ee.on("track.filesize", self.on_title)
        # ee.on("track.samplerate", self.on_title)
        # ee.on("track.track", self.on_title)
        # ee.on("track.track_total", self.on_title)

        self.genre_clean = True

    def reset_metadata(self, event):
        self.tc_title.Clear()
        self.tc_artist.Clear()
        self.tc_grouping.Clear()
        self.cb_genre.SetValue("Urban Fantasy")
        self.tc_chapter_text.SetValue("Chapter")
        self.cb_chapterisation.SetSelection(0)
        self.sc_disc.SetValue(1)
        self.sc_disk_total.SetValue(1)
        self.tc_year.Clear()
        self.tc_comment.SetValue(ivonet.TXT_COMMENT)
        self.genre_clean = True

    def ee_on_conver_art(self, image):
        # TODO dirty check. What if mp3 have different mp3's or a dnd has already happened?
        log(f"Setting cover art to: {image}")
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
        ee.emit("audiobook.title", event.GetString())
        event.Skip()

    def ee_on_title(self, value):
        if self.tc_title.IsEmpty():
            self.tc_title.SetValue(value)

    def on_artist(self, event):
        ee.emit("audiobook.artist", event.GetString())
        event.Skip()

    def ee_on_artist(self, value):
        if self.tc_artist.IsEmpty():
            self.tc_artist.SetValue(value)

    def on_grouping(self, event):
        ee.emit("audiobook.grouping", event.GetString())
        event.Skip()

    def ee_on_grouping(self, value):
        if self.tc_grouping.IsEmpty():
            self.tc_grouping.SetValue(value)

    def on_genre(self, event):
        ee.emit("audiobook.genre", event.GetString())
        event.Skip()

    def ee_on_genre(self, value):
        if self.genre_clean:
            if value in GENRES:
                self.genre_clean = False
                self.cb_genre.SetValue(value)
            else:
                log(f"Genre {value} from the metadata is not a known genre.")

    def on_chapter_text(self, event):
        ee.emit("audiobook.chapter_text", event)
        event.Skip()

    def on_chapter_method(self, event):
        log("Event handler 'on_chapter_method' not implemented!")
        event.Skip()

    def on_disc(self, event):
        self.check_disc()
        ee.emit("audiobook.disc", self.sc_disc.GetValue())
        ee.emit("audiobook.disc_total", self.sc_disk_total.GetValue())
        event.Skip()

    def ee_on_disc(self, value):
        self.sc_disc.SetValue(int(value))
        # self.check_disc()

    def ee_on_disc_total(self, value):
        self.sc_disk_total.SetValue(int(value))
        # self.check_disc()

    def on_year(self, event):
        log("Event handler 'on_year' not implemented!")
        event.Skip()

    def ee_on_year(self, value):
        if self.tc_year.IsEmpty():
            self.tc_year.SetValue(value)

    def on_comment(self, event):
        log("Event handler 'on_comment' not implemented!")
        event.Skip()

    def ee_on_comment(self, value):
        if self.tc_comment.IsEmpty() or self.tc_comment.GetValue() == ivonet.TXT_COMMENT:
            self.tc_comment.SetValue(value)

    def check_disc(self):
        if self.sc_disk_total.GetValue() < self.sc_disc.GetValue():
            log("Correcting disk total as it can not be smaller than the current disk.")
            self.sc_disk_total.SetValue(self.sc_disc.GetValue())
