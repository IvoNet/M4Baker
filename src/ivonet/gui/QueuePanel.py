#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:21:13$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
Yup the Queue Panel. 
"""

import math
import random

import wx
import wx.lib.agw.ultimatelistctrl as ULC

from ivonet.events import ee

PIPE_HEIGHT = 18
PIPE_WIDTH = 300


class TempListCtrl(wx.ListCtrl):
    """ListCtrl(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=LC_ICON,
    validator=DefaultValidator, name=ListCtrlNameStr)"""

    def __init__(self, target, ctrl_id=wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES):
        super().__init__(target, id=ctrl_id, style=style)

        self.AppendColumn("Audiobook", format=wx.LIST_FORMAT_LEFT, width=200)
        self.AppendColumn("Progress", format=wx.LIST_FORMAT_LEFT, width=650)
        self.AppendColumn("Status", format=wx.LIST_FORMAT_LEFT, width=100)


class ProgressBarRenderer(object):
    DONE_BITMAP = None
    REMAINING_BITMAP = None

    def __init__(self, parent):

        self.progress_value = random.randint(1, 99)

    def DrawSubItem(self, dc, rect, line, highlighted, enabled):
        """Draw a custom progress bar using double buffering to prevent flicker"""

        canvas = wx.Bitmap(rect.width, rect.height)
        mdc = wx.MemoryDC()
        mdc.SelectObject(canvas)

        if highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)))
        mdc.Clear()

        self.DrawProgressBar(mdc, 0, 0, rect.width, rect.height, self.progress_value)

        mdc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        text = "%d Mb" % self.progress_value
        textWidth, dummy = mdc.GetTextExtent(text)
        mdc.DrawText(text, rect.width / 2 - textWidth / 2, rect.height / 2 - dummy / 2)
        dc.SetClippingRegion(rect.x, rect.y, rect.width, rect.height)
        dc.Blit(rect.x + 3, rect.y, rect.width - 6, rect.height, mdc, 0, 0)
        dc.DestroyClippingRegion()

    def GetLineHeight(self):

        return PIPE_HEIGHT + 6

    def GetSubItemWidth(self):

        return 130

    def UpdateValue(self):

        self.progress_value += 5
        if self.progress_value >= 100:
            self.progress_value = 1

    def DrawHorizontalPipe(self, dc, x, y, w, colour):
        """Draws a horizontal 3D-looking pipe."""

        for r in range(PIPE_HEIGHT):
            red = int(colour.Red() * math.sin((math.pi / PIPE_HEIGHT) * r))
            green = int(colour.Green() * math.sin((math.pi / PIPE_HEIGHT) * r))
            blue = int(colour.Blue() * math.sin((math.pi / PIPE_HEIGHT) * r))
            dc.SetPen(wx.Pen(wx.Colour(red, green, blue)))
            dc.DrawLine(x, y + r, x + w, y + r)

    def DrawProgressBar(self, dc, x, y, w, h, percent):
        """
        Draws a progress bar in the (x,y,w,h) box that represents a progress of
        'percent'. The progress bar is only horizontal and it's height is constant
        (PIPE_HEIGHT). The 'h' parameter is used to vertically center the progress
        bar in the allotted space.

        The drawing is speed-optimized. Two bitmaps are created the first time this
        function runs - one for the done (green) part of the progress bar and one for
        the remaining (white) part. During normal operation the function just cuts
        the necessary part of the two bitmaps and draws them.
        """

        # Create two pipes
        if self.DONE_BITMAP is None:
            self.DONE_BITMAP = wx.Bitmap(PIPE_WIDTH, PIPE_HEIGHT)
            mdc = wx.MemoryDC()
            mdc.SelectObject(self.DONE_BITMAP)
            self.DrawHorizontalPipe(mdc, 0, 0, PIPE_WIDTH, wx.GREEN)
            mdc.SelectObject(wx.NullBitmap)

            self.REMAINING_BITMAP = wx.Bitmap(PIPE_WIDTH, PIPE_HEIGHT)
            mdc = wx.MemoryDC()
            mdc.SelectObject(self.REMAINING_BITMAP)
            self.DrawHorizontalPipe(mdc, 0, 0, PIPE_WIDTH, wx.RED)
            self.DrawHorizontalPipe(mdc, 1, 0, PIPE_WIDTH - 1, wx.WHITE)
            mdc.SelectObject(wx.NullBitmap)

        # Center the progress bar vertically in the box supplied
        y = int(y + (h - PIPE_HEIGHT) / 2)

        if percent == 0:
            middle = 0
        else:
            middle = int((w * percent) / 100)

        if middle == 0:  # not started
            bitmap = self.REMAINING_BITMAP.GetSubBitmap((1, 0, w, PIPE_HEIGHT))
            dc.DrawBitmap(bitmap, x, y, False)
        elif middle == w:  # completed
            bitmap = self.DONE_BITMAP.GetSubBitmap((0, 0, w, PIPE_HEIGHT))
            dc.DrawBitmap(bitmap, x, y, False)
        else:  # in progress
            doneBitmap = self.DONE_BITMAP.GetSubBitmap((0, 0, middle, PIPE_HEIGHT))
            dc.DrawBitmap(doneBitmap, x, y, False)
            remainingBitmap = self.REMAINING_BITMAP.GetSubBitmap((0, 0, w - middle, PIPE_HEIGHT))
            dc.DrawBitmap(remainingBitmap, x + middle, y, False)


class QueueUltimateListCtrl(ULC.UltimateListCtrl):
    def __init__(self,
                 parent,
                 id=wx.ID_ANY,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=0,
                 agw_style=ULC.ULC_REPORT | ULC.ULC_VRULES | ULC.ULC_HRULES | ULC.ULC_SINGLE_SEL |
                           ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
                 ):
        ULC.UltimateListCtrl.__init__(self, parent, id, pos, size, style, agw_style)

        self.InsertColumn(0, "Audiobook")
        self.InsertColumn(1, "Time", width=100)
        self.InsertColumn(2, "Progress", width=200)

        self.SetColumnWidth(0, ULC.ULC_AUTOSIZE_FILL)


class QueuePanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL | wx.WANTS_CHARS | wx.SUNKEN_BORDER
        wx.Panel.__init__(self, *args, **kwds)
        self.count = 0

        hs_queue = wx.BoxSizer(wx.HORIZONTAL)

        vs_queue = wx.BoxSizer(wx.VERTICAL)
        hs_queue.Add(vs_queue, 1, wx.EXPAND, 0)

        self.queue = QueueUltimateListCtrl(self)

        #  test
        info = ULC.UltimateListItem()
        info.SetId(0)
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_CHECK
        # # info._image = [1, 2]
        # info._format = 0
        # # info._kind = 1
        info._text = "Queen"
        # self.queue.InsertStringItem(0, info)
        # self.queue.InsertColumnInfo(0, info)

        vs_queue.Add(self.queue, 1, wx.EXPAND, 0)

        self.progress = wx.Gauge(self, -1, 100, (110, 50), (250, -1))
        vs_queue.Add(self.progress, 0, wx.EXPAND, 0)

        # TODO TEMP Code while progressbar not yet implemented
        self.Bind(wx.EVT_TIMER, self.timer_handler)
        self.timer = wx.Timer(self)
        ee.on("processing.start", self.on_start)
        ee.on("processing.stop", self.on_stop)
        # /TEMP Code while progressbar not yet implemented

        self.SetSizer(hs_queue)
        self.Layout()

    # noinspection PyUnusedLocal
    def on_start(self, event):
        self.timer.Start(100)

    # noinspection PyUnusedLocal
    def on_stop(self, event):
        self.timer.Stop()
        self.count = 0
        self.progress.SetValue(self.count)

    # noinspection PyUnusedLocal
    def timer_handler(self, event):
        self.count = self.count + 1

        if self.count >= 100:
            self.count = 0

        self.progress.SetValue(self.count)
