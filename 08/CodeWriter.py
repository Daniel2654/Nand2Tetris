from Parser import *

ASM_FILE = "{}.asm"  # asm file syntax
SYS_INIT = "Sys.init"
EMPTY_STRING = ""
WRITE = "w"

NEW_LINE = "\n"
TAB = "\t"

THIS_NUM = '0'
THAT_NUM = '1'

SYS_VAL = '0'

# x + y
ADD_ASM = "// add x + y" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "AM=M-1" + NEW_LINE + \
          "D=M" + NEW_LINE + \
          "A=A-1" + NEW_LINE + \
          "M=D+M" + NEW_LINE
# x - y
SUB_ASM = "// sub x - y" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "AM=M-1" + NEW_LINE + \
          "D=-M" + NEW_LINE + \
          "A=A-1" + NEW_LINE + \
          "M=D+M" + NEW_LINE
# -y
NEG_ASM = "// neg -y" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "A=M-1" + NEW_LINE + \
          "M=-M" + NEW_LINE

# true if x == y false other wise
EQ_ASM = "// true if x = y, false otherwise" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "A=A-1" + NEW_LINE + \
         "D=D-M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JNE" + NEW_LINE + \
         "(TRUE{i})" + NEW_LINE + \
         TAB + "@SP" + NEW_LINE + \
         TAB + "A=M-1" + NEW_LINE + \
         TAB + "M=-1" + NEW_LINE + \
         TAB + "@DONE{i}" + NEW_LINE + \
         TAB + "0;JMP" + NEW_LINE + \
         "(FALSE{i})" + NEW_LINE + \
         TAB + "@SP" + NEW_LINE + \
         TAB + "A=M-1" + NEW_LINE + \
         TAB + "M=0" + NEW_LINE + \
         "(DONE{i})" + NEW_LINE

