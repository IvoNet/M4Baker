#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
A Cover Art specialized FileDropTarget
"""

import os

import wx

from ivonet.events import log, ee
from ivonet.image import IMAGE_TYPES
from ivonet.model.Track import Track


class CoverArtDropTarget(wx.FileDropTarget):
    """Listening to image drops on the target it is set to

    This FileDropTarget does not need any init parameters as it will only
    emit an event containing the image file name.

    This drop target will check if the file dropped is an image before
    emitting the event.

    The subscriber is responsible for processing the image.
    """

    def __init__(self):
        super().__init__()

    def OnDropFiles(self, x, y, filenames):
        """Covers the DropFiles event.
        - Checks if it is an image
        - if a list of images just take the first
        - emit a "cover_art.force" event with the name of the file
        """
        log("Cover art dropped")
        if len(filenames) > 1:
            log("More than one cover art image was dropped. Taking only the first")

        split_filename = os.path.splitext(filenames[0])
        if len(split_filename) != 2:
            log("The file dropped is probably not an image.")
            return False
        if split_filename[1] in IMAGE_TYPES:
            ee.emit("cover_art.force", filenames[0])
        elif filenames[0].lower().endswith(".mp3"):
            track = Track(filenames[0], silent=True)
            if track.get_cover_art():
                ee.emit("cover_art.force", track.get_cover_art())
            else:
                log("Could not retrieve any Cover Art from the dropped mp3 file.")
        else:
            log(f"File {filenames[0]} is not an image.")
            return False
        return True
