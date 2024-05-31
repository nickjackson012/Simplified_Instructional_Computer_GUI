import wx

from SIC_GUI.Simulator.Peripherals.input_panel import InputPanel


class InputDeviceF1Panel(wx.Panel):
    def __init__(self, parent):
        super(InputDeviceF1Panel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # PANELS
        input_panel = InputPanel(self)

        # CONTROLS
        lbl_info = wx.StaticText(self, label="Input one character and press Enter")
        btn_end_of_file = wx.Button(self, label="End of File")
        btn_end_of_record = wx.Button(self, label="End of Record")
        btn_enter = wx.Button(self, label="Enter")
        btn_newline = wx.Button(self, label="Newline")

        # LAYOUT
        grid_bag_sizer.Add(lbl_info, pos=(0, 0), span=(0, 4), flag=wx.ALIGN_LEFT | wx.EXPAND)
        grid_bag_sizer.Add(input_panel, pos=(1, 0), span=(0, 4), flag=wx.EXPAND)
        grid_bag_sizer.Add(btn_end_of_file, pos=(2, 0))
        grid_bag_sizer.Add(btn_end_of_record, pos=(2, 1))
        grid_bag_sizer.Add(btn_newline, pos=(2, 2))
        grid_bag_sizer.Add(btn_enter, pos=(2, 3))

        # STATIC BOX
        input_device_f1_static_box = wx.StaticBox(self, label="Input Device F1", size=wx.DefaultSize)
        static_box_sizer = wx.StaticBoxSizer(input_device_f1_static_box, orient=wx.VERTICAL)

        static_box_sizer.Add(grid_bag_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # LAYOUT
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # LAYOUT
        vertical_box_sizer.Add(static_box_sizer, proportion=0, flag=wx.EXPAND)

        self.SetSizer(vertical_box_sizer)