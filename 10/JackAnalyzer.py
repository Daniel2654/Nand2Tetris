from CompilationEngine import *
import os

JACK_END = ".jack"


class JackAnalyzer:
    """"start the compilation process"""

    def __init__(self, filepath):
        """"the constructor of the JackAnalyzer gets a path to directory
        that contains jack files or specific file"""
        self.__path = filepath
        self.__code_writer = None
        self.__filename = os.path.basename(filepath)
        self.__cur_index = 0

    def __translate_single_file(self, filename):
        """"translate a single vm file
        :param filename: the name of the file"""
        file_path = self.__path + '/' + filename
        compilation_engine = CompilationEngine(file_path, filename)
        compilation_engine.start()


    def __translate_dir(self):
        """"translate whole directory that contains jack files and store the
        xml files in the same directory"""
        files = os.listdir(self.__path)
        for file in files:
            if file.endswith(JACK_END):
                self.__translate_single_file(file)

    def startTranslate(self):
        """"start the compilation process, determine if the given path is a
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
    jack_analyzer = JackAnalyzer(sys.argv[1])
    jack_analyzer.startTranslate()
