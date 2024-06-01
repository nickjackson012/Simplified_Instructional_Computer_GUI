import wx


class AssemblyListingPanel(wx.Panel):
    def __init__(self, parent):
        super(AssemblyListingPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        self.txt_assembly_listing = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        monospaced_font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.txt_assembly_listing.SetFont(monospaced_font)

        # LAYOUT
        vertical_box_sizer.Add(self.txt_assembly_listing, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_box_sizer)

    def load_assembly_listing_file(self, assembly_listing_file_path):
        self.txt_assembly_listing.LoadFile(assembly_listing_file_path)
