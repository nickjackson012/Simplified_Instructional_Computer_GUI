import wx

from SIC_Assembler.sic_assembler import assembler_pass_one, assembler_pass_two, SICAssemblerError
from SIC_Assembler.sic_assembly_parser import parse_assembly_code_file, SICAssemblyParserError
from SIC_GUI.Assembler.assembly_listing_panel import AssemblyListingPanel
from SIC_GUI.Assembler.assembly_status_panel import AssemblyStatusPanel
from SIC_GUI.Assembler.control_panel import ControlPanel
from SIC_GUI.Assembler.object_code_panel import ObjectCodePanel
from SIC_Utilities.sic_messaging import print_error


class AssemblerPanel(wx.Panel):
    def __init__(self, parent):
        super(AssemblerPanel, self).__init__(parent)

        self.disable_file_context_tabs = True

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROL PANEL
        self.control_panel = ControlPanel(self)

        # NOTEBOOK
        self.notebook_assembler = wx.Notebook(self)

        self.tab_assembler_status = AssemblyStatusPanel(self.notebook_assembler)
        self.notebook_assembler.AddPage(self.tab_assembler_status, "Assembly Status")

        self.tab_assembly_listing = AssemblyListingPanel(self.notebook_assembler)
        self.notebook_assembler.AddPage(self.tab_assembly_listing, "Assembly Listing")

        self.tab_object_code = ObjectCodePanel(self.notebook_assembler)
        self.notebook_assembler.AddPage(self.tab_object_code, "Object Code")

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.notebook_tab_handler)

        # LAYOUT
        vertical_box_sizer.Add(self.control_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=20)
        vertical_box_sizer.Add(self.notebook_assembler, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
                               border=20)

        self.SetSizer(vertical_box_sizer)

        # EVENT HANDLING
        self.Bind(wx.EVT_BUTTON, self.button_handler)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.file_picker_changed_handler)

    def file_picker_changed_handler(self, event):
        self.notebook_assembler.ChangeSelection(0)
        assembly_program_file_path = self.control_panel.get_file_path()
        self.tab_assembler_status.load_assembly_program_file(assembly_program_file_path)
        self.tab_assembly_listing.clear_assembly_listing()
        self.tab_object_code.clear_object_code()
        self.control_panel.enable_assemble_button()

    def notebook_tab_handler(self, event):
        tab = event.GetEventObject()
        tab_number = tab.GetSelection()
        if tab.GetPageText(tab_number) == "Assembly Status":
            if self.disable_file_context_tabs:
                event.Veto()

    def button_handler(self, event):
        try:
            # Get complete file path from the assembler control panel file picker control
            program_file_path = self.control_panel.get_file_path()

            # Parse assembly code
            parsed_code_dict_list = parse_assembly_code_file(program_file_path, self.tab_assembler_status)

            # Execute pass one and pass two assembly
            assembler_pass_one(parsed_code_dict_list, self.tab_assembler_status)
            assembler_pass_two(parsed_code_dict_list, program_file_path, self.tab_assembler_status)

            # Load *.lst and *.obj into the corresponding notebook tabs
            assembly_listing_file_path = program_file_path.replace(".asm", ".lst")
            self.tab_assembly_listing.load_assembly_listing_file(assembly_listing_file_path)

            object_code_file_path = program_file_path.replace(".asm", ".obj")
            self.tab_object_code.load_object_code_file(object_code_file_path)

            self.disable_file_context_tabs = False
        except (SICAssemblyParserError, SICAssemblerError) as ex:
            # ERROR
            print_error(str(ex))
            self.tab_assembler_status.set_assembly_status(str(ex), assembly_error=True)

