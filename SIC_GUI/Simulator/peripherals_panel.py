import wx

from SIC_GUI.Simulator.Peripherals.input_device_f1_panel import InputDeviceF1Panel
from SIC_GUI.Simulator.Peripherals.output_device_05_panel import OutputDevice05Panel


class PeripheralsPanel(wx.Panel):
    def __init__(self, parent):
        super(PeripheralsPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        input_device_f1_panel = InputDeviceF1Panel(self)
        output_device_05_panel = OutputDevice05Panel(self)

        # LAYOUT
        horizontal_box_sizer.Add(input_device_f1_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        horizontal_box_sizer.Add(output_device_05_panel, proportion=1, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, border=10)

        self.SetSizer(horizontal_box_sizer)