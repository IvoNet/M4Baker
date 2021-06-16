#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-06-16 22:33:08$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Represents the state of one project
The idea is that this project can be Pickled to a file and restored again to get the last state back of an
Audiobook configuration.
"""

from ivonet.io.ffprobe import duration, sexagesimal


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class StateMachine(object):

    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.artist = ""
        self.grouping = ""
        self.genre = "Urban Fantasy"
        self.chapter_method = "Based on mp3 length"


class Project(object):

    def __init__(self) -> None:
        self.name = None
        self.tracks = []
        self.title = ""
        self.artist = StateMachine.instance().artist
        self.grouping = StateMachine.instance().grouping
        self.genre = StateMachine.instance().genre
        self.chapter_text = "Chapter"
        self.chapter_method = StateMachine.instance().chapter_method
        self.comment = ""
        self.disc = 1
        self.disc_total = 1
        self.year = ""
        self.cover_art = None
        self.m4b_name = None

    def set_artist(self, value):
        self.artist = value
        StateMachine.instance().artist = value

    def set_grouping(self, value):
        self.grouping = value
        StateMachine.instance().grouping = value

    def set_chapter_method(self, value):
        self.chapter_method = value
        StateMachine.instance().chapter_method = value

    def set_genre(self, value):
        self.genre = value
        StateMachine.instance().genre = value

    def has_cover_art(self):
        return self.cover_art is not None

    def final_name(self, extension=".m4b"):
        part = ""
        if self.disc_total > 1:
            part = f".Part {self.disc}"
        if self.grouping:
            return f"{self.artist} - {self.grouping.replace('#', '')} - {self.title}{extension}{part}"
        return f"{self.artist} - {self.title}{part}"

    def chapter_file(self, chapter_start=1):
        ret = [f"00:00:00.000 {self.chapter_text} {chapter_start:03d}"]
        total_time = 0.0
        for idx, track in enumerate(self.tracks, start=chapter_start + 1):
            total_time += duration(track)
            ret.append(f"{sexagesimal(total_time)} {self.chapter_text} {idx:03d}")
        return "\n".join(ret)

    def verify(self) -> bool:
        if self.title and self.tracks and self.artist and self.has_cover_art():
            return True
        return False

    def get_comment(self):
        return self.comment.replace('"', "").replace("'", "").replace("  ", " ").replace("\t", " ")

    def refresh_after_pickle(self):
        """Should be called after a pickle load operation.
        This method is to guarantee backwards compatibility for m4baker files after a model change
        """
        try:
            self.m4b_name
        except AttributeError:
            self.m4b_name = None

        StateMachine.instance().artist = self.artist
        StateMachine.instance().genre = self.genre
        StateMachine.instance().grouping = self.grouping
        StateMachine.instance().chapter_method = self.chapter_method

    def __repr__(self) -> str:
        return f"""Project [
    project_name={self.name},
    m4b_name={self.m4b_name},
    title={self.title}, 
    artist={self.artist}, 
    grouping={self.grouping},
    genre={self.genre},
    disk={self.disc}/{self.disc_total},
    year={self.year},
    chapter_text={self.chapter_text},
    chapter_method={self.chapter_method},
    comment={self.comment},
    cover_art={self.has_cover_art()},
    tracks={self.tracks},
    ]"""
