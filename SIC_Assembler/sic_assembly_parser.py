import os

from SIC_GUI.Assembler.assembly_status_panel import AssemblyStatusPanel
from SIC_Utilities.sic_constants import COMMENT_LINE_INDICATOR, MINIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_MEMORY_ADDRESS_DEC, \
    OPCODE_VALIDATION_SET, LONE_OPCODE_VALIDATION_SET, MAXIMUM_LENGTH_OF_START_OPERAND, MINIMUM_BYTE_OPERAND_LENGTH, \
    MAXIMUM_BYTE_OPERAND_LENGTH, HEX_DIGIT_SET, MINIMUM_INTEGER, MAXIMUM_INTEGER, MINIMUM_RESB, MAXIMUM_RESB, \
    MINIMUM_RESW, MAXIMUM_RESW, MAXIMUM_LENGTH_OF_OPERAND
from SIC_Utilities.sic_converter import hex_string_to_dec, SICConverterError
from SIC_Utilities.sic_messaging import print_status


class SICAssemblyParserError(Exception):
    pass


# This function tests for a comment line.
# Comment lines are indicated by a "." as the first non-whitespace character.
def test_for_comment_line(line_of_code):
    #
    for character in line_of_code:
        if character == COMMENT_LINE_INDICATOR:
            #
            return True
        elif character.isspace():
            #
            continue
        else:
            #
            return False


# This function tests for the presence of a label in a line of code.
# If a label is present it must begin in the 0 index of the line of code.
def test_for_label(line_of_code):
    return not line_of_code[0].isspace()


# This function tests for the presence of the indexed addressing indicator (",X")
# as the last two characters of an operand.
def test_for_index_addressing(operand):
    return operand[-2:] == ",X"


# This function validates label tokens against defined label rules.
# Labels must contain uppercase and alphanumeric characters.
# The first character must be alphabetical(A-Z).
# Labels must be 1 to 6 characters in length.
def validate_label(label):
    characters_valid = label.isupper() and label.isalnum()
    first_character_valid = label[0].isalpha
    length_valid = 0 < len(label) <= 6

    if characters_valid and first_character_valid and length_valid:
        return label
    else:
        message = "Label is invalid\n"

        if not characters_valid:
            message += "Labels must contain only uppercase alphanumeric characters (A-Z, 0-9)\n"
        if not first_character_valid:
            message += "The first character must be uppercase (A-Z)\n"
        if not length_valid:
            message += "Labels must be 1 to 6 characters in length\n"

        raise SICAssemblyParserError(message)


# This function validates opcode tokens against a set of valid opcodes.
def validate_opcode(opcode):
    if opcode in OPCODE_VALIDATION_SET:
        return opcode
    else:
        raise SICAssemblyParserError("Opcode is invalid\n")


# This function validates opcode tokens against a set of valid opcodes.
def validate_lone_opcode(opcode):
    if opcode in LONE_OPCODE_VALIDATION_SET:
        return opcode
    else:
        raise SICAssemblyParserError("Lone opcode is invalid\n")


# This function validates the operand that follows a START opcode
# Rules:
#    1.) Operand must be a valid memory address hex string
#           No additional decorations should be present
def validate_start_operand(operand):
    error_message = "Start address must be between 0000 and 7FFF."

    if len(operand) > MAXIMUM_LENGTH_OF_START_OPERAND:
        raise SICAssemblyParserError(error_message)

    try:
        dec_value = hex_string_to_dec(operand)
    except SICConverterError:
        raise SICAssemblyParserError(error_message)

    if dec_value < MINIMUM_MEMORY_ADDRESS_DEC or dec_value > MAXIMUM_MEMORY_ADDRESS_DEC:
        raise SICAssemblyParserError(error_message)

    required_leading_zeros = MAXIMUM_LENGTH_OF_START_OPERAND - len(operand)
    return ("0" * required_leading_zeros) + operand


