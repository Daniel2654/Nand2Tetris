from assembler import *
import sys
import os


class AssemblerRunner:
    """"Start the translation process from assembly to binary, the assembler
    runner gets path from the terminal that could be directory or a specific
    file if its directory it will translate all the .asm files if it a
    specific file it will translate it and store it in the directory it was
    originally
    """

    def __init__(self, filepath):
        """"the constructor of the AssemblerRunner gets a path to directory
        that contains asm files or specific file"""
        self.__path = filepath

    def __translate_single_file(self, filename):
        """"translate a single asm file and export it into hdl file
        :param filename: the name of the file"""
        file_path = self.__path + '/' + filename
        assembler = Assembler(file_path, filename)
        assembler.translate()
        assembler.export_output()

    def __translate_dir(self):
        """"translate whole directory that contains asm files and store the
        hdl files int the same directory"""
        files = os.listdir(self.__path)
        for file in files:
            if file.endswith(ASM_END):
                self.__translate_single_file(file)

    def startTranslate(self):
        """"start the translsting process, determine if the given path is a
        directory or specific file and start to translating process"""

        # check if the file is directory or a specific file
        if os.path.isdir(self.__path):
            self.__translate_dir()
        else:
            file = os.path.basename(self.__path)
            abs_path = os.path.abspath(self.__path)
            self.__path = os.path.dirname(abs_path)
            self.__translate_single_file(file)


if __name__ == '__main__':
    x = AssemblerRunner(sys.argv[1])
    x.startTranslate()
