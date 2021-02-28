import wx
import wx.adv

from ivonet.events import log, ee, _


class MP3DropTarget(wx.FileDropTarget):

    def __init__(self):
        super().__init__()

    def OnDropFiles(self, x, y, filenames):
        log("MP3 Files dropped")

        mp3s = []
        for name in filenames:
            if name.lower().endswith(".mp3"):
                mp3s.append(name)
            else:
                log(f"Dropped file '{name}' is not an mp3 file.")

        ee.emit("audiobook.mp3s", mp3s)

        return True


class MP3ListBox(wx.adv.EditableListBox):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetStrings([])
        self.SetDropTarget(MP3DropTarget())
        self.SetToolTip("Drag and Drop MP3 files here")
        self.del_button = self.GetDelButton()

    def append(self, line):
        lines = list(self.GetStrings())
        lines.append(line)
        self.SetStrings(lines)

    def clear(self):
        self.SetStrings([])


class MP3FileTarget(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        hs_right_pnl_m4b_page = wx.BoxSizer(wx.HORIZONTAL)

        bs_right_pnl_m4b_page = wx.BoxSizer(wx.VERTICAL)
        hs_right_pnl_m4b_page.Add(bs_right_pnl_m4b_page, 1, wx.EXPAND, 0)

        self.lc_mp3 = MP3ListBox(self, wx.ID_ANY, "Drag and Drop mp3 files below...",
                                 style=wx.adv.EL_ALLOW_DELETE)

        bs_right_pnl_m4b_page.Add(self.lc_mp3, 1, wx.EXPAND, 0)

        self.SetSizer(hs_right_pnl_m4b_page)

        self.Layout()
        ee.on("audiobook.tracks", self.ee_on_tracks)
        ee.on("audiobook.new", self.ee_on_new_audiobook)

    def ee_on_tracks(self, tracks):
        for idx, track in enumerate(tracks):
            _(track)
            # self.lc_mp3.SetItem(self.lc_mp3.GetItemCount(), 0, track.mp3)
            self.lc_mp3.append(track.mp3)

    def ee_on_new_audiobook(self):
        self.lc_mp3.clear()