# This function validates the BYTE operand.
# Rules:
#    1.) Operand can be either a hex string or a character string
#    2A.) If operand is a hex string it must be formed as such "X'hhhh...'" (h = valid hex digit string)
#    2B.) The hex digit string must contain an even number of characters and must be 2-32 characters in length.
#    3A.) If operand is a character string it must be formed as such "C'aaaa...'" (a = valid ascii character)
#    3B.) The character string must contain an even number of characters and must be  1-32 characters in length.
def validate_byte_operand(operand):
    if len(operand) < 4:
        raise SICAssemblyParserError("Invalid BYTE OPERAND")

    if operand[1] == "'" and operand[-1] == "'":
        if len(operand[2:-1]) < MINIMUM_BYTE_OPERAND_LENGTH or len(operand[2:-1]) > MAXIMUM_BYTE_OPERAND_LENGTH:
            raise SICAssemblyParserError("OPERAND must have 1-32 characters between the quotation marks.")

        if operand[0] == "X":
            # Handle hex
            hex_digit_string = operand[2:-1]
            if (len(hex_digit_string) % 2) == 0:
                for digit in hex_digit_string:
                    if digit not in HEX_DIGIT_SET:
                        raise SICAssemblyParserError("OPERAND must contain valid hex value.")

                return operand
            else:
                raise SICAssemblyParserError("OPERAND must contain an even number of hex digits.")
        elif operand[0] == "C":
            # Handle characters
            character_string = operand[2:-1]
            if character_string.isascii():
                return operand
            else:
                raise SICAssemblyParserError("OPERAND must contain ascii characters.")
        else:
            raise SICAssemblyParserError("Valid format indicator(C or X) required in OPERAND")
    else:
        raise SICAssemblyParserError("Single quotation marks missing from OPERAND")


# This function validates the WORD operand.
# Rules:
#   1.) Operand can be a decimal integer in the supported SIC architecture range.
#        -8,388,608 to 8,388,607
def validate_word_operand(operand):
    word_value = None
    try:
        word_value = int(operand)
    except ValueError:
        raise SICAssemblyParserError("WORD operand must be a decimal integer.")

    if MINIMUM_INTEGER <= word_value <= MAXIMUM_INTEGER:
        return operand
    else:
        raise SICAssemblyParserError("WORD operand must be in the range of -8,388,608 to 8,388,607")


# This function validates the RESB operand.
# Rules:
# NOTE: this is a very loose restriction. It will not protect against reserving more memory than what is available.
#    1.) Operand must be a positive decimal integer
#    2.) Operand must be less than the number of possible bytes in memory(32,768).
def validate_resb_operand(operand):
    resb_value = None
    try:
        resb_value = int(operand)
    except ValueError:
        raise SICAssemblyParserError("RESB operand must be a positive decimal integer.")

    if MINIMUM_RESB <= resb_value <= MAXIMUM_RESB:
        return operand
    else:
        raise SICAssemblyParserError("RESB operand must be between 0 and 32768")


# This function validates the RESW operand.
# Rules:
# NOTE: this is a very loose restriction. It will not protect against reserving more memory than what is available.
#    1.) Operand must be a positive decimal integer
#    2.) Operand must be less than the number of possible words in memory(10,922).
def validate_resw_operand(operand):
    resw_value = None
    try:
        resw_value = int(operand)
    except ValueError:
        raise SICAssemblyParserError("RESW operand must be a positive decimal integer.")

    if MINIMUM_RESW <= resw_value <= MAXIMUM_RESW:
        return operand
    else:
        raise SICAssemblyParserError("RESW operand must be between 0 and 10,922")


# This function validates the operand for all other opcodes.
# Rules:
#    1.) Operand can be a string that follows label rules (see validate_label() for label rules)
#    2.) Operand can be a valid hex memory address string padded with "0" as the first character.
#           a max of 5 total characters ex. "0hhhh" (h = valid hex value)
#    3.) Each of the above may include the indexed addressing indicator(",X") as the last two characters in the string

def validate_nonspecific_operand(operand):
    # Check for indexed addressing indicator and remove indicator from operand.
    if operand[-2:] == ",X":
        operand = operand[:-2]
    if operand[0].isalpha():
        # Operand will be validated as label.
        characters_valid = operand.isupper() and operand.isalnum()
        length_valid = 0 < len(operand) <= 6
        if characters_valid and length_valid:
            return operand
        else:
            raise SICAssemblyParserError("Operand must be formatted as a label")
    elif operand[0] == "0":
        # Operand will be validated as a hex memory address.
        error_message = "Operand memory address must be between 00000 and 07FFF."

        if len(operand) > MAXIMUM_LENGTH_OF_OPERAND:
            raise SICAssemblyParserError(error_message)

        try:
            dec_value = hex_string_to_dec(operand)
        except SICConverterError:
            raise SICAssemblyParserError(error_message)

        if dec_value < MINIMUM_MEMORY_ADDRESS_DEC or dec_value > MAXIMUM_MEMORY_ADDRESS_DEC:
            raise SICAssemblyParserError(error_message)

        required_leading_zeros = MAXIMUM_LENGTH_OF_OPERAND - len(operand)
        return ("0" * required_leading_zeros) + operand

    else:
        raise SICAssemblyParserError("Operand must be a hex memory address or a label")


