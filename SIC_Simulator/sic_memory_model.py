from SIC_Utilities.sic_constants import BYTES_IN_MEMORY, INITIALIZATION_CHARACTER, MINIMUM_MEMORY_ADDRESS_DEC, \
    MAXIMUM_MEMORY_ADDRESS_DEC
from SIC_Utilities.sic_converter import dec_to_memory_address_hex_string


class SICMemoryModelError(Exception):
    pass


class SICMemoryModel:
    SMALL_SEPARATOR = " "  # 1 space
    LARGE_SEPARATOR = "   "  # 3 spaces
    BYTES_PER_ROW = 16
    BYTES_PER_GROUP = 4
    ROWS_IN_MEMORY_DUMP = BYTES_IN_MEMORY // BYTES_PER_ROW

    def __init__(self):
        self.memory_model_dict = self.initialize_memory()

    def test_for_dec_memory_address_in_range(self, memory_address_dec_value: int):
        is_in_memory_address_range = False

        if MINIMUM_MEMORY_ADDRESS_DEC <= memory_address_dec_value <= MAXIMUM_MEMORY_ADDRESS_DEC:
            is_in_memory_address_range = True
        else:
            # NOTE: Raise exception?
            pass
        return is_in_memory_address_range

    def get_byte(self, memory_address_dec_value: int):
        if not self.test_for_dec_memory_address_in_range(memory_address_dec_value):
            raise SICMemoryModelError("Memory address out of range.")

        byte_string = self.memory_model_dict[memory_address_dec_value]
        # Replace the initialization characters("-") encountered with "F".
        byte_string = byte_string.replace(INITIALIZATION_CHARACTER, "F")

        return byte_string

    def get_bytes(self, memory_address_dec_value: int, number_of_bytes: int):
        byte_string = ""
        index = 0

        # Concatenate requested byte string
        while index < number_of_bytes:
            if not self.test_for_dec_memory_address_in_range(memory_address_dec_value + index):
                raise SICMemoryModelError("Memory address out of range.")
            byte_string += self.memory_model_dict[memory_address_dec_value + index]
            index += 1
        # Replace the initialization characters("-") encountered with "F".
        byte_string = byte_string.replace(INITIALIZATION_CHARACTER, "F")

        return byte_string

    def set_byte(self, memory_address_dec_value: int, byte_string: str):
        if not self.test_for_dec_memory_address_in_range(memory_address_dec_value):
            raise SICMemoryModelError("Memory address out of range.")

        self.memory_model_dict[memory_address_dec_value] = byte_string

    def initialize_memory(self):
        # Create an empty dictionary to model memory
        # Load dictionary with empty bytes
        self.memory_model_dict = {}
        for byte_address_dec in range(BYTES_IN_MEMORY):
            self.memory_model_dict[byte_address_dec] = INITIALIZATION_CHARACTER * 2

        return self.memory_model_dict

    def dump_memory(self):
        memory_dump_string = ""
        # rows 0 through 2048 (32767 / 16)
        for row in range(self.ROWS_IN_MEMORY_DUMP):
            # Row Format:
            # ADDR   Memory Contents
            # XXXX   -- -- -- --   -- -- -- --   -- -- -- --   -- -- -- --

            # Create memory_row_string and initialize it with a byte address as a 4 digit hex value
            memory_row_string = dec_to_memory_address_hex_string(row * self.BYTES_PER_ROW)
            # 0 through 15
            for byte_column in range(self.BYTES_PER_ROW):
                # calculate byte address
                byte_address_dec = row * self.BYTES_PER_ROW + byte_column

                if byte_address_dec % self.BYTES_PER_GROUP == 0:
                    memory_row_string += self.LARGE_SEPARATOR + self.memory_model_dict[byte_address_dec]
                else:
                    memory_row_string += self.SMALL_SEPARATOR + self.memory_model_dict[byte_address_dec]

            # print(memory_row_string)
            memory_dump_string += memory_row_string + "\n"

        return memory_dump_string


MEMORY_MODEL = SICMemoryModel()

# test bed
# memory_model_dict = initialize_memory()
#
# dump_memory(memory_model_dict)
