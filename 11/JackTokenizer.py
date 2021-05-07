import xml.etree.ElementTree as ET
from xml.dom import minidom

import sys
import re

EMPTY_STRING = ""
SPACE = ' '
TAB = '\t'
NEW_LINE = '\n'
READ = 'r'
DECLARATION_LEN = 23
TOKENS = "tokens"

RE_REMOVE = r'(//.*)|(\/\*\*.+\*\/)'

VM_POSTFIX = ".vm"
WRITE = 'w'

# --------------------------------- Keyword ------------------------------------------------
KEYWORD = "keyword"

CLASS = "class"
CONSTRUCTOR = "constructor"
FUNCTION = "function"
METHOD = "method"
FIELD = "field"
STATIC = "static"
VAR = "var"
INT = "int"
CHAR = "char"
BOOLEAN = "boolean"
VOID = "void"
TRUE = "true"
FALSE = "false"
NULL = "null"
THIS = "this"
LET = "let"
DO = "do"
IF = "if"
ELSE = "else"
WHILE = "while"
RETURN = "return"

# ------------------------------ Symbols ------------------------------------------------

SYMBOL = "symbol"
RE_EXPRESION = '(\"[^\"]*\"|\s|{|\}|\[|\]|\(|\)|\.|,|;|\+|-|&|\||<|>|=|\~|"|/\S)'
# Regular expression that match notes and strings
RE_NOTES_STRINGS = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"

QUOTE = '"'
LEFT_BRACKET1 = '{'
RIGHT_BRACKET1 = '}'
LEFT_BRACKET2 = '['
RIGHT_BRACKET2 = ']'
LEFT_BRACKET3 = '('
RIGHT_BRACKET3 = ')'
DOT = '.'
COMMA = ','
SEMICOLON = ';'
PLUS = '+'
MINUS = '-'
SLASH = '/'
AMPERSAND = '&'
VERTICAL_BAR = '|'
LESS_THAN = '<'
GREATER_THEN = '>'
EQUAL = '='
TILDA = '~'
ASTRIX = '*'

TYPE_DICT = {CLASS: KEYWORD, CONSTRUCTOR: KEYWORD, FUNCTION: KEYWORD, METHOD: KEYWORD, FIELD: KEYWORD, STATIC: KEYWORD,
             VAR: KEYWORD, INT: KEYWORD, CHAR: KEYWORD, BOOLEAN: KEYWORD, VOID: KEYWORD, TRUE: KEYWORD, FALSE: KEYWORD,
             NULL: KEYWORD, THIS: KEYWORD, LET: KEYWORD, DO: KEYWORD, IF: KEYWORD, ELSE: KEYWORD, WHILE: KEYWORD,
             RETURN: KEYWORD, LEFT_BRACKET1: SYMBOL, RIGHT_BRACKET1: SYMBOL, LEFT_BRACKET2: SYMBOL,
             RIGHT_BRACKET2: SYMBOL,
             LEFT_BRACKET3: SYMBOL, RIGHT_BRACKET3: SYMBOL, DOT: SYMBOL, COMMA: SYMBOL, SEMICOLON: SYMBOL, PLUS: SYMBOL,
             MINUS: SYMBOL, SLASH: SYMBOL, AMPERSAND: SYMBOL, VERTICAL_BAR: SYMBOL, LESS_THAN: SYMBOL,
             GREATER_THEN: SYMBOL,
             EQUAL: SYMBOL, TILDA: SYMBOL, ASTRIX: SYMBOL}

IDENTIFIER = "identifier"
STRING_CONSTANT = "stringConstant"
INTEGER_CONSTANT = "integerConstant"


class JackTokenizer:

    def __init__(self, filepath, filename):
        self.__filepath = filepath
        self.__output_path = filepath[:-5] + VM_POSTFIX
        self.__tokens = self.__split_file()
        self.__cur_token_index = 0
        self.__cur_token = None
        self.__cur_func = None
        self.__root = ET.Element(TOKENS)

    def __split_file(self):
        with open(self.__filepath, READ) as file:
            # Remove notes and support things like " // "  or " /* * /"
            regex = re.compile(RE_NOTES_STRINGS, re.MULTILINE | re.DOTALL)
            file_lines = regex.sub(lambda match: EMPTY_STRING if match.group(2) is not None else match.group(1),
                                   file.read())
            file_lines = [line.strip() for line in file_lines.splitlines()]
            # Split to tokens
            tokens = [token for line in file_lines for token in re.split(RE_EXPRESION, line) if token not in
                      [EMPTY_STRING, SPACE]]

            return tokens

    def has_more_tokens(self):
        """check if there is any more tokens in the input
        :returns: true if there is more tokens, false otherwise"""
        if self.__cur_token_index < len(self.__tokens):
            return True
        return False

    def advance(self):
        """"gets the next token from the input and make it the current token, call only if has_more_tokens is true
        """
        self.__cur_token = self.__tokens[self.__cur_token_index]
        self.__cur_token_index += 1

    def token_type(self):
        """":returns - the type of the current token as constant"""
        func_dict = {KEYWORD: self.key_word, SYMBOL: self.symbol}
        if self.__cur_token in TYPE_DICT:
            self.__cur_func = func_dict[TYPE_DICT[self.__cur_token]]
        elif self.__cur_token.isdigit():
            self.__cur_func = self.int_val
        elif self.__cur_token[0] == QUOTE:
            self.__cur_func = self.string_val
        else:
            self.__cur_func = self.identifier

    def key_word(self):
        """"should be called only if token type is KEYWORD
        :returns - the keyword which is the current token as a constant.
        KEYWORD"""
        ET.SubElement(self.__root, KEYWORD).text = self.__cur_token

    def symbol(self):
        """"should be called only if token type is SYMBOL
        :returns - the character which the current token."""
        ET.SubElement(self.__root, SYMBOL).text = self.__cur_token

    def identifier(self):
        """"Should be called only if token type is IDENTIFIER
        :returns: the identifier which is the current token"""
        ET.SubElement(self.__root, IDENTIFIER).text = self.__cur_token

    def int_val(self):
        """"Should be called only if token type is INT_CONST
        :returns: the integer which is the current token"""
        ET.SubElement(self.__root, INTEGER_CONSTANT).text = self.__cur_token

    def string_val(self):
        """"Should be called only if token type is STRING_CONST
        :returns: the string value of the current token without two enclosing double quotes"""
        ET.SubElement(self.__root, STRING_CONSTANT).text = self.__cur_token[1:-1]

    def execute_cur_func(self):
        self.__cur_func()

    def parse(self):
        while self.has_more_tokens():
            self.advance()
            self.token_type()
            self.execute_cur_func()
        self.__tokens = (minidom.parseString(ET.tostring(self.__root)).toprettyxml()[DECLARATION_LEN:])

        return self.__output_path

    def get_root(self):
        return self.__root
