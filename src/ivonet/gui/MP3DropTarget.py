#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 08/03/2021 19:57$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx

from ivonet.events import log
from ivonet.model.Track import Track


class MP3DropTarget(wx.FileDropTarget):
    """Handler for the Drag and Drop events of MP3 files"""

    def __init__(self, target):
        super().__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        log("MP3 Files dropped")

        for name in filenames:
            if name.lower().endswith(".mp3") and name not in self.target.lc_mp3.GetStrings():
                Track(name, silent=False)
                self.target.append_track(name)
            else:
                log(f"Dropped file '{name}' is not an mp3 file or not unique in the list.")
        return True
