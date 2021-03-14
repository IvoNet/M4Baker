#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/03/2021 09:36$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

Post events examples:
wx.PostEvent(EVT_PROJECT_HISTORY, ProjectHistoryEvent(path=path))
wx.PostEvent(EVT_PROJECT_HISTORY, CoverArtEvent(cover=img))


Bind to events examples:
self.Bind(EVT_PROJECT_HISTORY, self.on_project_history)
self.Bind(EVT_PROCESS_DONE, self.on_done)
self.Bind(EVT_COVER_ART, self.on_cover_art_dropped)

method exampleL
    def on_project_history(self, event: ProjectHistoryEvent):
        self.GetMenuBar().file_history.AddFileToHistory(event.path)
        self.save_history()
"""

from wx.lib.newevent import NewEvent

(ProcessDoneEvent, EVT_PROCESS_DONE) = NewEvent()
(ProcessCleanEvent, EVT_PROCESS_CLEAN) = NewEvent()
(ProcessCancelledEvent, EVT_PROCESS_CANCELLED) = NewEvent()
(ProcessExceptionEvent, EVT_PROCESS_ERROR) = NewEvent()
(ProjectHistoryEvent, EVT_PROJECT_HISTORY) = NewEvent()
