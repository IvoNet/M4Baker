import wx

from ivonet.events import _


class MP3DropTarget(wx.FileDropTarget):

    def __init__(self, target):
        super(MP3DropTarget, self).__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        # self.target.write("\n".join(filenames))
        for idx, name in enumerate(filenames):
            _(str(idx), name)
            self.target.Append((name, "TODO"))
        return True


class MP3FileTarget(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MP3DropTarget.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        hs_right_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        bs_right_pnl_m4b_page = wx.BoxSizer(wx.VERTICAL)
        hs_right_pnl_m4b_page.Add(bs_right_pnl_m4b_page, 1, wx.EXPAND, 0)

        self.lc_mp3 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.lc_mp3.SetToolTip("Drag and Drop MP3 files here")
        self.lc_mp3.AppendColumn("MP3", format=wx.LIST_FORMAT_LEFT, width=500)
        self.lc_mp3.AppendColumn("Length", format=wx.LIST_FORMAT_LEFT, width=135)
        bs_right_pnl_m4b_page.Add(self.lc_mp3, 1, wx.EXPAND, 0)

        self.SetDropTarget(MP3DropTarget(self.lc_mp3))

        self.SetSizer(hs_right_pnl_m4b_page)

        self.Layout()
