#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-10 21:00:01$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import _thread
import os
import re
import shutil
import subprocess
import tempfile
from io import BytesIO

import wx
import wx.lib.newevent

import ivonet
from ivonet.book.meta import CHAPTER_LIST
from ivonet.events import dbg, log
from ivonet.events.custom import ProcessDoneEvent, ProcessExceptionEvent
from ivonet.io import unique_name
from ivonet.model.Project import Project


def time_seconds(seq) -> int:
    """ Calculates the time in seconds based on hours, minutes, seconds.
    The milliseconds are ignored. That kind of accuracy is not needed
    :param seq: (hours, minutes, seconds, [milliseconds])
    :return: int of seconds
    """
    return int(seq[0]) * 3600 + int(seq[1]) * 60 + int(seq[2])


class ProjectConverterWorker(object):
    DURATION = re.compile(".*Duration: ([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{2}).*")
    TIME_ELAPSED = re.compile(".*size=.*time=([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{2}).*")

    def __init__(self, parent, project: Project) -> None:
        self.parent = parent
        self.project = project
        self.keep_going = False
        self.running = False
        self.pid = None
        self.total_duration = 0
        self.progress = 0
        self.process = None

    def calc_percentage_done(self, seq):
        return int(time_seconds(seq) * 100 / self.total_duration)

    def start(self):
        self.keep_going = self.running = True
        _thread.start_new_thread(self.run, ())

    def stop(self):
        self.keep_going = False

    def is_running(self) -> bool:
        return self.running

    def run(self):
        self.running = True

        with tempfile.TemporaryDirectory() as project_tmpdir:
            dbg("Temp dir:", project_tmpdir)
            log(f"Creating: {self.project.m4b_name}")

            # bind all mp3 into one file (mp3binder)
            self.parent.stage = 0
            merged = os.path.join(project_tmpdir, "merged.mp3")
            self.merge_mp3_files(merged)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Convert ffmpeg
            self.parent.stage = 1
            m4a = os.path.join(project_tmpdir, "converted.m4a")
            self.convert_2_m4a(merged, m4a)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Add metadata tags
            self.parent.stage = 2
            self.add_metadata(m4a)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Add chapters
            self.parent.stage = 3
            m4b = os.path.join(project_tmpdir, "converted.m4b")
            self.create_chapters(project_tmpdir, m4b)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Add CoverArt
            self.parent.stage = 4
            cover = os.path.join(project_tmpdir, "cover.png")
            self.add_cover_art(cover, m4b)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            self.parent.stage = 5
            self.parent.update(25)
            log(f"Moving completed audiobook [{self.project.title}] to final destination.")
            shutil.move(m4b, unique_name(self.project.m4b_name))
            self.parent.update(100)

            if self.keep_going:
                self.parent.update(100)
                wx.PostEvent(self.parent, ProcessDoneEvent())
            self.running = False
            self.keep_going = False
            log(f"Created: {self.project.m4b_name}")

    def merge_mp3_files(self, merged):

        if len(self.project.tracks) == 1:
            self.parent.update(25)
            shutil.copyfile(self.project.tracks[0], merged)
            self.parent.update(100)
            return

        cmd = [ivonet.APP_MP3_BINDER, '-out', merged]
        [cmd.append(mp3) for mp3 in self.project.tracks]

        self.subprocess(cmd)

        log(f"Merging mp3 files for: {self.project.title}")
        total = len(self.project.tracks)
        count = 0
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line
                continue
            dbg(line)
            if not line:
                dbg(f"Finished Merge for: {self.project.title}")
                break
            if "Processing:" in line:
                count += 1
                self.parent.update(int((count * 100) / total))
        self.__check_process(cmd)

    def convert_2_m4a(self, merged, m4a):
        cmd = [ivonet.APP_FFMPEG,
               '-i',
               merged,
               "-stats",
               "-threads", "4",
               "-vn",
               "-y",
               "-acodec", "aac",
               "-strict",
               "-2",
               "-map_metadata", "0",
               "-map_metadata:s:a", "0:s:a",
               "-ac", "1",
               m4a,
               ]
        self.subprocess(cmd)

        log(f"Conversion has started for: {self.project.title}")
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line
                continue
            if not line:
                dbg(f"Conversion finished for: {self.project.title}")
                break
            dbg(line)
            duration = self.DURATION.match(line)
            if duration:
                self.total_duration = time_seconds(duration.groups())
                continue
            elapsed = self.TIME_ELAPSED.match(line)
            if elapsed:
                self.progress = self.calc_percentage_done(elapsed.groups())
                self.parent.update(self.progress)
        self.__check_process(cmd)

    def add_metadata(self, m4a):
        """AtomicParsley "${AUDIOBOOK}.m4a" --title "${TITLE}"
        --grouping "${GROUPING}" --sortOrder album "${GROUPING}"
        --album "${ALBUM}" --artist "${AUTHOR}" --genre "${GENRE}"
        --tracknum "${TRACK}" --disk "${TRACK}" --comment "${COMMENT}"
        --year "${YEAR}" --stik Audiobook --overWrite"""
        cmd = [
            ivonet.APP_ATOMIC_PARSLEY,
            m4a,
            "--title", f"{self.project.title}",
            "--grouping", f"{self.project.grouping}",
            "--sortOrder", 'album', f"{self.project.grouping}",
            "--album", f"{self.project.title}",
            "--artist", f"{self.project.artist}",
            "--genre", f"{self.project.genre}",
            "--tracknum", f"{self.project.disc}/{self.project.disc_total}",
            "--disk", f"{self.project.disc}/{self.project.disc_total}",
            "--comment", f"""{self.project.get_comment()}""",
            "--year", f"{self.project.year}",
            "--encodingTool", f"{ivonet.TXT_APP_NAME} ({ivonet.TXT_APP_TINY_URL})",
            "--stik", "Audiobook",
            "--overWrite"
        ]
        self.subprocess(cmd)

        log(f"Adding metadata to: {self.project.title}")
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line
                continue
            if not line:
                dbg(f"Finished Adding metadata to {self.project.title}")
                break
            dbg(line)
            if "Progress:" in line:
                ret = line.split("%")
                if len(ret) > 1:
                    try:
                        percentage = int(ret[0].split()[-1])
                        self.parent.update(percentage)
                        dbg(percentage)
                    except (IndexError, ValueError):
                        # Just ignore... probably bad line
                        pass
        self.parent.update(100)
        self.__check_process(cmd)

    def create_chapters(self, project_tmpdir, m4b):
        cmd = [ivonet.APP_MP4_CHAPS, ]
        if self.project.chapter_method == CHAPTER_LIST[0]:
            chapter_file = os.path.join(project_tmpdir, "converted.chapters.txt")
            with open(chapter_file, "w") as fo:
                fo.write(self.project.chapter_file())
                self.parent.update(10)
            cmd.append("-i")
        else:
            fixed = int(self.project.chapter_method.split()[1].strip()) * 60
            cmd.append("-e")
            cmd.append(str(fixed))
        cmd.append(m4b)

        self.subprocess(cmd)

        log(f"Adding chapter information to: {self.project.title}")
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line should not effect the progress
                continue
            if not line:
                dbg(f"Chapter information done: {self.project.title}")
                break
            dbg(line)
            if "QuickTime" in line:
                self.parent.update(50)
        self.__check_process(cmd)
        self.parent.update(100)

    def add_cover_art(self, cover, m4b):
        """add_cover_art(cover_name, audiobook_file) -> audiobook file with cover art

        Saved the CoverArt from the project to disc and adds it to the audiobook.
        """
        img = wx.Image(BytesIO(self.project.cover_art), wx.BITMAP_TYPE_ANY)
        img.SaveFile(cover, wx.BITMAP_TYPE_PNG)
        self.parent.update(10)
        cmd = [ivonet.APP_MP4_ART, "--add", cover, m4b]

        self.subprocess(cmd)

        log(f"Adding Cover Art to: {self.project.title}")
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line.
                continue
            if not line:
                dbg(f"Finished Adding CoverArt to: {self.project.title}")
                break
            dbg(line)
            if "adding" in line:
                self.parent.update(50)
        self.__check_process(cmd)
        self.parent.update(100)

    def subprocess(self, cmd: list):
        """subprocess(command_list) -> perfors a system command.

        Runs a subprocess with the stderr piped to stdout.
        The input stream (stdin) is closed right after startup. The process does not need it.
        """
        if not self.keep_going:
            self.running = False
            return
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False,
            universal_newlines=True,
        )
        # Close stdin as it is not used
        self.process.stdin.close()

    def __check_process(self, cmd):
        if self.process and not self.keep_going:
            self.process.terminate()
        self.process.stdout.close()
        self.process.wait()
        if self.process.returncode != 0 and self.keep_going:
            # Only throw an exception if the process terminated wrong
            # but we wanted to keep going
            self.keep_going = False
            dbg("Process exitcode: ", self.process.returncode)
            wx.PostEvent(self.parent, ProcessExceptionEvent(cmd=cmd, project=self.project))