GT_ASM = "// true if x > y false otherwise" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@GT{i}" + NEW_LINE + \
         "D;JGT" + NEW_LINE + \
         "@LT{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(GT{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@TRUE{i}" + NEW_LINE + \
         "D;JLT" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M+1" + NEW_LINE + \
         "D=D-M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JGT" + NEW_LINE + \
         "@TRUE{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(LT{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JGE" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M+1" + NEW_LINE + \
         "D=D-M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JGE" + NEW_LINE + \
         "@TRUE{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(FALSE{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "M=-1" + NEW_LINE + \
         "@DONE{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(TRUE{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "M=0" + NEW_LINE + \
         "(DONE{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "M=M+1" + NEW_LINE

AND_ASM = "// x and y" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "AM=M-1" + NEW_LINE + \
          "D=M" + NEW_LINE + \
          "A=A-1" + NEW_LINE + \
          "M=D&M" + NEW_LINE

OR_ASM = "// x or y" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "A=A-1" + NEW_LINE + \
         "M=D|M" + NEW_LINE

NOT_ASM = "// not y" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "A=M-1" + NEW_LINE + \
          "M=!M" + NEW_LINE

LT_ASM = "// true if x < y false otherwise" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@GT{i}" + NEW_LINE + \
         "D;JGT" + NEW_LINE + \
         "@LT{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(GT{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@TRUE{i}" + NEW_LINE + \
         "D;JLE" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M+1" + NEW_LINE + \
         "D=D-M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JGE" + NEW_LINE + \
         "@TRUE{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(LT{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "AM=M-1" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JGE" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M+1" + NEW_LINE + \
         "D=D-M" + NEW_LINE + \
         "@FALSE{i}" + NEW_LINE + \
         "D;JGE" + NEW_LINE + \
         "@TRUE{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(TRUE{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "M=-1" + NEW_LINE + \
         "@DONE{i}" + NEW_LINE + \
         "0;JMP" + NEW_LINE + \
         "(FALSE{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "M=0" + NEW_LINE + \
         "(DONE{i})" + NEW_LINE + \
         "@SP" + NEW_LINE + \
         "M=M+1" + NEW_LINE

# push command for constant
PUSH_CONST_ASM = "// push const {index}" + NEW_LINE + \
                 "@{index}" + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1" + NEW_LINE + \
                 "A=M-1" + NEW_LINE + \
                 "M=D" + NEW_LINE

# push / pop commands for LCL, ARG, THIS, THAT
PUSH_ASM = "//push {segment} {index}" + NEW_LINE + \
           "@{segment}" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@{index}" + NEW_LINE + \
           "A=D+A" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1" + NEW_LINE + \
           "A=M-1" + NEW_LINE + \
           "M=D" + NEW_LINE

POP_ASM = "// pop {segment} {index}" + NEW_LINE + \
          "@{segment}" + NEW_LINE + \
          "D=M" + NEW_LINE + \
          "@{index}" + NEW_LINE + \
          "D=D+A" + NEW_LINE + \
          "@R13" + NEW_LINE + \
          "M=D" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "AM=M-1" + NEW_LINE + \
          "D=M" + NEW_LINE + \
          "@R13" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=D" + NEW_LINE

# maybe switch between them
PUSH_STATIC_ASM = "// push static {index}" + NEW_LINE + \
                  "@{filename}.{index}" + NEW_LINE + \
                  "D=M" + NEW_LINE + \
                  "@SP" + NEW_LINE + \
                  "AM=M+1" + NEW_LINE + \
                  "A=A-1" + NEW_LINE + \
                  "M=D" + NEW_LINE

POP_STATIC_ASM = "// pop static {index}" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "AM=M-1" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@{filename}.{index}" + NEW_LINE + \
                 "M=D" + NEW_LINE

PUSH_POINTER_ASM = "// push pointer {index}" + NEW_LINE + \
                   "@{segment}" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "AM=M+1" + NEW_LINE + \
                   "A=A-1" + NEW_LINE + \
                   "M=D" + NEW_LINE

POP_POINTER_ASM = "// pop pointer {index}" + NEW_LINE + \
                  "@SP" + NEW_LINE + \
                  "AM=M-1" + NEW_LINE + \
                  "D=M" + NEW_LINE + \
                  "@{segment}" + NEW_LINE + \
                  "M=D" + NEW_LINE

# check where i starts LATER
PUSH_TEMP_ASM = "// push temp {index}" + NEW_LINE + \
                "@{index}" + NEW_LINE + \
                "D=M" + NEW_LINE + \
                "@SP" + NEW_LINE + \
                "M=M+1" + NEW_LINE + \
                "A=M-1" + NEW_LINE + \
                "M=D" + NEW_LINE

# pop to temp (need to add 5 to the index manually)
POP_TEMP_ASM = "// pop temp {index}" + NEW_LINE + \
               "@SP" + NEW_LINE + \
               "AM=M-1" + NEW_LINE + \
               "D=M" + NEW_LINE + \
               "@{index}" + NEW_LINE + \
               "M=D" + NEW_LINE

LABEL = "({func_name}${label})" + NEW_LINE

IF_GOTO_ASM = "// if-goto {func_name}${label}" + NEW_LINE + \
              "@SP" + NEW_LINE + \
              "AM=M-1" + NEW_LINE + \
              "D=M" + NEW_LINE + \
              "@{func_name}${label}" + NEW_LINE + \
              "D;JNE" + NEW_LINE

GOTO_ASM = "// goto {func_name}${label}" + NEW_LINE + \
           "@{func_name}${label}" + NEW_LINE + \
           "0;JMP" + NEW_LINE

CALL_ASM = "// call {func_name} {num_vars}" + NEW_LINE + \
           "@{func_name}$ret.{index}" + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "AM=M+1" + NEW_LINE + \
           "A=A-1" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@LCL" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "AM=M+1" + NEW_LINE + \
           "A=A-1" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@ARG" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "AM=M+1" + NEW_LINE + \
           "A=A-1" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@THIS" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "AM=M+1" + NEW_LINE + \
           "A=A-1" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@THAT" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "AM=M+1" + NEW_LINE + \
           "A=A-1" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@{n_vars_plus5}" + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "D=M-D" + NEW_LINE + \
           "@ARG" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@LCL" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@{func_name}" + NEW_LINE + \
           "0;JMP" + NEW_LINE + \
           "({func_name}$ret.{index})" + NEW_LINE

FUNCTION_PREFIX = "// function {func_name} {num}" + NEW_LINE + \
                  "({func_name})" + NEW_LINE

PUSH_FUNCTION_LCL = "@0" + NEW_LINE + \
                    "D=A" + NEW_LINE + \
                    "@SP" + NEW_LINE + \
                    "M=M+1" + NEW_LINE + \
                    "A=M-1" + NEW_LINE + \
                    "M=D" + NEW_LINE

RETURN_ASM = "// return" + NEW_LINE + \
             "@LCL" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@5" + NEW_LINE + \
             "A=D-A" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@R14" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@LCL" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@R13" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@SP" + NEW_LINE + \
             "A=M-1" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@ARG" + NEW_LINE + \
             "A=M" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "D=A+1" + NEW_LINE + \
             "@SP" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@R13" + NEW_LINE + \
             "AM=M-1" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@THAT" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@R13" + NEW_LINE + \
             "AM=M-1" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@THIS" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@R13" + NEW_LINE + \
             "AM=M-1" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@ARG" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@R13" + NEW_LINE + \
             "AM=M-1" + NEW_LINE + \
             "D=M" + NEW_LINE + \
             "@LCL" + NEW_LINE + \
             "M=D" + NEW_LINE + \
             "@R14" + NEW_LINE + \
             "A=M" + NEW_LINE + \
             "0;JMP" + NEW_LINE

BOOT_STRAP = "@256" + NEW_LINE + \
             "D=A" + NEW_LINE + \
             "@SP" + NEW_LINE + \
             "M=D" + NEW_LINE

PUSH_SEGMENT_DICT = {CONSTANT: PUSH_CONST_ASM, LOCAL_SYMBOL: PUSH_ASM, ARGUMENT_SYMBOL: PUSH_ASM, THIS_SYMBOL: PUSH_ASM,
                     THAT_SYMBOL: PUSH_ASM,
                     POINTER: PUSH_POINTER_ASM, STATIC: PUSH_STATIC_ASM, TEMP_SYMBOL: PUSH_TEMP_ASM}

POP_SEGMENT_DICT = {LOCAL_SYMBOL: POP_ASM, ARGUMENT_SYMBOL: POP_ASM, THIS_SYMBOL: POP_ASM, THAT_SYMBOL: POP_ASM,
                    POINTER: POP_POINTER_ASM,
                    STATIC: POP_STATIC_ASM, TEMP_SYMBOL: POP_TEMP_ASM}

ARITHMETIC_DICT = {ADD: ADD_ASM, SUB: SUB_ASM, NEG: NEG_ASM, EQ: EQ_ASM, GT: GT_ASM, LT: LT_ASM, AND: AND_ASM,
                   OR: OR_ASM, NOT: NOT_ASM}


class CodeWriter:
    """"A code runner that translate a single vm file into assembly commands"""

    def __init__(self, filename, parser, index):
        """"Constructor of CodeWriter
        :param: __output_file_name - the name of the output file
        :param: __assembly_commands - the assembly commands that the CodeWriter translated
        :param: __parser - a parser object
        :param  __index - to avoid duplicate of labels each true of false label will have a unique index"""

        self.__output_file_name = re.sub(r'\.vm', EMPTY_STRING, os.path.basename(filename))
        self.__file_name = filename
        self.__assembly_commands = EMPTY_STRING
        self.__parser = parser
        self.__cur_label_index = index
        self.__cur_func = None

    def __add__(self, other):
        """" add two CodeWriters means add their assembly commands
        :param other: another CodeWriter object
        :returns code writer that that has two vm files assembly commands"""
        if type(other) != CodeWriter:
            raise TypeError
        self.__assembly_commands += other.__assembly_commands
        return self

    def get_cur_index(self):
        return self.__cur_label_index

    def write_arithmetic(self, command, index=None):
        """"writes to the output file the assembly code that implements the
        give arithmetic command"""
        command = ARITHMETIC_DICT[command]
        self.__assembly_commands += (command.format(i=self.__cur_label_index))
        # self.__output_file.write(command.format(i=self.__cur_arithmetic))
        self.__cur_label_index += 1

    def __write_push(self, segment, index):
        """"writes push command for segments LCL, ARG, THIS, THAT"""
        self.__assembly_commands += PUSH_SEGMENT_DICT[segment].format(segment=segment, index=index)

    def __write_pop(self, segment, index):
        """"writes pop command for segments LCL, ARG, THIS, THAT"""
        self.__assembly_commands += POP_SEGMENT_DICT[segment].format(segment=segment, index=index)

    def __write_push_pointer(self, segment, index):
        """"writes push command for pointer"""
        self.__assembly_commands += PUSH_POINTER_ASM.format(segment=segment, index=index)

    def __write_pop_pointer(self, segment, index):
        """"writes pop command for pointer"""
        self.__assembly_commands += POP_POINTER_ASM.format(segment=segment, index=index)

    def __write_push_static(self, index):
        """"writes push command for static"""

        self.__assembly_commands += PUSH_STATIC_ASM.format(filename=self.__output_file_name, index=index)

    def __write_pop_static(self, index):
        """"writes pop command for static"""

        self.__assembly_commands += POP_STATIC_ASM.format(filename=self.__output_file_name, index=index)

    def __write_static(self):
        """"gets a static command and determine if its pop or push command, and writes the command"""

        index = self.__parser.arg2()
        if self.__parser.command_type() == C_POP:
            self.__write_pop_static(index)
        elif self.__parser.command_type() == C_PUSH:
            self.__write_push_static(index)

    def __write_pointer(self):
        """"gets a pointer command and determine if its that or this command, and if it a push or a pop command and
        writes the command"""

        if self.__parser.arg2() == THIS_NUM:
            segment = THIS_SYMBOL
        elif self.__parser.arg2() == THAT_NUM:
            segment = THAT_SYMBOL
        if self.__parser.command_type() == C_POP:
            self.__write_pop_pointer(segment, self.__parser.arg2())
        elif self.__parser.command_type() == C_PUSH:
            self.__write_push_pointer(segment, self.__parser.arg2())

    def __write_label(self, label, index=None):
        self.__assembly_commands += LABEL.format(func_name=self.__cur_func, label=label)

    def __write_goto(self, label, index=None):
        self.__assembly_commands += GOTO_ASM.format(func_name=self.__cur_func, label=label)

    def __write_if_goto(self, label, index=None):
        self.__assembly_commands += IF_GOTO_ASM.format(func_name=self.__cur_func, label=label)

    def write_call(self, func_name, num_vars):
        self.__assembly_commands += CALL_ASM.format(func_name=func_name, num_vars=num_vars,
                                                    n_vars_plus5=int(num_vars) + 5, index=self.__cur_label_index)
        self.__cur_label_index += 1

    def __write_function(self, func_name, num_of_args):
        self.__cur_func = func_name
        self.__assembly_commands += FUNCTION_PREFIX.format(file_name=self.__file_name, func_name=func_name,
                                                           num=num_of_args)
        self.__assembly_commands += PUSH_FUNCTION_LCL * int(num_of_args)

    def __write_return(self):
        self.__assembly_commands += RETURN_ASM.format()

    def translator(self):
        """"start the translating process"""
        func_dict = {C_ARITHMETIC: self.write_arithmetic, C_PUSH: self.__write_push, C_POP: self.__write_pop,
                     C_LABEL: self.__write_label, C_GOTO: self.__write_goto, C_IF: self.__write_if_goto,
                     C_CALL: self.write_call, C_FUNCTION: self.__write_function, C_RETURN: self.__write_return}
        while self.__parser.has_more_commands():
            self.__parser.advance()
            if self.__parser.arg1() == POINTER:
                self.__write_pointer()
            elif self.__parser.arg1() == STATIC:
                self.__write_static()
            elif self.__parser.command_type() == C_RETURN:
                self.__write_return()
            else:
                # func is the function.asm we need to execute that determined by the command type
                func = self.__parser.command_type()
                func_dict[func](self.__parser.arg1(), self.__parser.arg2())

    def export_output(self, output_file_name, file_path):
        """"export the assembly commands that the code writer translated into asm file"""
        output_file_name = ASM_FILE.format(re.sub(r'\.vm', EMPTY_STRING, output_file_name))
        file_path += "/" + output_file_name

        output = open(file_path, WRITE)
        call = CALL_ASM.format(func_name=SYS_INIT, num_vars=SYS_VAL, n_vars_plus5=int(SYS_VAL) + 5,
                               index=self.__cur_label_index)
        self.__assembly_commands = BOOT_STRAP + call + self.__assembly_commands

        output.write(self.__assembly_commands)
        output.close()
