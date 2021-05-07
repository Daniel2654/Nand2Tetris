import re
import os

R_DICT = {"R" + str(i): str(i) for i in range(16)}  # allocate i memory to R[i]
SPECIAL_LABELS_DICT = {"SP": "0", "LCL": "1", "ARG": "2", "THIS": "3",
                       "THAT": "4", "SCREEN": "16384", "KBD": "24576"}

# Dicts of asm commend and their translation to binary
DEST_DICT = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100",
             "AM": "101", "AD": "110", "AMD": "111"}
JUMP_DICT = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
             "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
# Comp dict including a (7 bits)
COMP_DICT = {"0": "0101010", "1": "0111111", "-1": "0111010",
             "D": "0001100", "A": "0110000", "!D": "0001101",
             "!A": "0110001", "-D": "0001111", "-A": "0110011",
             "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
             "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
             "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
             "M": "1110000", "!M": "1110001", "-M": "1110011",
             "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
             "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
             "D|M": "1010101"}

READ = "r"
WRITE = "w"
A_INSTRUCTION = "@"
LABEL = "("
EMPTY_STRING = ""
NEW_LINE = "\n"

HDL_FILE = "{}.hack"  # HDL file syntax
ASM_END = '.asm'

# What appears after what, for example destination appears after = sign
COMP = ""
DEST = "="
JUMP = ";"

NULL = "null"
D = {COMP: 0, DEST: 1, JUMP: 2}
C_INSTRUCTION_DICTS = {0: COMP_DICT, 1: DEST_DICT, 2: JUMP_DICT}

FIRST_VARIABLE_INDEX = 16  # The first memory location of variables
BITS_IN_BINARY_NUMBER = 16

C_COMMAND_PREFIX = "111"  # Each C commend starts with "111"


def read_file(filename):
    """reads file data
    :argument: name of the file
    :returns: each line of the file in a list"""
    with open(filename, READ) as file:
        return file.read().splitlines()


def remove_non_relevant_information(lst):
    """"remove notes ( // xxx... ) and empty lines from list
    :argument: list that each element is an assembly code
    :returns: list that each element is an asssembly code without notes and
    empty lines"""
    x = map(lambda string: re.sub(r'(//.*)|(\s)', EMPTY_STRING, string), lst)
    return list(filter(None, x))


def dec_to_binary(decimal):
    """convert decimal number to 16 bits binary number
    :argument: decimal number
    :returns: 16 bits binary number in string"""
    binary = bin(int(decimal))[2:]
    while len(binary) != BITS_IN_BINARY_NUMBER:
        binary = "0" + binary
    return binary


class Assembler:
    """"An assembler object gets a file name that name of assembly file and
    translate it when using the translate method"""

    def __init__(self, filepath, filename):
        """"constructor of the assembler the constructor the following
        properties
        filename - the name of the assembly file
        file_data - list that each element is an assembly command
        symbol_table - table of all the symbols
        variable_counter - counts how many variable the program has
        binary_instructon - string that contain the binary instructions
        translate from the assembly commands"""
        self.__filepath = filepath
        self.__filename = filename
        self.__file_data = remove_non_relevant_information(read_file(filepath))
        self.__symbol_table = {**R_DICT, **SPECIAL_LABELS_DICT}
        self.__variable_counter = FIRST_VARIABLE_INDEX
        self.__binary_instructions = EMPTY_STRING

    def __table_adder(self, key):
        """"Add to the table variables and their address if they are not
        already exists """
        if key not in self.__symbol_table and not key.isdecimal():
            self.__symbol_table[key] = self.__variable_counter
            self.__variable_counter += 1

    def __add_labels(self):
        """"Scan the assembly program and add to table labels address"""
        label_counter = 0
        for line_num, line in enumerate(self.__file_data):
            if line[0] == LABEL:
                label_name = re.sub(r'(\()|(\))', EMPTY_STRING, line)
                self.__symbol_table[label_name] = line_num - label_counter
                label_counter += 1

    def __translate_a_instruction(self, command):
        """"translate a instruction and write it into the the output file"""
        self.__table_adder(command)
        # check if the command is variable or digit
        if command.isdigit():
            binary_code = dec_to_binary(command)
        else:
            binary_code = dec_to_binary(self.__symbol_table[command])

        self.__binary_instructions += binary_code + NEW_LINE
        # self.__output_file.write(binary_code + NEW_LINE)

    def __translate_c_instruction(self, line):
        """""translate c instruction and write it into the output file"""
        # Because not all of the instructions are mandatory some symbols
        # may not appear so we'll add them manually and the for sure we'll have
        # expression dest = comp ; jump even if one of them is empty that okay
        if DEST not in line:
            line = DEST + line
        if JUMP not in line:
            line += JUMP

        # create list that contains [COMP, DEST, JUMP]
        lst = re.split(r';|=', line)
        # replace empty string with null
        lst = [data if data else NULL for data in lst]
        lst[0], lst[1] = lst[1], lst[0]  # Switch between comp and dest

        binary_code = C_COMMAND_PREFIX
        for i in range(len(lst)):
            binary_code += C_INSTRUCTION_DICTS[i][lst[i]]

        self.__binary_instructions += binary_code + NEW_LINE
        # self.__output_file.write(binary_code + NEW_LINE)

    def __translate_instructions(self):
        """"starts the translating process for each line in the file check
        if its an A instruction or C instruction and translate it"""
        # check the type of the instruction (A instruction starts with @)
        for line in self.__file_data:
            if line[0] == A_INSTRUCTION:
                self.__translate_a_instruction(line[1:])
            elif line[0] != LABEL:
                self.__translate_c_instruction(line)

    def export_output(self):
        """export the output into hdl file"""
        output_filename = HDL_FILE.format(re.sub(r'\.asm', EMPTY_STRING,
                                                  self.__filename))

        output_path = os.path.dirname(self.__filepath) + '/' + output_filename

        with open(output_path, WRITE) as output_file:
            output_file.write(self.__binary_instructions)

    def translate(self):
        """"start the translating process"""
        self.__add_labels()
        self.__translate_instructions()


