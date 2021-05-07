NEW_LINE = '\n'

PUSH_COMMAND = "push {segment} {index}" + NEW_LINE
POP_COMMAND = "pop {segment} {index}" + NEW_LINE
ARITHMETIC_COMMAND = "{command}" + NEW_LINE
LABEL_COMMAND = "label {label}" + NEW_LINE
GOTO_COMMAND = "goto {label}" + NEW_LINE
IF_GOTO_COMMAND = "if-goto {label}" + NEW_LINE
CALL_COMMAND = "call {func_name} {num_of_args}" + NEW_LINE
FUNCTION_COMMAND = "function {func_name} {num_of_locals}" + NEW_LINE
RETURN_COMMAND = "return" + NEW_LINE

EMPTY_STRING = ""
WRITE = 'w'





class VMWriter:

    def __init__(self, path):
        """"later"""
        self.__vm_commands = EMPTY_STRING
        self.__cur_command = None
        self.__path = path

    def write_push(self, segment, index):
        """"writes a VM push command"""
        self.__vm_commands += PUSH_COMMAND.format(segment=segment, index=index)

    def write_pop(self, segment, index):
        """"writes a VM pop command"""
        self.__vm_commands += POP_COMMAND.format(segment=segment, index=index)

    def write_arithmetic(self, command):
        """"writes a VM arithmetic logical command"""
        self.__vm_commands += ARITHMETIC_COMMAND.format(command=command)

    def write_label(self, label):
        """writes a VM label command"""
        self.__vm_commands += LABEL_COMMAND.format(label=label)

    def write_goto(self, label):
        """"writes a VM goto command"""
        self.__vm_commands += GOTO_COMMAND.format(label=label)

    def write_if(self, label):
        """"writes a VM if-goto command"""
        self.__vm_commands += IF_GOTO_COMMAND.format(label=label)

    def write_call(self, name, num_of_args):
        """"writes a VM function command"""
        self.__vm_commands += CALL_COMMAND.format(func_name=name, num_of_args=num_of_args)

    def write_function(self, name, num_of_locals):
        """"writes a VM function command"""
        self.__vm_commands += FUNCTION_COMMAND.format(func_name=name, num_of_locals=num_of_locals)

    def edit_locals(self, num_of_locals):
        self.__vm_commands = self.__vm_commands.format(num=num_of_locals)

    def write_return(self):
        """"writes a VM return command"""
        self.__vm_commands += RETURN_COMMAND

    def get_vm(self):
        return self.__vm_commands


    def export_output(self):
        """"export the VM command to the output file"""
        with open(self.__path, WRITE) as output:
            output.write(self.__vm_commands)
