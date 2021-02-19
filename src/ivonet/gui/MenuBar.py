#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import wx

from ivonet import FILE_MENU_PROCESS, FILE_MENU_STOP_PROCESS, FILE_MENU_CLEAR, FILE_MENU_SHOW_LOG, FILE_MENU_TO_DIR


class MenuBar(wx.MenuBar):
    def __init__(self, parent, style=0):
        super().__init__(style)
        self.parent = parent

        file_menu = wx.Menu()
        file_menu.Append(FILE_MENU_PROCESS, "Process\tCTRL-P")
        file_menu.Append(FILE_MENU_STOP_PROCESS, "Stop Processing\tCTRL-S")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_CLEAR, "Clear\tCTRL-E")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_SHOW_LOG, "Show output log\tCTRL-L")
        file_menu.AppendSeparator()
        file_menu.Append(FILE_MENU_TO_DIR, "Select output folder\tCTRL-F")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "Quit\tCTRL-Q")

        self.Append(file_menu, "&File")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT)

        self.Append(help_menu, "&Help")

        # Create event handlers
        menu_handlers = [
            (FILE_MENU_PROCESS, self.parent.on_process),
            (FILE_MENU_STOP_PROCESS, self.parent.on_stop_process),
            (FILE_MENU_CLEAR, self.parent.on_clear),
            (FILE_MENU_TO_DIR, self.parent.on_select_dir),
            (FILE_MENU_SHOW_LOG, self.parent.on_show_log),
            (wx.ID_EXIT, self.parent.on_exit),
            (wx.ID_ABOUT, self.parent.on_about),
        ]
        for menu_id, handler in menu_handlers:
            self.parent.Bind(wx.EVT_MENU, handler, id=menu_id)


class Example(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)

        # create a panel in the frame
        main_panel = wx.Panel(self)

        # put some text with a larger bold font on it
        st = wx.StaticText(main_panel, label="Look at the menu and the statusbar for the events")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))

        self.SetMenuBar(MenuBar(self))
        self.CreateStatusBar()

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def on_about(self, event):
        self.SetStatusText("Menu choice -> About")

    def on_process(self, event):
        self.SetStatusText("Menu choice -> on_process")

    def on_stop_process(self, event):
        self.SetStatusText("Menu choice -> on_stop_process")

    def on_select_dir(self, event):
        self.SetStatusText("Menu choice -> on_select_dir")

    def on_clear(self, event):
        self.SetStatusText("Menu choice -> on_clear")

    def on_show_out_log(self, event):
        self.SetStatusText("Menu choice -> on_show_log")


if __name__ == '__main__':
    app = wx.App()
    ex = Example(None, size=(600, 100))
    ex.Show()
    app.MainLoop()
