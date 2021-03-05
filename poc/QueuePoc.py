#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-03-04 22:53:00$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

/Users/iwo16283/dev/ivonet-audiobook/src/resources/ffmpeg -i "/Users/iwo16283/dev/ivonet-audiobook/mp3_tests/Acorna Series/01 - Acorna The Unicorn Girl/mp3/Anne McCaffrey-Acorna 01.mp3" -v quiet -stats -threads 4 -vn -y -acodec aac -strict -2 -map_metadata 0 -map_metadata:s:a 0:s:a  -ac 1 "test.m4a"
"""

import _thread
import re
import subprocess
import time

import wx
import wx.lib.newevent

import ivonet
from ivonet.io import unique_name

(ProcessDoneEvent, EVT_PROCESS_DONE) = wx.lib.newevent.NewEvent()


def time_seconds(seq) -> int:
    """ Calculates the time in seconds based on hours, minutes, seconds.
    The milliseconds are ignored. That kind of accuracy is not needed
    :param seq: (hours, minutes, seconds, [milliseconds])
    :return: int of seconds
    """
    return int(seq[0]) * 3600 + int(seq[1]) * 60 + int(seq[2])


class FfmpegThread(object):
    DURATION = re.compile(".*Duration: ([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{2}).*")
    TIME_ELAPSED = re.compile(".*size=.*time=([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{2}).*")

    def __init__(self, parent, project) -> None:
        self.target = parent
        self.keep_going = False
        self.running = False
        self.pid = None
        self.project = project
        self.total_duration = 0
        self.progress = 0
        self.ffmpeg = None

    def calc_percentage_done(self, seq):
        return int(time_seconds(seq) * 100 / self.total_duration)

    def start(self):
        self.keep_going = self.running = True
        _thread.start_new_thread(self.run, ())

    def stop(self):
        self.keep_going = False

    def run(self):
        cmd = [f'{ivonet.RESOURCE}/ffmpeg',
               '-i',
               self.project,
               # "-v", "quiet",
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
               unique_name("test.m4a")
               ]
        print(cmd)
        self.ffmpeg = subprocess.Popen(
            cmd,  # args should be a string, or a sequence of program
            # arguments. The program to execute is normally the first item
            # in the args sequence or string, but can be explicitly set by
            # using the executable argument.
            # bufsize=0,
            # executable=None,  # The executable argument specifies the program
            # to execute. It is very seldom needed: Usually, the program
            # to execute is defined by the args argument. If shell=True,
            # the executable argument specifies which shell to use.
            # On Unix, the default shell is /bin/sh. On Windows, the
            # default shell is specified by the COMSPEC environment variable.
            stdin=subprocess.PIPE,  # stdin, stdout and stderr specify the
            # executed programs' standard input, standard output and
            # standard error file handles, respectively. Valid values
            # are PIPE, an existing file descriptor (a positive integer),
            # an existing file object, and None. PIPE indicates that a new
            # pipe to the child should be created. With None, no
            # redirection will occur; the child's file handles will be
            # inherited from the parent. Additionally, stderr can be
            # STDOUT, which indicates that the stderr data from the
            # applications should be captured into the same file handle
            # as for stdout.
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # preexec_fn=None,  # If preexec_fn is set to a callable object,
            # this object will be called in the child process just before
            # the child is executed.
            # close_fds=False,  # If close_fds is true, all file descriptors
            # except 0, 1 and 2 will be closed before the child process
            # is executed.
            shell=False,  # If shell is True, the specified command will be
            # executed through the shell.
            # cwd=None,  # If cwd is not None, the current directory will be
            # changed to cwd before the child is executed.
            # env=None,  # If env is not None, it defines the environment
            # variables for the new process.
            universal_newlines=True,  # If universal_newlines is True,
            # the file objects stdout and stderr are opened as a text
            # files, but lines may be terminated by any of '\n', the
            # Unix end-of-line convention, '\r', the Macintosh
            # convention or '\r\n', the Windows convention. All of
            # these external representations are seen as '\n' by the
            # Python program. Note: This feature is only available if
            # Python is built with universal newline support (the default).
            # Also, the newlines attribute of the file objects stdout,
            # stdin and stderr are not updated by the communicate() method.
            # startupinfo=None,  # startupinfo, #The startupinfo and
            # creationflags, if given, will be passed to the underlying
            # CreateProcess() function. They can specify things such as
            # appearance of the main window and priority for the new
            # process. (Windows only)
            # creationflags= win32process.CREATE_NO_WINDOW,
        )
        self.ffmpeg.stdin.close()  # You can close the handle of course after creation

        # self.pid = self.ffmpeg.pid  # Child process id... Needed if abort is called
        # print(self.pid)
        while self.keep_going:
            # print(self.keep_going)
            line = self.ffmpeg.stdout.readline()
            if not line:
                self.keep_going = False
                break
            # print(line)
            duration = self.DURATION.match(line)
            if duration:
                self.total_duration = time_seconds(duration.groups())
                print(self.total_duration)
                continue
            elapsed = self.TIME_ELAPSED.match(line)
            if elapsed:
                self.progress = self.calc_percentage_done(elapsed.groups())
                self.target.update(self.progress)

        if self.ffmpeg and not self.keep_going:
            self.ffmpeg.terminate()

        self.ffmpeg.stdout.close()
        self.ffmpeg.wait()
        if self.ffmpeg.returncode != 0 and self.keep_going:
            # Only throw an exception if the process terminated wrong
            # but we wanted to keep going
            raise subprocess.CalledProcessError(self.ffmpeg.returncode, cmd)
        wx.PostEvent(self.target, ProcessDoneEvent(project=self.project, value=self.ffmpeg.returncode))


class AudiobookEntry(wx.Panel):
    def __init__(self, parent, project, panel_id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, panel_id, style=wx.BORDER_SIMPLE)

        self.start_time = time.perf_counter()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((10, 10), 0, 0, 0)

        self.filename = wx.StaticText(self, wx.ID_ANY, project)
        sizer.Add(self.filename, 5, wx.ALIGN_CENTER_VERTICAL, 0)

        self.time_indicator = wx.StaticText(self, wx.ID_ANY, "00:00:00")
        sizer.Add(self.time_indicator, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_time_indicator, self.refresh_timer)
        self.refresh_timer.Start(1000)

        self.progress = wx.Gauge(self, wx.ID_ANY, 100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer.Add(self.progress, 3, wx.ALIGN_CENTER_VERTICAL, 0)

        self.stop_button = wx.Button(self, wx.ID_ANY, "x")
        self.stop_button.SetMinSize((24, 34))
        sizer.Add(self.stop_button, 0, wx.EXPAND, 0)
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.stop_button)
        self.Bind(EVT_PROCESS_DONE, self.on_stop)

        sizer.Add((10, 10), 0, 0, 0)
        self.SetSizer(sizer)

        self.Layout()

        self.process = FfmpegThread(self, project)
        self.process.start()

    def on_stop(self, event):
        print("Stopping")
        self.process.stop()
        self.refresh_timer.Stop()

    def update(self, percent):
        self.progress.SetValue(percent)

    def on_time_indicator(self, event):
        print("on_refresh_time")
        elapsed = time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - self.start_time))
        self.time_indicator.SetLabel(elapsed)
        print(elapsed)
        self.Refresh()
        self.Layout()


# end of class AudiobookEntry

class QueuePanel(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.SetScrollRate(10, 10)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.sizer)

        self.Layout()

    def add_audiobook(self, audiobook):
        book = AudiobookEntry(self, audiobook)
        self.sizer.Add(book, 0, wx.ALL | wx.EXPAND, 0)
        self.Layout()
        return book


class QueueFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1024, 800))
        self.SetTitle("frame")

        self.queue = QueuePanel(self, wx.ID_ANY)
        self.Layout()

        self.queue.add_audiobook(
            "/Users/iwo16283/dev/ivonet-audiobook/mp3_tests/Acorna Series/01 - Acorna The Unicorn Girl/mp3/Anne McCaffrey-Acorna 01.mp3")
        # self.queue.add_audiobook(
        #     "/Users/iwo16283/dev/ivonet-audiobook/mp3_tests/Acorna Series/01 - Acorna The Unicorn Girl/mp3/Anne McCaffrey-Acorna 02.mp3")


class QueueApp(wx.App):
    def OnInit(self):
        self.frame = QueueFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    QuePanel = QueueApp(0)
    QuePanel.MainLoop()
