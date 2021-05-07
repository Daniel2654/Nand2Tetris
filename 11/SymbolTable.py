
ARG = "argument"
VAR = "var"
STATIC = "static"
FIELD = "field"

TYPE = 0
KIND = 1
INDEX = 2

class SymbolTable:

    def __init__(self):
        """"Creates a new symbol"""
        self.__symbol_table = dict()
        self.__index_counter = {STATIC: 0, FIELD: 0, ARG: 0, VAR: 0}

    def clear(self):
        """"resets the subroutine symbol table"""
        self.__symbol_table.clear()
        for key in self.__index_counter:
            self.__index_counter[key] = 0


    def define(self, kind, val_type,  name):
        """"Defines a new identifier of the given name, type and kind and assigns it a running index. STATIC and
        FIELD identifiers have a class scope while ARG and VAR identifiers have subroutine scope"""
        self.__symbol_table[name] = [val_type, kind, self.__index_counter[kind]]
        self.__index_counter[kind] += 1

    def var_count(self, kind):
        """returns the number of variables of the given kind already defined in the current scope"""
        return self.__index_counter[kind]

    def kind_of(self, name):
        """"returns the kind of the named identifier in the current scope. if the identifier is unkowen in the
        current scope it returns none"""
        return self.__symbol_table[name][KIND]

    def type_of(self, name):
        """"returns the type of the named identifier in the current scope"""
        return self.__symbol_table[name][TYPE] if name in self.__symbol_table else name

    def index_of(self, name):
        """"returns the index assigned to the named identifier"""
        return self.__symbol_table[name][INDEX]

    def is_in(self, key):
        return key in self.__symbol_table

    def get_table(self):
        return self.__symbol_table


if __name__ == '__main__':
    s = SymbolTable()