#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

__doc__ = """
The main application file. 
The file to rule them all.
Here it all starts and .... ends.
There can be only one.
import this
"""

import wx

from ivonet.gui import MainWindow


class M4Baker(wx.App):
    """The M4Baker app"""

    def __init__(self, redirect=False, filename=None, use_best_visual=False, clear_sig_int=True):
        super(M4Baker, self).__init__(redirect, filename, use_best_visual, clear_sig_int)

        self.Bind(wx.EVT_ACTIVATE_APP, self.on_activate)

    def on_activate(self, event):
        if event.GetActive():
            self.bring_window_to_front()
        event.Skip()

    def bring_window_to_front(self):
        # try:
        self.GetTopWindow().Raise()
        # except:  # TODO specific Exception if thrown here
        #     pass


def main():
    wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
    app = M4Baker(False)
    frame = MainWindow(None, title="B4Baker", size=(800, 600))
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
