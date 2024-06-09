import wx


class InputPanel(wx.Panel):
    def __init__(self, parent):
        super(InputPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        input_grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        lbl_input = wx.StaticText(self, label="Input")
        self.txt_input = wx.TextCtrl(self)
        self.txt_input.SetMaxLength(1)
        self.txt_input.SetFont(MONOSPACED_FONT)

        # LAYOUT
        input_grid_bag_sizer.Add(lbl_input, pos=(0, 0))
        input_grid_bag_sizer.Add(self.txt_input, pos=(0, 1), flag=wx.EXPAND)
        input_grid_bag_sizer.AddGrowableCol(idx=1)

        self.SetSizer(input_grid_bag_sizer)

    def initialize(self):
        self.txt_input.Clear()
