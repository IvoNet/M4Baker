#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 28/02/2021 23:16$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx

from ivonet.events import log, _, ee
from ivonet.gui.ConverArtDropTarget import CoverArtDropTarget
from ivonet.image.images import yoda


class CoverArtStaticBitmap(wx.StaticBitmap):
    """CoverArt specialised StaticBitmap"""
    def __init__(self, parent, id=wx.ID_ANY):
        """StaticBitmap(parent, id=ID_ANY,
        bitmap=NullBitmap, pos=DefaultPosition,
        size=DefaultSize, style=0, name=StaticBitmapNameStr)"""
        super().__init__(parent, id=id)
        self.parent = parent

        self.PhotoMaxSize = 350

        self.SetDropTarget(CoverArtDropTarget())
        self.SetToolTip("Drag and drop Cover Art here. Double click to reset.")
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_reset_cover_art)

        self.cover_art_pristine = False
        self.on_reset_cover_art(None)
        ee.on("cover_art.force", self.ee_on_cover_art)
        ee.on("track.cover_art", self.ee_on_cover_art_from_mp3)

    def dirty(self):
        """Marks the Cover Art set 'dirty'."""
        self.cover_art_pristine = False

    def is_pristine(self):
        """True if no cover art has been set"""
        return self.cover_art_pristine

    def on_reset_cover_art(self, event):
        """Resets the cover art on double clicking the image"""
        self.reset()

    def reset(self):
        _("Reset Cover Art event")
        if not self.cover_art_pristine:
            log("Resetting Cover Art")
            self.SetBitmap(yoda.GetBitmap())
            self.Center()
            self.parent.Refresh()
            self.cover_art_pristine = True

    def ee_on_cover_art(self, image):
        """handles the 'cover_art.force' and 'track.cover_art' events.
        gets an image file object or file location as input.
        """
        log("Setting Cover Art")
        self.dirty()
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        width = img.GetWidth()
        height = img.GetHeight()
        if width > height:
            new_width = self.PhotoMaxSize
            new_height = self.PhotoMaxSize * height / width
        else:
            new_height = self.PhotoMaxSize
            new_width = self.PhotoMaxSize * width / height
        img = img.Scale(new_width, new_height)

        self.SetBitmap(wx.Bitmap(img))
        self.Center()
        self.parent.Refresh()
        ee.emit("project.cover_art", image)

    def ee_on_cover_art_from_mp3(self, image):
        """handles the "track.cover_art" event if the images has not already been set"""
        if self.is_pristine():
            self.dirty()
            self.ee_on_cover_art(image)
