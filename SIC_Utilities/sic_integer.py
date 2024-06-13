# class SICConvert
from SIC_Utilities.sic_constants import NUMBER_OF_BITS_IN_A_INTEGER, MINIMUM_INTEGER, MAXIMUM_INTEGER, HEX_TO_BIN_DICT, \
    BIN_TO_HEX_DICT


class SICIntegerError(Exception):
    pass


def bin_string_to_dec(bin_value_string: str):
    # Confirm bin_value is a string
    # Confirm bin_value is the proper length
    # Confirm bin_value represents a binary number
    # Confirm bin_value comprised of 1's and 0's
    if ((not isinstance(bin_value_string, str)) or
            (len(bin_value_string) != NUMBER_OF_BITS_IN_A_INTEGER) or
            (bin_value_string.count("0") + bin_value_string.count("1") != NUMBER_OF_BITS_IN_A_INTEGER)):
        raise SICIntegerError("Invalid binary value string")
    # Convert bin_value_string to a list
    binary_digit_list = []
    for binary_digit in bin_value_string:
        binary_digit_list.append(int(binary_digit))

    # Determine if bin_value_string is negative
    is_negative = False
    if binary_digit_list[0] == 1:
        is_negative = True
        # Reverse 2's compliment
        # Subtract 1 from bin_value_string
        for index in reversed(range(NUMBER_OF_BITS_IN_A_INTEGER)):
            match binary_digit_list[index]:
                case 0:
                    binary_digit_list[index] = 1
                case 1:
                    binary_digit_list[index] = 0
                    break

        for index in range(NUMBER_OF_BITS_IN_A_INTEGER):
            if binary_digit_list[index] == 0:
                binary_digit_list[index] = 1
            else:
                binary_digit_list[index] = 0
    # Convert binary value to decimal value
    reversed_binary_digit_list = list(reversed(binary_digit_list))
    dec_value = 0
    for index in range(NUMBER_OF_BITS_IN_A_INTEGER):
        dec_value += reversed_binary_digit_list[index] * 2 ** index

    # Convert to negative if necessary
    if is_negative:
        dec_value *= -1

    return dec_value


# Test Bed


# try:
#     dec_value1 = bin_string_to_dec("101010101010101010101010")
#     print("dec_value1:", dec_value1)
#     dec_value2 = bin_string_to_dec("000000000000000010101010")
#     print("dec_value2:", dec_value2)
#     dec_value3 = bin_string_to_dec("101011101010101010101011")
#     print("dec_value3:", dec_value3)
#     dec_value4 = bin_string_to_dec("01010101010101010101010")
#     print("dec_value4:", dec_value4)
#     dec_value5 = bin_string_to_dec("101010101010101111010101010")
#     print("dec_value5:", dec_value5)
#
# except SICIntegerError:
#     print("Invalid Value")


# Exceptions: ValueError, IntegerOutOfRangeError

def dec_to_bin_string(dec_value: int):
    # Check for invalid input
    # Make sure dec_value is an integer
    if not isinstance(dec_value, int):
        raise SICIntegerError("Cannot convert non-integer value passed to dec_to_bin_string function.")

    # Make sure dec_value is in supported range of integers
    if not MINIMUM_INTEGER <= dec_value <= MAXIMUM_INTEGER:
        raise SICIntegerError("Integer out of range.")

    is_negative = False
    if dec_value < 0:
        is_negative = True
        dec_value = abs(dec_value)

    # Convert decimal value to binary
    binary_digit_list = []
    quotient = dec_value
    while quotient != 0:
        remainder = quotient % 2
        binary_digit_list.insert(0, remainder)
        quotient = quotient // 2

    # Pad Binary Number with Zeros
    while len(binary_digit_list) < NUMBER_OF_BITS_IN_A_INTEGER:
        binary_digit_list.insert(0, 0)

    # Check to see if 2's complement is necessary
    if is_negative:
        # Convert to 2's Complement
        # Step 1: Flip all the bits
        for index in range(NUMBER_OF_BITS_IN_A_INTEGER):
            if binary_digit_list[index] == 0:
                binary_digit_list[index] = 1
            else:
                binary_digit_list[index] = 0

        # Step 2: Add 1
        for index in reversed(range(NUMBER_OF_BITS_IN_A_INTEGER)):
            match binary_digit_list[index]:
                case 0:
                    binary_digit_list[index] = 1
                    break
                case 1:
                    binary_digit_list[index] = 0

    # Step 3: Convert binary_digit_list to a string
    binary_number_string = ""
    for binary_digit in binary_digit_list:
        binary_number_string += str(binary_digit)

    return binary_number_string


def hex_to_bin(hex_string):
    bin_string = ""
    # Register holds 24 bits
    # range(start, stop, step)
    for hex_digit in hex_string:
        bin_string += HEX_TO_BIN_DICT[hex_digit]
    return bin_string


def bin_to_hex(bin_string):
    hex_string = ""
    # Register holds 24 bits
    # range(start, stop, step)
    for index in range(0, 24, 4):
        hex_string += BIN_TO_HEX_DICT[bin_string[index:index + 4]]
    return hex_string


def hex_string_to_dec(hex_string: str):
    bin_string = hex_to_bin(hex_string)

    return bin_string_to_dec(bin_string)


def dec_to_hex_string(dec_value: int):
    bin_string = dec_to_bin_string(dec_value)

    return bin_to_hex(bin_string)

# Test Bed
# try:
#     binary_value1 = dec_to_bin_string(-5592406)
#     print("binary_value1", binary_value1)
#     binary_value2 = dec_to_bin_string(170)
#     print("binary_value2", binary_value2)
#     binary_value3 = dec_to_bin_string(-5330261)
#     print("binary_value3", binary_value3)
#
# except SICIntegerError:
#     print("Invalid Value")
