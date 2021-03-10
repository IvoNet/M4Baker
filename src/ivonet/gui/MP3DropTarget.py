#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/03/2021 19:57$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx
from tinytag import TinyTag

import ivonet
from ivonet.book.meta import GENRES
from ivonet.events import log, dbg

# Method and their mapping
methods = [
    ("album", "title"),
    ("artist", "artist"),
    ("comment", "comment"),
    ("disc", "disc"),
    ("disc_total", "disc_total"),
    ("track", "disc"),
    ("track_total", "disc_total"),
    ("genre", "genre"),
    ("title", "title"),
    ("year", "year"),
]


class MP3DropTarget(wx.FileDropTarget):
    """Handler for the Drag and Drop events of MP3 files"""

    def __init__(self, target):
        super().__init__()
        self.target = target
        self.genre_logged = False
        self.disc_correction_logged = False

    def OnDropFiles(self, x, y, filenames):
        dbg("MP3 Files dropped", filenames)

        for name in filenames:
            if name.lower().endswith(ivonet.FILE_EXTENSION):
                log("Recognized project file. Opening...")
                self.target.project_open(name)
                return True
            if name.lower().endswith(".mp3") and name not in self.target.lc_mp3.GetStrings():
                self.target.append_track(name)
                tag = TinyTag.get(name, image=True, ignore_errors=True)
                if tag.get_image():
                    self.target.set_cover_art(tag.get_image())
                for item, mapping in methods:
                    dbg("method: ", item)
                    value = getattr(tag, item)
                    if value:
                        dbg("Value:", value)
                        getattr(self, f"set_{mapping}")(value.strip())
            else:
                log(f"Dropped file '{name}' is not an mp3 file or not unique in the list.")
                return False
        self.genre_logged = False
        self.disc_correction_logged = False
        return True

    def set_title(self, value):
        """Sets the title.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.target.tc_title.IsEmpty():
            self.target.tc_title.SetValue(value)

    def set_artist(self, value):
        """Sets the artist
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.target.tc_artist.IsEmpty():
            self.target.tc_artist.SetValue(value)

    def set_grouping(self, value):
        """Sets the grouping.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.target.tc_grouping.IsEmpty():
            self.target.tc_grouping.SetValue(value)

    def set_genre(self, value):
        """Sets the genre.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        In this case we need a 'dirty' flag to do this as the field is a drop down and is never empty
        This event is less important then manual or previous set values.
        """
        if self.target.genre_pristine:
            if value in GENRES:
                self.target.genre_pristine = False
                self.target.cb_genre.SetValue(value)
            else:
                if not self.genre_logged:
                    log(f"Genre {value} from the metadata is not a known genre.")
                    self.genre_logged = True

    def set_disc(self, value):
        """Sets the disc.
        It will always set it and that will trigger the on_disc handler
        to check if all is well...
        """
        self.target.sc_disc.SetValue(int(value))
        if not self.target.check_disc():
            log("Corrected disk total as it can not be smaller than the disk.")

    def set_disc_total(self, value):
        """Sets the disc total.
        It will always set it and that will trigger the on_disc handler
        to check if all is well...
        """
        self.target.sc_disk_total.SetValue(int(value))
        if not self.target.check_disc():
            log("Corrected disk total as it can not be smaller than the disk.")

    def set_year(self, value):
        """Sets the year.
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.target.tc_year.IsEmpty():
            self.target.tc_year.SetValue(value)

    def set_comment(self, value):
        """Sets the comment
        It assumes that if the field has already been set either by a previous event
        or manually this event can be ignored.
        This event is less important then manual or previous set values.
        """
        if self.target.tc_comment.IsEmpty():
            self.target.tc_comment.SetValue(value)

    def set_cover_art_from_mp3(self, image):
        if not self.target.project.has_cover_art():
            self.target.set_cover_art(image)
