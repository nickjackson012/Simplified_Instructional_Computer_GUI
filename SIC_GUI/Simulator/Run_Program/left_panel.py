import wx

from SIC_GUI.Simulator.Run_Program.instruction_and_registers_history_panel import InstructionAndRegistersHistoryPanel
from SIC_GUI.Simulator.Run_Program.instruction_and_registers_panel import InstructionAndRegistersPanel


class LeftPanel(wx.Panel):
    def __init__(self, parent):
        super(LeftPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # PANELS
        self.instruction_and_registers_panel = InstructionAndRegistersPanel(self)
        self.instruction_and_registers_history_panel = InstructionAndRegistersHistoryPanel(self)

        # LAYOUT
        vertical_box_sizer.Add(self.instruction_and_registers_panel, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=10)
        vertical_box_sizer.Add(self.instruction_and_registers_history_panel, proportion=1, flag=wx.EXPAND)

        self.SetSizer(vertical_box_sizer)

    def update_registers_text_ctrls(self):
        self.instruction_and_registers_panel.update_registers_text_ctrls()

    def update_instruction_text_ctrl(self, line_of_code):
        self.instruction_and_registers_panel.update_instruction_text_ctrl(line_of_code)

    def print_assembly_listing_line(self, parsed_listing_dict):
        self.instruction_and_registers_history_panel.print_assembly_listing_line(parsed_listing_dict)

    def set_state_of_run_program_buttons(self, enable_reset, enable_run, enable_step):
        self.instruction_and_registers_panel.set_state_of_run_program_buttons(enable_reset, enable_run, enable_step)

    def dump_registers(self):
        self.instruction_and_registers_history_panel.dump_registers()

    def initialize_instruction_and_registers_history_txt_ctrl(self):
        self.instruction_and_registers_history_panel.initialize_instruction_and_registers_history_txt_ctrl()