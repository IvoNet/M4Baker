#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import os
from io import BytesIO

from tinytag import TinyTag, TinyTagException

from ivonet.events import _, ee, log


class Track(object):
    """Represents an Audiobook track or 1 MP3 file."""

    def __init__(self, filename, silent=False) -> None:
        """Track constructor

        :param filename: The mp3 file
        :param silent: if True then don't emit events just create the track. Default is False
        """
        self.mp3 = filename
        try:
            self.tag = TinyTag.get(self.mp3, image=True)
            self.cover_art = self.tag.get_image()
        except TinyTagException as e:
            log(f"Could not retrieve metadata from: {os.path.splitext(filename)[1]}")
            _(e)
            return
        if not silent:
            ee.emit("track.mp3", self.mp3)
            if self.tag.album:
                ee.emit("track.album", self.tag.album)
            if self.tag.albumartist:
                ee.emit("track.albumartist", self.tag.albumartist)
            if self.tag.artist:
                ee.emit("track.artist", self.tag.artist)
            if self.tag.bitrate:
                ee.emit("track.bitrate", self.tag.bitrate)
            if self.tag.comment:
                ee.emit("track.comment", self.tag.comment)
            if self.tag.disc:
                ee.emit("track.disc", self.tag.disc)
            if self.tag.disc_total:
                ee.emit("track.disc_total", self.tag.disc_total)
            if self.tag.duration:
                ee.emit("track.duration", self.tag.duration)
            if self.tag.filesize:
                ee.emit("track.filesize", self.tag.filesize)
            if self.tag.genre:
                ee.emit("track.genre", self.tag.genre)
            if self.tag.samplerate:
                ee.emit("track.samplerate", self.tag.samplerate)
            if self.tag.title:
                ee.emit("track.title", self.tag.title)
            if self.tag.track:
                ee.emit("track.track", self.tag.track)
            if self.tag.track_total:
                ee.emit("track.track_total", self.tag.track_total)
            if self.tag.year:
                if self.tag.year.isnumeric():
                    ee.emit("track.year", self.tag.year)
                else:
                    log(f"Ignoring year tag [{self.tag.year}] as it is not numeric.")
            if self.tag.get_image():
                ee.emit("track.cover_art", self.get_cover_art())

    def get(self, key) -> any:
        return self.tag.as_dict().get(key)

    def get_cover_art(self):
        if self.tag.get_image():
            return BytesIO(self.tag.get_image())
        return None

    def get_ctrl(self) -> tuple:
        return self.mp3, self.tag.duration

    def __repr__(self) -> str:
        return str(self.tag.as_dict())
