#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx

from ivonet.image.images import catalog, index


class IvoNetArtProvider(wx.ArtProvider):
    """
    The IvoNet ArtProvider.
    """

    def __init__(self, art_id_prefix="inART_"):
        self.prefix = art_id_prefix
        self.catalog = catalog
        self.index = index

        wx.ArtProvider.__init__(self)

    def generate_art_id_list(self):
        return [self.prefix + name.upper() for name in self.index]

    def CreateBitmap(self, art_id, client, size):
        if art_id.startswith(self.prefix):
            name = art_id[len(self.prefix):].lower()
            if name in self.catalog:
                return self.catalog[name].GetBitmap()

        return wx.NullBitmap
