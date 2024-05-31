import wx


class ExecutionControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ExecutionControlPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # CONTROLS
        btn_end = wx.Button(self, label="End")
        btn_run = wx.Button(self, label="Run")
        btn_step = wx.Button(self, label="Step")

        # LAYOUT
        grid_bag_sizer.Add(btn_end, pos=(0, 0), flag=wx.ALIGN_RIGHT)
        grid_bag_sizer.Add(btn_run, pos=(0, 1), flag=wx.ALIGN_CENTER)
        grid_bag_sizer.Add(btn_step, pos=(0, 2), flag=wx.ALIGN_RIGHT)

        self.SetSizer(grid_bag_sizer)