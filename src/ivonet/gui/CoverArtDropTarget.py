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
from tinytag import TinyTag

import ivonet
from ivonet.events import log
from ivonet.image import IMAGE_TYPES


class CoverArtDropTarget(wx.FileDropTarget):
    """Listening to image drops on the target it is set to

    This FileDropTarget does not need any init parameters as it will only
    emit an event containing the image file name.

    This drop target will check if the file dropped is an image before
    emitting the event.

    The subscriber is responsible for processing the image.
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def OnDropFiles(self, x, y, filenames):
        """Covers the DropFiles event.
        - Checks if it is an image
        - if a list of images just take the first
        - Sets the cover art
        """
        if len(filenames) > 1:
            log("More than one cover art image was dropped. Taking only the first")

        split_filename = os.path.splitext(filenames[0])
        if len(split_filename) != 2:
            log("The file dropped is probably not valid.")
            return False
        if split_filename[1] == ivonet.FILE_EXTENSION:
            log("Recognized project file. Opening...")
            self.parent.project_open(filenames[0])
            return False
        if split_filename[1] in IMAGE_TYPES:
            with open(filenames[0], 'rb') as img:
                self.parent.set_cover_art(img.read())
        elif filenames[0].lower().endswith(".mp3"):
            tag = TinyTag.get(filenames[0], image=True, ignore_errors=True)
            if tag.get_image():
                self.parent.set_cover_art(tag.get_image())
            else:
                log("Could not retrieve any Cover Art from the dropped mp3 file.")
        else:
            log(f"File {filenames[0]} is not an image.")
            return False
        log("Cover art dropped")
        return True
