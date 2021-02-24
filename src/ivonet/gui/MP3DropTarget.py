import wx


class MP3DropTarget(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MP3DropTarget.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        hs_right_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        bs_right_pnl_m4b_page = wx.BoxSizer(wx.VERTICAL)
        hs_right_pnl_m4b_page.Add(bs_right_pnl_m4b_page, 1, wx.EXPAND, 0)

        self.lc_mp3 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.lc_mp3.SetToolTip("Drag and Drop MP3 files here")
        self.lc_mp3.AppendColumn("mp3", format=wx.LIST_FORMAT_LEFT, width=498)
        self.lc_mp3.AppendColumn("length", format=wx.LIST_FORMAT_LEFT, width=80)
        bs_right_pnl_m4b_page.Add(self.lc_mp3, 1, wx.EXPAND, 0)

        self.SetSizer(hs_right_pnl_m4b_page)

        self.Layout()
