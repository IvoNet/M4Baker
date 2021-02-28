#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 2021-02-28 13:45:20$"
__copyright__ = "Copyright (c) 2004 - 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """
This little app makes updating the __revised__ variable easy...
"""
__history__ = """
2021-02-28
- Updated to Python 3
2004-11-17
-Added a field with the value of the found or generated state of __revised__
2004-11-16
-New
"""

import wx
from time import localtime, strftime


# noinspection PyUnusedLocal
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1, )
        self.btn_set = wx.Button(self.panel_1, -1, "Set", )
        self.combo_box_1 = wx.ComboBox(self.panel_1, -1, size=(400, 24), choices=[],
                                       style=wx.CB_DROPDOWN)
        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, -1, "", size=(250, 24))

        self.files = {}

        self.__set_properties()
        self.__do_layout()
        self.__do_bind()
        self.__do_startup()

    def __set_properties(self):
        """Program properties are set here"""
        self.SetTitle("Set revised")
        self.btn_set.SetSize((70, 24))
        self.btn_set.SetFocus()
        # self.combo_box_1.SetSize((400, 21))
        # self.combo_box_1.SetSelection(-1)
        self.combo_box_1.SetEditable(False)
        # self.text_ctrl_1.SetSize(wx.Size(400, 21))
        self.text_ctrl_1.SetEditable(False)

    def __do_layout(self):
        """program layout is done here"""
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.btn_set, 0, wx.EXPAND, 0)
        sizer_2.Add(self.combo_box_1, 0, wx.EXPAND, 1)
        sizer_2.Add(self.text_ctrl_1, 0, wx.EXPAND, 0)
        self.panel_1.SetAutoLayout(1)
        self.panel_1.SetSizer(sizer_2)
        # sizer_2.Fit(self.panel_1)
        sizer_2.SetSizeHints(self.panel_1)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)

        self.__make_menu_bar()

        self.Layout()
        self.Centre()

    def __make_menu_bar(self):
        file_menu = wx.Menu()
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    def __do_bind(self):
        """Event binding is done here"""
        self.Bind(wx.EVT_BUTTON, self.on_btn_set, self.btn_set)
        self.Bind(wx.EVT_TEXT, self.on_combo_box_evt, self.combo_box_1)

    def __do_startup(self):
        """these are startup actions -- program init actions"""
        # import IvoNet.Editor.IniFile as IniFile
        from ivonet.io import walk
        import re
        # ini=IniFile.IniFile()
        pat = re.compile("__revised__.*=.*(\$.*\$)")  # __revised__   = "$revised: 2021-02-28 13:45:20$"
        for file in walk('.', True, '*.py;*.pyw', False):
            # if os.path.basename(file).lower() == 'set_revised.py': continue
            inh = open(file, 'r').read()
            found = pat.findall(inh)
            if found:
                self.combo_box_1.Append(file)
                self.files[file] = found[0]
        self.Update()

    def on_btn_set(self, evt):
        """when set button is pressed"""
        f = self.combo_box_1.GetValue()
        fn = open(f, 'r').read()
        tm = '$revised: %s$' % strftime("%Y-%m-%d %H:%M:%S", localtime())
        fn = fn.replace(self.files[f], tm)
        open(f, 'w').write(fn)
        self.files[f] = tm
        self.on_combo_box_evt(None)

    def on_combo_box_evt(self, evt):
        """when combobox selection has occured"""
        f = self.combo_box_1.GetValue()
        if f:
            self.text_ctrl_1.SetValue(self.files[f])

    def on_exit(self, event):
        self.Close(True)


# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "", size=(800, 25))
        self.SetTopWindow(frame_1)
        frame_1.Show(1)
        return 1


# end of class MyApp

if __name__ == "__main__":
    set_revised = MyApp(False)
    set_revised.MainLoop()
