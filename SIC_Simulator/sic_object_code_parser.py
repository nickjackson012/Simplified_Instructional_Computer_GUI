import os.path

from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_Utilities.sic_constants import SIC_OBJECT_CODE_FILE_EXTENSION
from SIC_Utilities.sic_converter import test_for_hex, hex_string_to_dec


class SICObjectCodeParserError(Exception):
    pass


# This function parses the header line of object code.
# It stores record type, program name, program start address, program length and unparsed line of code.
# It returns all the items recorded in a line of object code dictionary.
def parse_header_record(unparsed_line_of_object_code):
    # Validate unparsed line of code
    # Make sure length of header line is 19 characters and verifies that expected hex characters are hex digits.
    if len(unparsed_line_of_object_code) == 19 and test_for_hex(unparsed_line_of_object_code[7:]):
        parsed_line_of_object_code_dict = {"record_type": "header",
                                           "program_name": unparsed_line_of_object_code[1:7].rstrip(),
                                           "program_start_address": unparsed_line_of_object_code[9:13],
                                           "program_length": unparsed_line_of_object_code[15:19],
                                           "unparsed_line_of_object_code": unparsed_line_of_object_code}

        return parsed_line_of_object_code_dict

    else:
        # ERROR
        raise SICObjectCodeParserError("Invalid header record")

    # This function parses the text line of object code.


# It stores record type, line start address, byte count, a byte list and unparsed line of code.
# It returns all the items recorded in a line of object code dictionary.
def parse_text_record(unparsed_line_of_object_code):
    # Validate unparsed line of object code
    # Make sure that text record line is between 11 and 69 characters
    # Verifies that expected hex characters are hex digits
    # Verifies that the object code is an even number of characters
    if (11 <= len(unparsed_line_of_object_code) <= 69 and
            test_for_hex(unparsed_line_of_object_code[1:]) and
            len(unparsed_line_of_object_code[1:]) % 2 == 0):
        byte_list = []
        byte_object_code = unparsed_line_of_object_code[9:]
        start_index = 0
        end_index = 2

        while end_index <= len(byte_object_code):
            byte_list.append(byte_object_code[start_index:end_index])

            start_index += 2
            end_index += 2

        # Verify that byte count is correct
        byte_count = unparsed_line_of_object_code[7:9]
        if hex_string_to_dec(byte_count) != len(byte_list):
            # ERROR
            raise SICObjectCodeParserError("Invalid text record")

        parsed_line_of_object_code_dict = {"record_type": "text",
                                           "start_address": unparsed_line_of_object_code[3:7],
                                           "byte_count": byte_count,
                                           "byte_list": byte_list,
                                           "unparsed_line_of_object_code": unparsed_line_of_object_code}

        return parsed_line_of_object_code_dict

    else:
        # ERROR
        raise SICObjectCodeParserError("Invalid text record")


# This function parses the end line of object code.
# It stores record type, program start address and unparsed line of code.
# It returns all the items recorded in a line of object code dictionary.
def parse_end_record(unparsed_line_of_object_code):
    # Validate unparsed line of code
    # Make sure the length of the end record is 7 characters
    # Verifies that expected hex characters are hex digits.
    if len(unparsed_line_of_object_code) == 7 and test_for_hex(unparsed_line_of_object_code[1:]):
        parsed_line_of_object_code_dict = {"record_type": "end",
                                           "program_start_address": unparsed_line_of_object_code[3:7],
                                           "unparsed_line_of_code": unparsed_line_of_object_code}

        return parsed_line_of_object_code_dict

    else:
        # ERROR
        raise SICObjectCodeParserError("Invalid End Record")


# This function reads an object code file (*.obj).
# It processes each line of code one at a time
# It parses out all the relevant object code tokens and stores them in a line of object code dictionary.
# It returns a list containing all the parsed line of code dictionaries.
def sic_object_code_parser(object_code_file):
    parsed_object_code_dict_list = []
    header_found = False
    end_found = False

    for line_of_object_code in object_code_file:
        # Remove new line and any other trailing whitespace
        unparsed_line_of_object_code = line_of_object_code.rstrip()
        record_type_indicator = line_of_object_code[0]

        try:
            match record_type_indicator:
                case "H":
                    parsed_object_code_dict_list.append(parse_header_record(unparsed_line_of_object_code))
                case "T":
                    parsed_object_code_dict_list.append(parse_text_record(unparsed_line_of_object_code))
                case "E":
                    parsed_object_code_dict_list.append(parse_end_record(unparsed_line_of_object_code))
                case _:
                    # ERROR
                    raise SICObjectCodeParserError("Invalid record type")

        except SICObjectCodeParserError as ex:
            object_code_file.close()
            # ERROR
            raise SICObjectCodeParserError("Could not parse object code - " + str(ex))

    object_code_file.close()

    return parsed_object_code_dict_list


# TEST BED
# object_code_file_name = "ReadWrite"
#
# object_code_file_path = (SIC_DEFAULT_WORKING_DIRECTORY +
#                          object_code_file_name + "." +
#                          SIC_OBJECT_CODE_FILE_EXTENSION)
#
# object_code_file = open(object_code_file_path, "rt")
#
# parsed_object_code_dict_list = sic_object_code_parser(object_code_file)
#
# for line in parsed_object_code_dict_list:
#     print(line)
