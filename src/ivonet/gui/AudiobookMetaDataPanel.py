#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx

from ivonet.book.genre import GENRES


class AudiobookMetaDataPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

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
                                             choices=["Based on mp3 length", "Fixed 3 minutes", "Fixed 10 minutes",
                                                      "Fixed 30 minutes", "Fixed 60 minutes"],
                                             style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SIMPLE)
        self.cb_chapterisation.SetToolTip("Choose which chapterisation method is prefered")
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

        self.tc_comment = wx.TextCtrl(self, wx.ID_ANY, "Converted with M4Baker (c) IvonNet.nl", style=wx.TE_MULTILINE)
        self.tc_comment.SetToolTip("Add your comments here")
        vs_comment_1.Add(self.tc_comment, 2, wx.EXPAND, 0)

        vs_mp3_metadata_2 = wx.BoxSizer(wx.VERTICAL)
        fgs_lft_pnl_m4b_page.Add(vs_mp3_metadata_2, 1, wx.EXPAND, 0)

        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        vs_mp3_metadata_2.Add(sizer_17, 1, wx.ALL | wx.EXPAND, 0)

        label_11 = wx.StaticText(self, wx.ID_ANY, "Cover art")
        sizer_17.Add(label_11, 0, 0, 0)

        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.panel_2.SetToolTip("Drag and drop Cover Art here")
        sizer_17.Add(self.panel_2, 1, wx.ALL | wx.EXPAND, 0)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        bitmap_1 = wx.StaticBitmap(self.panel_2, wx.ID_ANY,
                                   wx.Bitmap("/Users/iwo16283/dev/ivonet-audiobook/images/yoda.png",
                                             wx.BITMAP_TYPE_ANY))
        sizer_1.Add(bitmap_1, 1, wx.EXPAND, 0)

        self.panel_2.SetSizer(sizer_1)

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

    def on_title(self, event):
        print("Event handler 'on_title' not implemented!")
        event.Skip()

    def on_artist(self, event):
        print("Event handler 'on_artist' not implemented!")
        event.Skip()

    def on_grouping(self, event):
        print("Event handler 'on_grouping' not implemented!")
        event.Skip()

    def on_genre(self, event):
        print("Event handler 'on_genre' not implemented!")
        event.Skip()

    def on_chapter_text(self, event):
        print("Event handler 'on_chapter_text' not implemented!")
        event.Skip()

    def on_chapter_method(self, event):
        print("Event handler 'on_chapter_method' not implemented!")
        event.Skip()

    def on_track(self, event):
        print("Event handler 'on_track' not implemented!")
        event.Skip()

    def on_track_total(self, event):
        print("Event handler 'on_track_total' not implemented!")
        event.Skip()

    def on_year(self, event):
        print("Event handler 'on_year' not implemented!")
        event.Skip()

    def on_comment(self, event):
        print("Event handler 'on_comment' not implemented!")
        event.Skip()

# end of class AudiobookMetaDataPanel
