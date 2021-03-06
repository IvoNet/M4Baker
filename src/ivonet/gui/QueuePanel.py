#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-04 22:53:09$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Yup the Queue Panel. 
"""

import _thread
import os
import re
import shutil
import subprocess
import tempfile
import time
from io import BytesIO

import wx
import wx.lib.newevent

import ivonet
from ivonet.book.meta import CHAPTER_LIST
from ivonet.events import ee, dbg, log
from ivonet.io import unique_name
from ivonet.model.Project import Project

(ProcessDoneEvent, EVT_PROCESS_DONE) = wx.lib.newevent.NewEvent()


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
        self.target = parent
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
            log("Temp dir:", project_tmpdir)

            # bind all mp3 into one file (mp3binder)
            self.target.stage = 0
            merged = os.path.join(project_tmpdir, "merged.mp3")
            self.merge_mp3_files(merged)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Convert ffmpeg
            self.target.stage = 1
            m4a = os.path.join(project_tmpdir, "converted.m4a")
            self.convert_2_m4a(merged, m4a)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Add metadata tags
            self.target.stage = 2
            self.add_metadata(m4a)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Add chapters
            self.target.stage = 3
            m4b = os.path.join(project_tmpdir, "converted.m4b")
            self.create_chapters(project_tmpdir, m4b)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # Add CoverArt
            self.target.stage = 4
            cover = os.path.join(project_tmpdir, "cover.png")
            self.add_cover_art(cover, m4b)

            self.process = None
            if not self.keep_going:
                self.running = False
                return

            # TODO Check and select target folder
            self.target.stage = 5
            shutil.move(m4b, unique_name(os.path.join(os.environ["HOME"],
                                                      "Music/" + self.project.final_name())))
            self.target.update(50)
            shutil.move(cover, unique_name(os.path.join(os.environ["HOME"],
                                                        "Music/" + self.project.final_name(".png"))))
            self.target.update(100)

            if self.keep_going:
                self.target.update(100)
                wx.PostEvent(self.target, ProcessDoneEvent())
            self.running = False
            self.keep_going = False

    def merge_mp3_files(self, merged):
        cmd = [f'{ivonet.RESOURCE}/mp3binder',
               '-out',
               merged
               ]
        [cmd.append(mp3) for mp3 in self.project.tracks]

        self.__subprocess(cmd)

        log(f"Merging mp3 files for: {self.project.title}")
        total = len(self.project.tracks)
        count = 0
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line
                continue
            if not line:
                dbg(f"Finished Merge for: {self.project.title}")
                break
            if "Processing:" in line:
                count += 1
                self.target.update(int((count * 100) / total))
        self.__check_process(cmd)

    def convert_2_m4a(self, merged, m4a):
        cmd = [f'{ivonet.RESOURCE}/ffmpeg',
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
        self.__subprocess(cmd)

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
            duration = self.DURATION.match(line)
            if duration:
                self.total_duration = time_seconds(duration.groups())
                continue
            elapsed = self.TIME_ELAPSED.match(line)
            if elapsed:
                self.progress = self.calc_percentage_done(elapsed.groups())
                self.target.update(self.progress)
        self.__check_process(cmd)

    def add_metadata(self, m4a):
        """AtomicParsley "${AUDIOBOOK}.m4a" --title "${TITLE}"
        --grouping "${GROUPING}" --sortOrder album "${GROUPING}"
        --album "${ALBUM}" --artist "${AUTHOR}" --genre "${GENRE}"
        --tracknum "${TRACK}" --disk "${TRACK}" --comment "${COMMENT}"
        --year "${YEAR}" --stik Audiobook --overWrite"""
        cmd = [
            f"{ivonet.RESOURCE}/AtomicParsley",
            m4a,
            "--title",
            f"{self.project.title}",
            "--grouping",
            f"{self.project.grouping}",
            "--sortOrder", 'album',
            f"{self.project.grouping}",
            "--album",
            f"{self.project.title}",
            "--artist",
            f"{self.project.artist}",
            "--genre",
            f"{self.project.genre}",
            "--tracknum",
            f"{self.project.disc}/{self.project.disc_total}",
            "--disk",
            f"{self.project.disc}/{self.project.disc_total}",
            "--comment",
            f"{self.project.get_comment()}",
            "--year", f"{self.project.year}",
            "--stik", "Audiobook",
            "--overWrite"
        ]
        self.__subprocess(cmd)

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
            if "Progress:" in line:
                ret = line.split("%")
                if len(ret) > 1:
                    try:
                        percentage = int(ret[0].split()[-1])
                        self.target.update(percentage)
                        dbg(percentage)
                    except (IndexError, ValueError):
                        # Just ignore... probably bad line
                        pass
        self.target.update(100)
        self.__check_process(cmd)

    def create_chapters(self, project_tmpdir, m4b):
        cmd = [
            f'{ivonet.RESOURCE}/mp4chaps',
        ]
        if self.project.chapter_method == CHAPTER_LIST[0]:
            chapter_file = os.path.join(project_tmpdir, "converted.chapters.txt")
            with open(chapter_file, "w") as fo:
                fo.write(self.project.chapter_file())
                self.target.update(10)
            cmd.append("-i")
        else:
            fixed = int(self.project.chapter_method.split()[1].strip()) * 60
            cmd.append("-e")
            cmd.append(str(fixed))
        cmd.append(m4b)

        self.__subprocess(cmd)

        log(f"Adding chapter information to {self.project.title}")
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line
                continue
            if not line:
                dbg(f"Chapter information done: {self.project.title}")
                break
            if "QuickTime" in line:
                self.target.update(50)
        self.__check_process(cmd)
        self.target.update(100)

    def add_cover_art(self, cover, m4b):
        img = wx.Image(BytesIO(self.project.cover_art), wx.BITMAP_TYPE_ANY)
        img.SaveFile(cover, wx.BITMAP_TYPE_PNG)
        self.target.update(10)
        cmd = [
            f"{ivonet.RESOURCE}/mp4art",
            "--add",
            cover,
            m4b
        ]
        self.__subprocess(cmd)

        log(f"Adding Cover Art to: {self.project.title}")
        while self.keep_going:
            try:
                line = self.process.stdout.readline()
            except UnicodeDecodeError:
                #  just skip a line
                continue
            if not line:
                dbg(f"Finished Adding Cover Art to {self.project.title}")
                break
            if "adding" in line:
                self.target.update(50)
        self.__check_process(cmd)
        self.target.update(100)

    def __subprocess(self, cmd):
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
            raise subprocess.CalledProcessError(self.process.returncode, cmd)


class AudiobookEntry(wx.Panel):
    def __init__(self, parent, project: Project, panel_id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, panel_id, style=wx.BORDER_SIMPLE)
        self.parent = parent
        self.start_time = time.perf_counter()
        self.stage = 0  # used for the progressbar based on the different conversion stages
        self.project = project
        self.running = False

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((10, 10), 0, 0, 0)

        self.filename = wx.StaticText(self, wx.ID_ANY,
                                      project.title)  #
        # TODO Tooltip with with complete representation of the book?
        sizer.Add(self.filename, 5, wx.ALIGN_CENTER_VERTICAL, 0)

        self.elapsed = wx.StaticText(self, wx.ID_ANY, "00:00:00")
        sizer.Add(self.elapsed, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_time_indicator, self.refresh_timer)

        # TODO Adjust range to the number of steps in the whole conversion
        self.progress = wx.Gauge(self, wx.ID_ANY, range=600, size=(300, 21), style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer.Add(self.progress, 3, wx.ALIGN_CENTER_VERTICAL, 0)

        self.stop_button = wx.Button(self, wx.ID_ANY, "x")
        self.stop_button.SetMinSize((24, 24))
        sizer.Add(self.stop_button, 0, wx.EXPAND, 0)
        self.Bind(wx.EVT_BUTTON, self.on_stopped, self.stop_button)
        self.Bind(EVT_PROCESS_DONE, self.on_done)

        sizer.Add((10, 10), 0, 0, 0)
        self.SetSizer(sizer)

        self.Layout()
        self.process = ProjectConverterWorker(self, self.project)

    def start(self):
        self.refresh_timer.Start(1000)
        self.process.start()
        self.running = True

    def update(self, percent):
        self.progress.SetValue(int(self.stage * 100 + percent))

    # noinspection PyUnusedLocal
    def stop(self):
        log(f"Finished converting: {self.project.final_name()}")
        self.process.stop()
        self.refresh_timer.Stop()
        self.running = False

    # noinspection PyUnusedLocal
    def on_stopped(self, event):
        if self.running:
            self.stop()
            self.progress.SetBackgroundColour(wx.RED)
        else:
            self.Destroy()

    # noinspection PyUnusedLocal
    def on_done(self, event):
        self.progress.SetBackgroundColour(wx.GREEN)
        self.stop()

    # noinspection PyUnusedLocal
    def on_time_indicator(self, event):
        self.elapsed.SetLabel(time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - self.start_time)))


class QueuePanel(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.SetScrollRate(10, 10)
        self.queue = []
        # TODO Save Queue and state on exit if processing not yet done?

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_refresh, self.refresh_timer)
        self.refresh_timer.Start(1000)

        self.Layout()
        ee.on("queue.project", self.ee_add_project)

    # noinspection PyUnusedLocal
    def on_refresh(self, event):
        self.Refresh()
        self.Layout()

    def ee_add_project(self, project: Project):
        book = AudiobookEntry(self, project)
        self.sizer.Add(book, 0, wx.ALL | wx.EXPAND, 0)
        self.Layout()
        self.queue.append(book)
        book.start()
