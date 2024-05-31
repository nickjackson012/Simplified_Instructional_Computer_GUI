import wx


class AssemblyStatusPanel(wx.Panel):
    def __init__(self, parent):
        super(AssemblyStatusPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_layout = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        txt_assembly_status = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # LAYOUT
        vertical_layout.Add(txt_assembly_status, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_layout)

        for i in range(300):
            txt_assembly_status.write(text="Testing\n")