#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import ivonet


class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

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
        self.make_menu_bar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("M4Baker (c) 2021 by IvoNet.nl")

    def make_menu_bar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT)

        menu_bar = wx.MenuBar()
        menu_bar.Append(help_menu, "&Help")
        # Give the menu bar to the frame
        self.SetMenuBar(menu_bar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
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
        info.SetIcon(wx.Icon(ivonet.APP_ICON, wx.BITMAP_TYPE_PNG))
        wx.adv.AboutBox(info, self)