# This function validates the operand token.
def validate_operand(operand, opcode):
    opcode = validate_opcode(opcode)

    match opcode:
        case "START":
            return validate_start_operand(operand)
        case "END":
            # END operand is not used.
            # We will ignore it and consider the END opcode the last instruction in the assembly code program.
            pass
        case "BYTE":
            return validate_byte_operand(operand)
        case "WORD":
            return validate_word_operand(operand)
        case "RESB":
            return validate_resb_operand(operand)
        case "RESW":
            return validate_resw_operand(operand)
        case _:
            return validate_nonspecific_operand(operand)


# This function parses and returns a BYTE character string if one exists in the line of code.
# Otherwise, it returns None
def get_byte_character_string(line_of_code):
    byte_character_string = None
    start_index = line_of_code.find("C'")
    if start_index != -1:
        byte_character_string = line_of_code[start_index + 2:]
        end_index = byte_character_string.find("'")
        if end_index != -1:
            byte_character_string = byte_character_string[:end_index]

            byte_character_string = "C'" + byte_character_string + "'"

    return byte_character_string


# This function handles BYTE character strings.
# This special handling is required when there are spaces in the byte character string that would be tokenized.
def handle_byte_character_string(parsed_token_list, byte_character_string):
    parsed_token_list_length = len(parsed_token_list)
    try:
        byte_opcode_index = parsed_token_list.index("BYTE")

        if byte_opcode_index == 0 and parsed_token_list_length >= 2:
            exists_index = parsed_token_list[byte_opcode_index + 1].find("C'")
            if exists_index != -1:
                parsed_token_list = [parsed_token_list[0], byte_character_string]

        elif byte_opcode_index == 1 and parsed_token_list_length >= 3:
            exists_index = parsed_token_list[byte_opcode_index + 1].find("C'")
            if exists_index != -1:
                parsed_token_list = [parsed_token_list[0], parsed_token_list[1], byte_character_string]
    except ValueError:
        pass

    return parsed_token_list


