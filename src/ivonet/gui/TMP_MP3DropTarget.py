#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import wx


class MP3DropTarget(wx.FileDropTarget):

    def __init__(self, target):
        super(MP3DropTarget, self).__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        self.target.write("\n".join(filenames))
        return True


class Example(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)

        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.text.SetDropTarget(MP3DropTarget(self.text))

        self.SetTitle('File drag and drop')
        self.Centre()

        self.SetMenuBar(wx.MenuBar())
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    ex = Example(None, size=(800, 600))
    ex.Show()
    app.MainLoop()
