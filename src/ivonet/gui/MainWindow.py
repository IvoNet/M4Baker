#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import ivonet
from ivonet.image.IvoNetArtProvider import IvoNetArtProvider
from ivonet.image.images import yoda


class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        self._make_toolbar()

        # create a panel in the frame
        pnl = wx.Panel(self)

        # put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello World!")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
        pnl.SetSizer(sizer)

        # create a menu bar
        self._make_menu_bar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("M4Baker (c) 2021 by IvoNet.nl")

    def _make_toolbar(self):
        """Toolbar"""
        tool_bar_size = (48, 48)
        tool_bar = self.CreateToolBar((wx.TB_HORIZONTAL
                                       | wx.NO_BORDER
                                       | wx.TB_FLAT
                                       # | wx.TB_TEXT
                                       # | wx.TB_HORZ_LAYOUT
                                       )
                                      )
        tool_bar.SetToolBitmapSize(tool_bar_size)

        wx.ArtProvider.Push(IvoNetArtProvider())

        process_bmp = wx.ArtProvider.GetBitmap("inART_PROCESS_1", wx.ART_TOOLBAR, tool_bar_size)
        tool_bar.AddTool(10, "Process", process_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Process", "Start processing", None)
        self.Bind(wx.EVT_TOOL, self.on_tool_clicked, id=10)

        clean_bmp = wx.ArtProvider.GetBitmap("inART_CLEAR", wx.ART_TOOLBAR, tool_bar_size)
        tool_bar.AddTool(20, "Clear", clean_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Clear", "Clear stuff", None)
        self.Bind(wx.EVT_TOOL, self.on_tool_clicked, id=20)

        stop_bmp = wx.ArtProvider.GetBitmap("inART_YODA", wx.ART_TOOLBAR, tool_bar_size)
        tool_bar.AddTool(30, "Stop", stop_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Stop", "Stop stuff", None)
        self.Bind(wx.EVT_TOOL, self.on_tool_clicked, id=30)

        tool_bar.Realize()

    def on_tool_clicked(self, event):
        self.SetStatusText("Clicked {}".format(event.GetId()))

    def _make_menu_bar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT)

        menu_bar = wx.MenuBar()
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def on_about(self, event):
        """Display an About Dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName(ivonet.APP_NAME)
        info.SetVersion(ivonet.VERSION)
        info.SetCopyright(ivonet.COPYRIGHT)
        info.SetDescription(wordwrap(ivonet.ABOUT_DESCRIPTION, 350, wx.ClientDC(self)))
        info.SetWebSite(ivonet.BLOG, ivonet.BLOG_DESCRIPTION)
        info.SetDevelopers(ivonet.DEVELOPERS)
        info.SetLicense(wordwrap(ivonet.LICENSE, 500, wx.ClientDC(self)))
        info.SetIcon(yoda.GetIcon())
        wx.adv.AboutBox(info, self)
