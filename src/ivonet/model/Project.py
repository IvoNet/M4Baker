#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-02 21:18:42$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Represents the state of one project
The idea is that this project can be Pickled to a file and restored again to get the last state back of an
Audiobook configuration.
"""

import ivonet


class Project(object):
    def __init__(self) -> None:
        self.name = None
        self.tracks = []
        self.title = ""
        self.artist = ""
        self.grouping = ""
        self.genre = "Urban Fantasy"
        self.chapter_text = "Chapter"
        self.chapter_method = "Based on mp3 length"
        self.comment = ivonet.TXT_COMMENT
        self.disc = 1
        self.disc_total = 1
        self.year = ""
        self.cover_art = None

    def has_cover_art(self):
        return self.cover_art is not None

    def __repr__(self) -> str:
        return f"""Project [
    project_name={self.name},
    tracks={self.tracks},
    title={self.title}, 
    artist={self.artist}, 
    grouping={self.grouping},
    genre={self.genre},
    disk={self.disc}/{self.disc_total},
    year={self.year},
    chapter_text={self.chapter_text},
    chapter_method={self.chapter_method},
    comment={self.comment},
    cover_art={self.has_cover_art()}
    ]"""

    def verify(self) -> bool:
        if self.name and self.title and self.tracks and self.artist and self.chapter_method and self.has_cover_art():
            return True
        return False