# This function opens and reads an assembly code file (*.asm).
# It processes each line of code one at a time
# It parses out all the relevant assembly code tokens and stores them in a line of code dictionary.
# It returns a list containing all the parsed line of code dictionaries.
def parse_assembly_code_file(assembly_code_file_path, assembly_status_panel: AssemblyStatusPanel):
    # STATUS
    status_message = "Beginning parsing\n" + assembly_code_file_path
    print_status(status_message)
    assembly_status_panel.set_assembly_status(status_message + "\n")
    # Check to see if assembly_code_file exists
    # Open the file if it does exist
    if os.path.exists(assembly_code_file_path):
        assembly_code_file = open(assembly_code_file_path, "rt")

        # This list will hold the dictionaries that represent a parsed line of assembly code.
        parsed_code_dict_list = []

        line_of_code_number = 0

        start_found = False
        end_found = False

        for line_of_code in assembly_code_file:
            line_of_code_number += 1

            # Create parsed_code_dict and record line number
            parsed_code_dict = {"line_number": line_of_code_number}

            # Line is not a comment, so record raw line of code.
            unparsed_line_of_code = line_of_code

            # Check for empty line in assembly code file.
            if line_of_code.isspace():
                # Close assembly file, print error message, and exit program.
                assembly_code_file.close()
                # ERROR
                raise SICAssemblyParserError("Parser Error: Line is blank. Line must contain code or comment" + "\n" +
                                             "LINE" + str(line_of_code_number) +
                                             ": " + unparsed_line_of_code)

            # Determine if line of code is a comment line
            is_comment_line = test_for_comment_line(line_of_code)
            if is_comment_line:
                # DEBUG: Print the parsed code dictionary for this line of code
                # print(parsed_code_dict)
                # No processing of this line necessary.
                continue

            # Determine if line contains a LABEL
            has_label = test_for_label(line_of_code)

            # Handle BYTE character strings,
            # Parse out expected code tokens and count the amount of tokens
            byte_character_string = get_byte_character_string(line_of_code)
            parsed_token_list = line_of_code.split()
            if byte_character_string is not None:
                parsed_token_list = handle_byte_character_string(parsed_token_list, byte_character_string)
            number_of_parsed_tokens = len(parsed_token_list)

            # Initialize all indexed_addressing flags to False
            # Will be changed to True only when ",X" is present at the end of the operand
            parsed_code_dict["indexed_addressing"] = False

            try:
                if has_label and number_of_parsed_tokens >= 3:
                    parsed_code_dict["label"] = validate_label(parsed_token_list[0])
                    parsed_code_dict["opcode"] = validate_opcode(parsed_token_list[1])
                    if (parsed_code_dict["opcode"] != "RSUB" and parsed_code_dict["opcode"] != "END"
                            and parsed_code_dict["opcode"] != "XOS"):
                        parsed_code_dict["operand"] = validate_operand(parsed_token_list[2], parsed_token_list[1])
                        parsed_code_dict["indexed_addressing"] = test_for_index_addressing(parsed_token_list[2])
                elif has_label and number_of_parsed_tokens >= 2:
                    parsed_code_dict["label"] = validate_label(parsed_token_list[0])
                    parsed_code_dict["opcode"] = validate_opcode(parsed_token_list[1])
                elif not has_label and number_of_parsed_tokens >= 2:
                    parsed_code_dict["opcode"] = validate_opcode(parsed_token_list[0])
                    if (parsed_code_dict["opcode"] != "RSUB" and parsed_code_dict["opcode"] != "END"
                            and parsed_code_dict["opcode"] != "XOS"):
                        parsed_code_dict["operand"] = validate_operand(parsed_token_list[1], parsed_token_list[0])
                        parsed_code_dict["indexed_addressing"] = test_for_index_addressing(parsed_token_list[1])
                elif not has_label and number_of_parsed_tokens == 1:
                    parsed_code_dict["opcode"] = validate_lone_opcode(parsed_token_list[0])
                else:
                    raise SICAssemblyParserError("Line of code cannot be parsed")

            except SICAssemblyParserError as ex:
                # Close assembly file, print error message, and exit program.
                assembly_code_file.close()
                # ERROR
                raise SICAssemblyParserError("Parser Error: " + str(ex) + "\n" +
                                             "LINE " + str(line_of_code_number) +
                                             ": " + unparsed_line_of_code)

            parsed_code_dict["comment"] = False

            # Make sure START assembly directive is the first opcode in the assembly program.
            if not start_found:
                if parsed_code_dict["opcode"] == "START":
                    start_found = True
                else:
                    # Close assembly file, print error message, and exit program.
                    assembly_code_file.close()
                    # ERROR
                    raise SICAssemblyParserError("Parser Error: START must be the first opcode called in assembly "
                                                 + "program\n" +
                                                 "LINE " + str(line_of_code_number) +
                                                 ": " + unparsed_line_of_code)

            parsed_code_dict["unparsed_line_of_code"] = unparsed_line_of_code

            parsed_code_dict_list.append(parsed_code_dict)

            # No further processing required after END found
            if parsed_code_dict["opcode"] == "END":
                end_found = True
                break

            # DEBUG: Print the parsed code dictionary for this line of code
            # print(parsed_code_dict)

        assembly_code_file.close()

        # Make sure the program includes an END assembly directive
        if end_found:
            # STATUS
            status_message = "Parsing complete"
            print_status("Parsing complete")
            assembly_status_panel.set_assembly_status(status_message + "\n")
        else:
            # if END assembly directive is not found, then assembly code is invalid and error is raised.
            assembly_code_file.close()
            # ERROR
            raise SICAssemblyParserError("Parser Error: No END assembly directive found.")

        # Return list of parsed code dictionaries and status
        return parsed_code_dict_list

    else:
        # ERROR
        raise SICAssemblyParserError("SIC assembly code file does not exist." + "\n" + assembly_code_file_path)

# TEST BED
# Create path to assembly code file
# NOTE: This is just temporary.
# File should be indicated at run time.
# assembly_code_file_name = "ReadWrite.asm"
# assembly_code_file_name = "ReadWriteTest01.asm"
# assembly_code_file_name = "ReadWriteTest02.asm"
# assembly_code_file_path = (
#         "/Users/nickjackson012/Desktop/Pycharm Projects/SIC_System_Software/Assembly Code/" + assembly_code_file_name)
#
# parsed_code_dict_list = parse_assembly_code_file(assembly_code_file_path)
#
# for line in parsed_code_dict_list:
#     print(line)
