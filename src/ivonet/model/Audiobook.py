#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 16:36:41$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

from io import BytesIO

import ivonet
from ivonet.events import log
from ivonet.model.Track import Track


class Audiobook(object):
    """Represents an audiobook"""

    def __init__(self) -> None:
        self.sorted = []
        self.tracks = {}
        self.title = None
        self.artist = None
        self.grouping = None
        self.genre = None
        self.chapter_text = "Chapter"
        self.chapter_method = None
        self.comment = ivonet.TXT_COMMENT
        self.disc = 1
        self.disc_total = 1
        self.cover_art = None
        self.year = None
        # ee.emit("audiobook.new")
        log("New Audiobook initialized")

    def add_all(self, filenames: list):
        for name in filenames:
            if name.lower().endswith(".mp3") and name not in self.sorted:
                track = Track(name)
                self.sorted.append(name)
                self.tracks[name] = track
                # ee.emit("audiobook.track", track)
            else:
                log(f"File {name} is not an mp3 file or already in the list.")

    def set_grouping(self, value):
        self.grouping = value
        # dbg(self)

    def set_title(self, value):
        self.title = value
        # dbg(self)

    def set_artist(self, value):
        self.artist = value
        # dbg(self)

    def set_disc(self, value):
        self.disc = value
        # dbg(self)

    def set_disc_total(self, value):
        self.disc_total = value
        # dbg(self)

    def set_comment(self, value):
        self.comment = value
        # dbg(self)

    def set_year(self, value):
        self.year = value
        # dbg(self)

    def set_cover_art(self, image):
        self.cover_art = image
        if type(image) == BytesIO:
            log("Cover art set from mp3")
        else:
            log(f"Cover art set from file {image}")

    def __repr__(self) -> str:
        return f"""Audiobook [
        title={self.title}, 
        artist={self.artist}, 
        grouping={self.grouping},
        genre={self.genre},
        disk={self.disc}/{self.disc_total},
        year={self.year},
        ]"""

    def verify(self) -> bool:
        ret = True
        if not self.title:
            log("Title is mandatory")
            ret = False
        if not self.artist:
            log("Artist is mandatory")
            ret = False
        if not self.genre:
            log("Genre is mandatory")
            ret = False

        return ret
