#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import os
import os.path

from tinytag import TinyTag, TinyTagException

from ivonet.events import _, ee


class TrackException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Track(object):

    def __init__(self, filename) -> None:
        self.mp3 = filename
        try:
            self.tag = TinyTag.get(self.mp3, image=True)
            self.cover_art = self.tag.get_image()
        except TinyTagException as e:
            ee.emit("log", f"Could not retrieve metadata from: {os.path.splitext(filename)[1]}")
            return

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
            ee.emit("track.year", self.tag.year)
        if self.tag.get_image():
            ee.emit("track.cover_art", self.tag.get_image())

    def get(self, key) -> any:
        return self.tag.as_dict().get(key)

    def __repr__(self) -> str:
        return str(self.tag.as_dict())


@ee.on("track.*")
def event(evt):
    print(str(evt))


class Audiobook(object):
    def __init__(self) -> None:
        self.tracks = []
        self.title = None
        self.artist = None
        self.grouping = None
        self.genre = None
        self.chapter_text = "Chapter"
        self.disk = 1
        self.disk_total = 1

    def mp3(self, filenames):
        if not filenames or not type(filenames) is list:
            _(f"Something went wrong while setting the mp3s [{filenames}]")
        # check of all are mp3
        for track in filenames:
            extension = os.path.splitext(track)[1]
            if extension != ".mp3":
                ee.emit("log", f"File {track} is not an mp3 file")


if __name__ == '__main__':
    import pprint

    track = Track("/Users/iwo16283/dev/ivonet-audiobook/test/test.mp3")
    pprint.pprint(track)
    print("Duration:", track.get("duration"))
