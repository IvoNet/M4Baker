#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-10 20:59:56$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
The Main Application Window
"""

import ast
import os
import pickle
from configparser import ConfigParser
from io import BytesIO

import wx
import wx.adv
from tinytag import TinyTag
from wx.lib.wordwrap import wordwrap

import ivonet
from ivonet.book.meta import GENRES, CHAPTER_LIST
from ivonet.events import dbg, log
from ivonet.events.custom import EVT_PROJECT_HISTORY, ProjectHistoryEvent, EVT_PROCESS_CLEAN, ProcessCleanEvent, \
    EVT_PROCESS_CANCELLED, ProcessCancelledEvent
from ivonet.gui.AudiobookEntryPanel import AudiobookEntry
from ivonet.gui.CoverArtDropTarget import CoverArtDropTarget
from ivonet.gui.MP3DropTarget import MP3DropTarget
from ivonet.gui.MenuBar import MenuBar, FILE_MENU_QUEUE
from ivonet.image.IvoNetArtProvider import IvoNetArtProvider
from ivonet.io.save import save_project
from ivonet.model.Project import Project

try:
    from ivonet.image.images import yoda, pixel
except ImportError:
    raise ImportError("The images file was not found. Did you forget to generate them?")


def handle_numeric_keypress(event):
    keycode = event.GetKeyCode()
    if keycode < 255 and chr(keycode).isnumeric():
        event.Skip()


class MainFrame(wx.Frame):
    """The main application Frame holding all the other panels"""

    def __init__(self, *args, **kw):
        """Initialize the gui here"""
        super().__init__(*args, **kw)

        #  Startup Settings
        self.active_queue = []
        self.genre_pristine = True
        self.project = Project()
        self.default_save_path = ivonet.DEFAULT_SAVE_PATH
        wx.ArtProvider.Push(IvoNetArtProvider())

        self.SetSize((1500, 1200))
        self.SetMinSize((1024, 768))
        self.current_size = self.GetSize()
        self.is_resizing = False

        self.__make_toolbar()
        self.SetMenuBar(MenuBar(self))

        self.CreateStatusBar()
        self.SetStatusText(ivonet.TXT_COPYRIGHT)

        self.status_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_clear_status, self.status_timer)

        vs_main = wx.BoxSizer(wx.VERTICAL)

        self.main_panel = wx.Panel(self, wx.ID_ANY)
        vs_main.Add(self.main_panel, 3, wx.EXPAND, 0)

        vs_main_panel = wx.BoxSizer(wx.VERTICAL)

        hs_main_panel = wx.BoxSizer(wx.HORIZONTAL)
        vs_main_panel.Add(hs_main_panel, 4, wx.EXPAND, 0)

        self.m4b_panel = wx.Panel(self.main_panel, wx.ID_ANY)
        hs_main_panel.Add(self.m4b_panel, 1, wx.EXPAND, 0)

        vs_m4b_panel = wx.BoxSizer(wx.VERTICAL)

        hs_m4b_panel = wx.BoxSizer(wx.HORIZONTAL)
        vs_m4b_panel.Add(hs_m4b_panel, 1, wx.EXPAND, 0)

        self.metadata_panel = wx.Panel(self.m4b_panel, wx.ID_ANY, style=wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL)
        hs_m4b_panel.Add(self.metadata_panel, 2, wx.ALL | wx.EXPAND, 0)

        hs_metadata_panel = wx.BoxSizer(wx.HORIZONTAL)

        fgs_metadata_panel = wx.FlexGridSizer(3, 1, 4, 0)
        hs_metadata_panel.Add(fgs_metadata_panel, 1, wx.ALL | wx.EXPAND, 2)

        fgs_mp3_metadata = wx.FlexGridSizer(6, 2, 4, 11)
        fgs_metadata_panel.Add(fgs_mp3_metadata, 1, wx.ALL | wx.EXPAND, 0)

        # MP3 Tags
        lbl_title = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Title")
        fgs_mp3_metadata.Add(lbl_title, 1, 0, 0)

        self.tc_title = wx.TextCtrl(self.metadata_panel, wx.ID_ANY, "")
        self.tc_title.SetToolTip("Title of the book")
        fgs_mp3_metadata.Add(self.tc_title, 1, wx.EXPAND, 0)

        lbl_artist = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Artist")
        fgs_mp3_metadata.Add(lbl_artist, 0, wx.EXPAND, 0)

        self.tc_artist = wx.TextCtrl(self.metadata_panel, wx.ID_ANY, "")
        self.tc_artist.SetToolTip("The author or album artist")
        fgs_mp3_metadata.Add(self.tc_artist, 0, wx.EXPAND, 0)

        lbl_grouping = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Grouping")
        fgs_mp3_metadata.Add(lbl_grouping, 1, 0, 0)

        self.tc_grouping = wx.TextCtrl(self.metadata_panel, wx.ID_ANY, "")
        self.tc_grouping.SetToolTip("Grouping e.g. series")
        fgs_mp3_metadata.Add(self.tc_grouping, 0, wx.EXPAND, 0)

        lbl_genre = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Genre")
        fgs_mp3_metadata.Add(lbl_genre, 0, 0, 0)

        self.cb_genre = wx.ComboBox(self.metadata_panel, wx.ID_ANY,
                                    choices=GENRES,
                                    style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_genre.SetToolTip("Select your genre")
        self.cb_genre.SetSelection(0)
        fgs_mp3_metadata.Add(self.cb_genre, 0, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

        label_1 = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Chapter text")
        fgs_mp3_metadata.Add(label_1, 0, 0, 0)

        self.tc_chapter_text = wx.TextCtrl(self.metadata_panel, wx.ID_ANY, "Chapter")
        self.tc_chapter_text.SetToolTip("Text to use fore chapterisation")
        fgs_mp3_metadata.Add(self.tc_chapter_text, 0, wx.EXPAND, 0)

        lbl_chapterisation = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Chapters")
        fgs_mp3_metadata.Add(lbl_chapterisation, 1, 0, 0)

        self.cb_chapterisation = wx.ComboBox(self.metadata_panel, wx.ID_ANY,
                                             choices=CHAPTER_LIST,
                                             style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SIMPLE)
        self.cb_chapterisation.SetToolTip("Choose which chapterisation method is prefered")
        self.cb_chapterisation.SetSelection(0)
        fgs_mp3_metadata.Add(self.cb_chapterisation, 0, wx.EXPAND, 0)

        vs_track_year_comment = wx.BoxSizer(wx.VERTICAL)
        fgs_metadata_panel.Add(vs_track_year_comment, 1, wx.EXPAND, 0)

        hs_track_year = wx.BoxSizer(wx.HORIZONTAL)
        vs_track_year_comment.Add(hs_track_year, 0, wx.ALL | wx.EXPAND, 0)

        lbl_disc = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Disc")
        hs_track_year.Add(lbl_disc, 0, 0, 0)

        hs_track_year.Add((60, 20), 0, 0, 0)

        self.sc_disc = wx.SpinCtrl(self.metadata_panel, wx.ID_ANY, "1", min=1, max=100)
        self.sc_disc.SetToolTip("which disk?")
        hs_track_year.Add(self.sc_disc, 0, 0, 0)

        label_8 = wx.StaticText(self.metadata_panel, wx.ID_ANY, "of")
        hs_track_year.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.sc_disk_total = wx.SpinCtrl(self.metadata_panel, wx.ID_ANY, "1", min=1, max=100)
        self.sc_disk_total.SetToolTip("Total number of discs for this book")
        hs_track_year.Add(self.sc_disk_total, 0, 0, 0)

        hs_track_year.Add((32, 20), 0, 0, 0)

        lbl_year = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Year")
        hs_track_year.Add(lbl_year, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.tc_year = wx.TextCtrl(self.metadata_panel, wx.ID_ANY, "")
        self.tc_year.Bind(wx.EVT_CHAR, handle_numeric_keypress)
        self.tc_year.SetToolTip("Publication year")
        hs_track_year.Add(self.tc_year, 1, wx.EXPAND, 0)

        vs_comment = wx.BoxSizer(wx.VERTICAL)
        vs_track_year_comment.Add(vs_comment, 0, wx.EXPAND, 0)

        vs_comment_1 = wx.BoxSizer(wx.VERTICAL)
        vs_comment.Add(vs_comment_1, 2, wx.ALL | wx.EXPAND, 0)

        lbl_comment = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Comment")
        vs_comment_1.Add(lbl_comment, 0, wx.LEFT, 0)

        self.tc_comment = wx.TextCtrl(self.metadata_panel, wx.ID_ANY, "",
                                      style=wx.TE_MULTILINE)
        self.tc_comment.SetToolTip("Add your comments here.")
        vs_comment_1.Add(self.tc_comment, 2, wx.EXPAND, 0)

        cover_art_wrapper_sizer_v = wx.BoxSizer(wx.VERTICAL)
        fgs_metadata_panel.Add(cover_art_wrapper_sizer_v, 1, wx.ALL | wx.EXPAND, 0)

        # Cover Art section
        lbl_cover_art = wx.StaticText(self.metadata_panel, wx.ID_ANY, "Cover art")
        cover_art_wrapper_sizer_v.Add(lbl_cover_art, 0, 0, 0)

        self.cover_art_panel = wx.Panel(self.metadata_panel, wx.ID_ANY)
        self.cover_art_panel.SetToolTip("Drag and drop Cover Art here")
        cover_art_wrapper_sizer_v.Add(self.cover_art_panel, 1, wx.EXPAND, 1)

        cover_art_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.cover_art = wx.StaticBitmap(self.cover_art_panel)
        self.cover_art.SetBitmap(yoda.GetBitmap())
        self.SetToolTip("Drag and drop Cover Art here. Double click to reset.")
        self.cover_art.SetDropTarget(CoverArtDropTarget(self))
        self.cover_art.Bind(wx.EVT_LEFT_DCLICK, self.on_reset_cover_art)
        cover_art_sizer_h.Add(self.cover_art, 1, wx.EXPAND, 0)

        # MP3 Drag n Drop section
        self.lc_mp3 = wx.adv.EditableListBox(self, wx.ID_ANY, "Drag and Drop mp3 files below...",
                                             style=wx.adv.EL_ALLOW_DELETE)
        self.lc_mp3.SetToolTip("Drag and Drop MP3 files here")
        self.lc_mp3.SetDropTarget(MP3DropTarget(self))
        self.lc_mp3.SetToolTip("Drag and Drop MP3 files here")
        self.lc_mp3.del_button = self.lc_mp3.GetDelButton()
        self.lc_mp3.GetListCtrl().Bind(wx.EVT_LEFT_DCLICK, self.on_tracks_empty)
        self.lc_mp3.GetListCtrl().Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_selected_right_click)

        hs_m4b_panel.Add(self.lc_mp3, 5, wx.ALL | wx.EXPAND, 0)

        self.log_panel = wx.Panel(self.main_panel, wx.ID_ANY)
        vs_main_panel.Add(self.log_panel, 1, wx.EXPAND, 0)

        log_sizer_v = wx.BoxSizer(wx.VERTICAL)

        log_sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        log_sizer_v.Add(log_sizer_h, 1, wx.EXPAND, 0)

        self.tc_log = wx.TextCtrl(self.log_panel, wx.ID_ANY, "",
                                  style=wx.TE_MULTILINE | wx.TE_LEFT | wx.TE_READONLY | wx.HSCROLL)
        self.tc_log.SetFont(
            wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Courier New"))
        wx.Log.SetActiveTarget(wx.LogTextCtrl(self.tc_log))
        log_sizer_h.Add(self.tc_log, 1, wx.EXPAND, 0)

        # Queue Part
        self.queue_window = wx.ScrolledWindow(self.main_panel, wx.ID_ANY,
                                              style=wx.BORDER_RAISED | wx.TAB_TRAVERSAL | wx.HT_WINDOW_VERT_SCROLLBAR)
        self.queue_window.SetScrollRate(10, 10)
        vs_main_panel.Add(self.queue_window, 1, wx.EXPAND, 0)

        self.queue_sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.queue_window.SetSizer(self.queue_sizer_v)

        self.log_panel.SetSizer(log_sizer_v)

        self.cover_art_panel.SetSizer(cover_art_sizer_h)

        fgs_mp3_metadata.AddGrowableCol(1)

        fgs_metadata_panel.AddGrowableRow(2)
        fgs_metadata_panel.AddGrowableCol(0)

        self.metadata_panel.SetSizer(hs_metadata_panel)

        self.m4b_panel.SetSizer(vs_m4b_panel)

        self.main_panel.SetSizer(vs_main_panel)

        self.SetSizer(vs_main)
        vs_main.SetSizeHints(self)

        self.load_settings()
        self.Layout()

        self.update_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update_ui)
        self.update_timer.Start(750)

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
        self.Bind(wx.EVT_TEXT_MAXLEN, self.on_log_empty, self.tc_log)
        self.tc_log.Bind(wx.EVT_LEFT_DCLICK, self.on_log_empty)

        self.Bind(wx.EVT_SIZING, self.on_resizing)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(EVT_PROJECT_HISTORY, self.on_project_history)
        self.Bind(EVT_PROCESS_CLEAN, self.on_clean_queue_item)
        self.Bind(EVT_PROCESS_CANCELLED, self.on_process_cancelled)

        self.init()

    def init(self):
        # Remove old log file if still exists
        if os.path.isfile(ivonet.LOG_FILE):
            os.remove(ivonet.LOG_FILE)

        # Tell the world we started anew
        self.reset_metadata(self.project)

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

    def on_update_ui(self, event):
        """Handles the wx.UpdateUIEvent."""
        self.project.tracks = self.lc_mp3.GetStrings()
        enable_disable = self.project.verify()
        self.GetToolBar().EnableTool(ivonet.TOOLBAR_ID_QUEUE, enable_disable)
        self.GetMenuBar().Enable(FILE_MENU_QUEUE, enable_disable)
        self.queue_window.Refresh()
        self.main_panel.Layout()
        self.Refresh()
        event.Skip()

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        if self.active_queue:
            with wx.MessageDialog(self, 'Conversions happening...',
                                  'Are you sure you want to exit?',
                                  wx.ICON_EXCLAMATION | wx.YES_NO) as dlg:
                if dlg.ShowModal() == wx.ID_NO:
                    return

        self.save_settings()
        self.Close(True)
        event.Skip()

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
        event.Skip()

    def on_queue(self, event):
        """Handles the queue event from either the toolbar or the File menu (shortcut)."""
        if not self.project.verify():
            dbg("You slipped between verifies :-) no no no processing allowed.")
            return
        self.status("Queueing audiobook...")

        base_dir = None
        if self.project.name:
            base_dir, filename = os.path.split(self.project.name)
        elif self.project.tracks:
            base_dir = os.path.split(self.project.tracks[0])[0]

        with wx.FileDialog(self, "Save audiobook...",
                           defaultDir=self.default_save_path,
                           defaultFile=self.project.final_name(),
                           wildcard=ivonet.FILE_WILDCARD_M4B,
                           style=wx.FD_SAVE) as fileDialog:

            if base_dir:
                fileDialog.SetDirectory(base_dir)

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            if not pathname.endswith(".m4b"):
                pathname += ".m4b"
            self.project.m4b_name = pathname

        self.queue_project(self.project)
        self.on_clear(event)
        event.Skip()

    def queue_project(self, project: Project):
        """Queue a project.
        Wraps a project into an AudiobookEntry and puts it on the queue and start it.
        AudiobookEntry will take care of the rest.
        """
        book = AudiobookEntry(self, project)
        self.queue_sizer_v.Prepend(book, 0, wx.ALL | wx.EXPAND, 0)
        self.active_queue.append(book)
        self.queue_window.Layout()
        self.Refresh()
        book.start()

    def on_clean_queue_item(self, event: ProcessCleanEvent):
        """Handles the cleaning of a queued item after it has been stopped and the button is pressed again."""
        event.obj.Destroy()
        self.remove_from_active_queue(event.obj)
        event.Skip()

    def on_process_cancelled(self, event: ProcessCancelledEvent):
        """Remove the process from the active queue when it is cancelled"""
        self.remove_from_active_queue(event.obj)

    def remove_from_active_queue(self, book):
        try:
            self.active_queue.remove(book)
        except ValueError as e:
            dbg(e)

    def on_select_dir(self, event):
        """Handles the default dir event
        Deprecated because I don't think I will really use it.
        """
        self.status("Select directory")
        with wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                                | wx.DD_DIR_MUST_EXIST
                                | wx.DD_CHANGE_DIR
                          ) as dir_dialog:
            if dir_dialog.ShowModal() == wx.ID_OK:
                self.default_save_path = dir_dialog.GetPath()
        event.Skip()

    def on_open_project(self, event):
        """Handles the open project event."""
        self.status("Open Project")
        with wx.FileDialog(self,
                           message="Choose a file...",
                           defaultDir=os.getcwd(),
                           defaultFile="",
                           wildcard=ivonet.FILE_WILDCARD_PROJECT,
                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
                           ) as open_dlg:
            if open_dlg.ShowModal() == wx.ID_OK:
                path = open_dlg.GetPath()
                log(f"Opening file: {path}")
                self.project_open(path)
                wx.PostEvent(self, ProjectHistoryEvent(path=path))
        event.Skip()

    def project_open(self, path):
        """Open a saved project"""
        try:
            with open(path, 'rb') as fi:
                self.project = pickle.load(fi)
                self.project.name = path
                self.reset_metadata(self.project)
        except FileNotFoundError:
            log(f"File: {path} could not be opened.")

    def reset_metadata(self, project):
        """Resets all the metadata fields to te provided project."""
        self.project = project
        self.genre_pristine = True
        if project.has_cover_art():
            self.set_cover_art(self.project.cover_art)
        else:
            self.reset_cover_art()
        self.tc_title.SetValue(project.title)
        self.tc_title.Refresh()
        self.tc_artist.SetValue(project.artist)
        self.tc_grouping.SetValue(project.grouping)
        self.cb_genre.SetValue(project.genre)
        self.tc_chapter_text.SetValue(project.chapter_text)
        self.cb_chapterisation.SetValue(project.chapter_method)
        self.sc_disc.SetValue(project.disc)
        self.sc_disk_total.SetValue(project.disc_total)
        self.tc_year.SetValue(project.year)
        self.tc_comment.SetValue(project.comment)
        self.lc_mp3.SetStrings(project.tracks)

    def on_save_project(self, event):
        """Handles the save project event."""
        self.status("Save Project")
        save_project(self, self.project)
        event.Skip()

    def on_clear(self, event):
        """Handles the new project event."""
        self.status("Starting new project")
        self.project = Project()
        self.reset_metadata(self.project)
        event.Skip()

    def status(self, msg):
        """Sets the statusbar text and triggers the reset timer"""
        self.SetStatusText(msg)
        if not self.status_timer.IsRunning():
            self.status_timer.Start(2000)

    def on_clear_status(self, event):
        """Handles the status bar timer event when triggered and resets it to the default message."""
        self.SetStatusText(ivonet.TXT_COPYRIGHT)
        if self.status_timer.IsRunning():
            self.status_timer.Stop()
        event.Skip()

    def on_tracks_empty(self, event):
        """Handles the double click event on the tracks panel and will empty the list"""
        dbg("on_tracks_empty")
        self.lc_mp3.SetStrings([])
        event.Skip()

    def on_selected_right_click(self, event):
        selected = event.GetItem().GetText()
        if selected:
            tag = TinyTag.get(selected, image=True, ignore_errors=True)
            if tag.get_image():
                self.set_cover_art(tag.get_image())
        event.Skip()

    def append_track(self, line):
        """Add a line to the list."""
        lines = list(self.lc_mp3.GetStrings())
        lines.append(line)
        self.lc_mp3.SetStrings(lines)

    def set_cover_art(self, image):
        """handles the 'cover_art.force' and 'track.cover_art' events.
        gets an image file object or file location as input.
        """
        self.project.cover_art = image
        try:
            img = wx.Image(BytesIO(image), wx.BITMAP_TYPE_ANY)
            width = img.GetWidth()
            height = img.GetHeight()
        except AssertionError as e:
            dbg(e)
            log("CoverArt found but unknown format")
            return
        pnl_width, pnl_height = self.cover_art_panel.GetSize()
        if width > height:
            new_width = pnl_width
            new_height = pnl_width * height / width
        else:
            new_height = pnl_height
            new_width = pnl_height * width / height
        self.cover_art.SetBitmap(wx.Bitmap(img.Scale(new_width, new_height)))
        self.cover_art.Center()
        self.cover_art.Refresh()

    def on_reset_cover_art(self, event):
        """Reset cover art event handler"""
        self.reset_cover_art()
        event.Skip()

    def reset_cover_art(self):
        """Resets the cover art on double clicking the image"""
        self.project.cover_art = None
        self.cover_art.SetBitmap(yoda.GetBitmap())
        self.cover_art.Center()
        self.Refresh()

    # noinspection PyUnusedLocal
    def on_resizing(self, event):
        """Catch resizing events to enable proportional presentations of the cover.
        On resizing the cover art image will be replaced with a "pixel image"
        a very small image with no background so the panel will resize to smaller sizes
        without trouble.
        Resizing to a larger size was no trouble but going back to a smaller size was.
        The image claimed the larger panel and therefore did not resize back to a smaller size.
        This hack is the solution I came up with :-)
        """
        if self.project.has_cover_art() and not self.is_resizing:
            self.cover_art.SetBitmap(pixel.GetBitmap())
            self.cover_art.Center()
        self.is_resizing = True
        event.Skip()

    def on_idle(self, event):
        """The first idle event after a resizing event must be caught to resize the cover art
        to its best fit.
        It is a bit of a hack to enable the containing panel to resize back to a smaller size.
        """
        if self.is_resizing and self.project.has_cover_art():
            self.set_cover_art(self.project.cover_art)
        self.is_resizing = False
        event.Skip()

    def save_settings(self):
        """save_settings() -> Saves default settings to the application settings location"""
        ini = ConfigParser()
        ini.add_section("Settings")
        ini.set('Settings', 'screen_size', str(self.GetSize()))
        ini.set('Settings', 'screen_pos', str(self.GetPosition()))
        ini.set('Settings', 'default_save_path', self.default_save_path)
        with open(ivonet.SETTINGS_FILE, "w") as fp:
            ini.write(fp)

    def load_settings(self):
        """Load_ settings() -> Loads and activates the settings saved by save_settings()"""
        if os.path.isfile(ivonet.SETTINGS_FILE):
            ini = ConfigParser()
            ini.read(ivonet.SETTINGS_FILE)
            display_width, display_height = wx.DisplaySize()
            view_size = ast.literal_eval(ini.get('Settings', 'screen_size'))
            view_x, view_h = view_size
            if view_x > display_width or view_h > display_height:
                self.SetSize(self.GetBestSize())
            else:
                self.SetSize(view_size)
            position = ast.literal_eval(ini.get('Settings', 'screen_pos'))
            pos_w, pos_h = position
            if pos_w > display_width or pos_h > display_height:
                self.Center()
            else:
                self.SetPosition(position)
            self.default_save_path = ini.get('Settings', 'default_save_path', fallback=ivonet.DEFAULT_SAVE_PATH)
        else:
            self.Center()
        self.load_history_file()

    def load_history_file(self):
        """Loads last file history settings from disk"""
        if os.path.isfile(ivonet.HISTORY_FILE):
            history_config = wx.FileConfig(localFilename=ivonet.HISTORY_FILE,
                                           style=wx.CONFIG_USE_LOCAL_FILE)
            self.GetMenuBar().file_history.Load(history_config)

    def on_file_history(self, event):
        """Handler for the event on file history selection in the file menu"""
        file_num = event.GetId() - wx.ID_FILE1
        path = self.GetMenuBar().file_history.GetHistoryFile(file_num)
        log(f"You selected {path}")
        wx.PostEvent(self, ProjectHistoryEvent(path=path))
        self.project_open(path)

    def save_history(self):
        """Saves the recent file history to disk"""
        history_config = wx.FileConfig()
        self.GetMenuBar().file_history.Save(history_config)
        with open(ivonet.HISTORY_FILE, "wb") as fo:
            history_config.Save(fo)

    def on_project_history(self, event: ProjectHistoryEvent):
        """handler for the 'EVT_PROJECT_HISTORY' event.
        it will add it to the history (again) for the ranking and then save
        to settings so it can be reloaded on restart.
        """
        self.GetMenuBar().file_history.AddFileToHistory(event.path)
        self.save_history()

    def on_title(self, event):
        """Handler for the title field event"""
        self.project.title = event.GetString()
        event.Skip()

    def on_artist(self, event):
        """Handler for the artist field event"""
        self.project.artist = event.GetString()
        event.Skip()

    def on_grouping(self, event):
        """Handler for the grouping field event"""
        self.project.grouping = event.GetString()
        event.Skip()

    def on_genre(self, event):
        """Handler for the genre field event"""
        self.project.genre = event.GetString()
        event.Skip()

    def on_chapter_text(self, event):
        """Handler for the chapter text field event"""
        self.project.chapter_text = event.GetString()
        event.Skip()

    def on_chapter_method(self, event):
        """Handler for the chapter convert method field event"""
        self.project.chapter_method = event.GetString()
        event.Skip()

    def on_disc(self, event):
        """Handler for the disc and disc_total field events as they are linked"""
        if not self.check_disc():
            log("Corrected disk total as it can not be smaller than the disk.")
        self.project.disc = self.sc_disc.GetValue()
        self.project.disc_total = self.sc_disk_total.GetValue()
        event.Skip()

    def on_year(self, event):
        """Handler for the year field event"""
        self.project.year = event.GetString()
        event.Skip()

    def on_comment(self, event):
        """Handler for the comment field event"""
        self.project.comment = event.GetString()
        event.Skip()

    def on_log_empty(self, event):
        """Happends on double click and max_len"""
        self.tc_log.SetValue("")
        event.Skip()

    def check_disc(self) -> bool:
        if self.sc_disk_total.GetValue() < self.sc_disc.GetValue():
            self.sc_disk_total.SetValue(self.sc_disc.GetValue())
            return False
        return True
