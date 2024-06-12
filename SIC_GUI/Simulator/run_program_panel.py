import wx

from SIC_GUI.Simulator.Run_Program.left_panel import LeftPanel
from SIC_GUI.Simulator.Run_Program.right_panel import RightPanel


class RunProgramPanel(wx.Panel):
    def __init__(self, parent):
        super(RunProgramPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)

        # LAYOUT
        horizontal_box_sizer.Add(self.left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        horizontal_box_sizer.Add(self.right_panel, proportion=1, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, border=10)

        self.SetSizer(horizontal_box_sizer)

    def update_memory_text_ctrl(self, memory_address_hex_string="0"):
        self.right_panel.update_memory_text_ctrl(memory_address_hex_string)

    def update_registers_text_ctrls(self):
        self.left_panel.update_registers_text_ctrls()

    def update_instruction_text_ctrl(self, line_of_code):
        self.left_panel.update_instruction_text_ctrl(line_of_code)

    def print_assembly_listing_line(self, parsed_listing_dict):
        self.left_panel.print_assembly_listing_line(parsed_listing_dict)

    def set_state_of_run_program_buttons(self, enable_reset, enable_run, enable_step):
        self.left_panel.set_state_of_run_program_buttons(enable_reset, enable_run, enable_step)

    def dump_registers(self):
        self.left_panel.dump_registers()

    def initialize_instruction_and_registers_history_txt_ctrl(self):
        self.left_panel.initialize_instruction_and_registers_history_txt_ctrl()

