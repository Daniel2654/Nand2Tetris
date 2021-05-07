import os
import sys
from CodeWriter import *

VM_END = ".vm"


class VmRunner:
    """"Start the vm translator"""

    def __init__(self, filepath):
        """"the constructor of the AssemblerRunner gets a path to directory
        that contains asm files or specific file"""
        self.__path = filepath
        self.__code_writer = None
        self.__filename = os.path.basename(filepath)
        self.__cur_index = 0

    def __translate_single_file(self, filename):
        """"translate a single vm file
        :param filename: the name of the file"""
        file_path = self.__path + '/' + filename
        parser = Parser(file_path)
        code_writer = CodeWriter(filename, parser, self.__cur_index)
        code_writer.translator()

        if self.__code_writer is not None:
            self.__code_writer += code_writer
        else:
            self.__code_writer = code_writer

        self.__cur_index += code_writer.get_cur_label_index()

    def __translate_dir(self):
        """"translate whole directory that contains vm files and store the
        asm files in the same directory"""
        files = os.listdir(self.__path)
        for file in files:
            if file.endswith(VM_END):
                self.__translate_single_file(file)

    def startTranslate(self):
        """"start the translsting process, determine if the given path is a
        directory or specific file and start the translating process"""

        # check if the file is directory or a specific file
        if os.path.isdir(self.__path):
            self.__translate_dir()
        else:
            file = os.path.basename(self.__path)
            abs_path = os.path.abspath(self.__path)
            self.__path = os.path.dirname(abs_path)
            self.__translate_single_file(file)

        if self.__code_writer:
            self.__code_writer.export_output(self.__filename, self.__path)


if __name__ == '__main__':
    x = VmRunner(sys.argv[1])
    x.startTranslate()
