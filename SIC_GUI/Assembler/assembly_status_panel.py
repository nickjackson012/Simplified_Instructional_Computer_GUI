import wx


class AssemblyStatusPanel(wx.Panel):
    def __init__(self, parent):
        super(AssemblyStatusPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_layout = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        self.txt_assembly_status = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        monospaced_font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.txt_assembly_status.SetFont(monospaced_font)

        # LAYOUT
        vertical_layout.Add(self.txt_assembly_status, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_layout)

        # for i in range(300):
        #     txt_assembly_status.write(text="Testing\n")

    def set_assembly_status(self, assembly_status, assembly_error=False):

        self.txt_assembly_status.SetForegroundColour(wx.BLACK)

        if assembly_error:
            self.txt_assembly_status.SetForegroundColour(wx.RED)

        self.txt_assembly_status.AppendText(assembly_status)

    def load_assembly_program_file(self, assembly_program_file_path):
        self.txt_assembly_status.LoadFile(assembly_program_file_path)
        self.txt_assembly_status.AppendText("\nAssembly Program File Ready\n")
        self.txt_assembly_status.AppendText("Click the Assemble button to generate assembly listing and object code\n")


