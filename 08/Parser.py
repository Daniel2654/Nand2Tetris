import re
import os
import sys

EMPTY_STRING = ""
NEW_LINE = "\n"

VM_END = ".vm"

C_ARITHMETIC = "c_arithmetic"
C_PUSH = "c_push"
C_POP = "c_pop"
C_LABEL = "c_label"
C_GOTO = "c_goto"
C_IF = "c_if"
C_FUNCTION = "c_function"
C_CALL = "c_call"
C_RETURN = "c_return"

CONSTANT = "constant"
LOCAL = "local"
ARGUMENT = "argument"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"
STATIC = "static"

LOCAL_SYMBOL = "LCL"
ARGUMENT_SYMBOL = "ARG"
THIS_SYMBOL = "THIS"
THAT_SYMBOL = "THAT"
TEMP_SYMBOL = "TEMP"

ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"

# The commands will located in a list from this form [command, arg1, arg2]
ARG_1_LOCATION = 1
ARG_2_LOCATION = 2

COMMAND_TYPE_DICT = {"add": C_ARITHMETIC, "sub": C_ARITHMETIC,
                     "neg": C_ARITHMETIC, "eq": C_ARITHMETIC,
                     "gt": C_ARITHMETIC, "lt": C_ARITHMETIC,
                     "and": C_ARITHMETIC, "or": C_ARITHMETIC,
                     "not": C_ARITHMETIC, "push": C_PUSH,
                     "pop": C_POP, "label": C_LABEL,
                     "goto": C_GOTO, "if-goto": C_IF,
                     "function": C_FUNCTION, "call": C_CALL,
                     "return": C_RETURN
                     }

SEGMENT_SYMBOLS_DICT = {LOCAL: LOCAL_SYMBOL, ARGUMENT: ARGUMENT_SYMBOL, THIS: THIS_SYMBOL, THAT: THAT_SYMBOL,
                        TEMP: TEMP_SYMBOL}


def remove_irrelevant_information(lst):
    """"remove notes ( // xxx... ) and empty lines from list
    :argument: list that each element is an assembly code
    :returns: list that each element is an assembly code without notes and
    empty lines"""
    x = map(lambda string: re.sub(r'(//.*)', EMPTY_STRING, string).rstrip(),
            lst)
    return list(filter(None, x))


class Parser:

    def __init__(self, filepath):
        self.__filepath = filepath
        self.__commands_queue = []
        self.__files_data = []
        # self.__read_files()
        with open(filepath) as vm_program:
            file_data = vm_program.readlines()
            self.__commands_queue = (remove_irrelevant_information(file_data))
        self.__queue_value = 0
        self.__cur_command = []

    def add_single_file(self, file_path):
        with open(file_path) as vm_program:
            file_data = vm_program.readlines()
            self.__commands_queue += (remove_irrelevant_information(file_data))

    def add_dir(self):
        """"translate whole directory that contains vm files and store the
        asm files in the same directory"""
        for file in iter(os.path.abspath(files) for files in os.listdir(self.__filepath)):
            if file.endswith(VM_END):
                self.add_single_file(file)

    def __read_files(self):
        if os.path.isdir(self.__filepath):
            self.add_dir()
        else:
            file_path = os.path.abspath(self.__filepath)
            self.add_single_file(file_path)

    def has_more_commands(self):  # API
        """"Checks if there is more commands on the virtual machine if there is
        return true otherwise return false"""
        if self.__queue_value < len(self.__commands_queue):
            return True
        return False

    def advance(self):  # API
        """"Reads and set the cur command to be the next command in the
        queue """
        self.__cur_command = self.__commands_queue[self.__queue_value].split()
        self.__queue_value += 1

    def command_type(self):  # API
        """""returns a constant representing the type of the current command
         when c_arithmetic is returns for all the arithmetic/logic commands
         :returns: constant representing type of current command
        """
        return COMMAND_TYPE_DICT[self.__cur_command[0]]

    def arg1(self):  # API
        """"returns the first argument of the current command, in case of
        c_arithmetic return the command itself"""
        commend_type = self.command_type()
        if commend_type == C_ARITHMETIC or commend_type == C_RETURN:
            return self.__cur_command[0]
        elif self.__cur_command[ARG_1_LOCATION] in SEGMENT_SYMBOLS_DICT:
            return SEGMENT_SYMBOLS_DICT[self.__cur_command[ARG_1_LOCATION]]
        else:
            return self.__cur_command[ARG_1_LOCATION]

    def arg2(self):  # API
        """"returns the second argument of the current command should be
        called only if the current command is c_push, c_pop, c_function or
        c_call"""
        command_type = self.command_type()
        if self.command_type() != C_ARITHMETIC and self.command_type() != C_RETURN and \
                self.__cur_command[ARG_1_LOCATION] == TEMP:
            return str(int(self.__cur_command[ARG_2_LOCATION]) + 5)
        if command_type != C_ARITHMETIC and command_type != C_LABEL and command_type != C_IF and command_type != \
                C_GOTO and command_type != C_RETURN:
            return self.__cur_command[ARG_2_LOCATION]
        return None


if __name__ == '__main__':
    x = Parser(sys.argv[1])
