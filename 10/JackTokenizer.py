import sys
import re

EMPTY_STRING = ""
SPACE = ' '
TAB = '\t'
NEW_LINE = '\n'
READ = 'r'

# --------------------------------- Keyword ------------------------------------------------
KEYWORD = "Keyword"

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
THIS = "THIS"
LET = "let"
DO = "do"
IF = "if"
ELSE = "else"
WHILE = "while"
RETURN = "return"

# ------------------------------ Symbols ------------------------------------------------

SYMBOL = "symbol"
RE_EXPRESION = '(\"[^\"]*\"|\s|{|\}|\[|\]|\(|\)|\.|,|;|\+|-|&|\||<|>|=|\~|")'
RE_REMOVE = r'//*.*/*/|(//.*)'

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

SPECIAL_XML = {LESS_THAN: "&lt;", GREATER_THEN: "&gt;", QUOTE: "&quot;", AMPERSAND: "&amp;"}

TYPE_DICT = {CLASS: KEYWORD, CONSTRUCTOR: KEYWORD, FUNCTION: KEYWORD, METHOD: KEYWORD, FIELD: KEYWORD, STATIC: KEYWORD,
             VAR: KEYWORD, INT: KEYWORD, CHAR: KEYWORD, BOOLEAN: KEYWORD, VOID: KEYWORD, TRUE: KEYWORD, FALSE: KEYWORD,
             NULL: KEYWORD, THIS: KEYWORD, LET: KEYWORD, DO: KEYWORD, IF: KEYWORD, ELSE: KEYWORD, WHILE: KEYWORD,
             RETURN: KEYWORD, LEFT_BRACKET1: SYMBOL, RIGHT_BRACKET1: SYMBOL, LEFT_BRACKET2: SYMBOL,
             RIGHT_BRACKET2: SYMBOL,
             LEFT_BRACKET3: SYMBOL, RIGHT_BRACKET3: SYMBOL, DOT: SYMBOL, COMMA: SYMBOL, SEMICOLON: SYMBOL, PLUS: SYMBOL,
             MINUS: SYMBOL, SLASH: SYMBOL, AMPERSAND: SYMBOL, VERTICAL_BAR: SYMBOL, LESS_THAN: SYMBOL,
             GREATER_THEN: SYMBOL,
             EQUAL: SYMBOL, TILDA: SYMBOL}

KEYWORD_FORMAT = "<keyword>{keyword}</keyword>"
IDENTIFIER_FORMAT = "<identifier>{identifier}</identifier>"
SYMBOL_FORMAT = "<symbol>{symbol}</symbol>"
INTEGER_CONSTANT_FORMAT = "<integerConstant>{integer}</integerConstant>"
STRING_CONSTANT_FORMAT = "<stringConstant>{string}</stringConstant>"
TOKEN_FORMAT = "<token>" + NEW_LINE + "{tokens}" + "</token>"

class JackTokenizer:

    def __init__(self, filepath):
        self.__filepath = filepath
        self.__tokens = self.__split_file()
        self.__cur_token_index = 0
        self.__cur_token = None
        self.__cur_func = None
        self.__xml_tokens = EMPTY_STRING
        print(self.__tokens)

    def __split_file(self):
        with open(self.__filepath, READ) as file:
            # Remove notes
            file_lines = map(lambda string: re.sub(r'(//.*)', EMPTY_STRING, string).rstrip(), file)
            # Split to tokens
            tokens = [token for line in file_lines for token in re.split(RE_EXPRESION, line) if token not in
                      [TAB, EMPTY_STRING, SPACE]]
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
        self.__xml_tokens += TAB + KEYWORD_FORMAT.format(keyword=self.__cur_token) + NEW_LINE

    def symbol(self):
        """"should be called only if token type is SYMBOL
        :returns - the character which the current token."""
        if self.__cur_token in SPECIAL_XML:
            self.__cur_token = SPECIAL_XML[self.__cur_token]
        self.__xml_tokens += TAB + SYMBOL_FORMAT.format(symbol=self.__cur_token) + NEW_LINE

    def identifier(self):
        """"Should be called only if token type is IDENTIFIER
        :returns: the identifier which is the current token"""
        self.__xml_tokens += TAB + IDENTIFIER_FORMAT.format(identifier=self.__cur_token) + NEW_LINE

    def int_val(self):
        """"Should be called only if token type is INT_CONST
        :returns: the integer which is the current token"""
        self.__xml_tokens += TAB + INTEGER_CONSTANT_FORMAT.format(integer=self.__cur_token) + NEW_LINE

    def string_val(self):
        """"Should be called only if token type is STRING_CONST
        :returns: the string value of the current token without two enclosing double quotes"""
        self.__xml_tokens += TAB + STRING_CONSTANT_FORMAT.format(string=self.__cur_token[1:-1]) + NEW_LINE

    def exccuate_cur_func(self):
        self.__cur_func()

    def parse(self):
        while self.has_more_tokens():
            self.advance()
            self.token_type()
            self.exccuate_cur_func()
        self.__xml_tokens = TOKEN_FORMAT.format(tokens=self.__xml_tokens)

        print(self.__xml_tokens)


if __name__ == '__main__':
    x = JackTokenizer(sys.argv[1])
    x.parse()
