import wx

from ivonet.events import log, ee


class MP3DropTarget(wx.FileDropTarget):

    def __init__(self, target):
        super().__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        log("MP3 Files dropped")

        mp3s = []
        for name in filenames:
            if name.lower().endswith(".mp3"):
                mp3s.append(name)
            else:
                log(f"Dropped file '{name}' is not an mp3 file.")

        ee.emit("audiobook.tracks", mp3s)

        return True


class MP3FileTarget(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        hs_right_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        bs_right_pnl_m4b_page = wx.BoxSizer(wx.VERTICAL)
        hs_right_pnl_m4b_page.Add(bs_right_pnl_m4b_page, 1, wx.EXPAND, 0)

        self.lc_mp3 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.lc_mp3.SetToolTip("Drag and Drop MP3 files here")
        # self.lc_mp3.AppendColumn("#", format=wx.LIST_FORMAT_LEFT, width=20)
        self.lc_mp3.AppendColumn("Track", format=wx.LIST_FORMAT_LEFT, width=500)
        self.lc_mp3.AppendColumn("Length", format=wx.LIST_FORMAT_LEFT, width=135)
        bs_right_pnl_m4b_page.Add(self.lc_mp3, 1, wx.EXPAND, 0)

        self.SetDropTarget(MP3DropTarget(self.lc_mp3))

        self.SetSizer(hs_right_pnl_m4b_page)

        self.Layout()
