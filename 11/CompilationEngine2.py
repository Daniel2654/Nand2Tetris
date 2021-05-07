from JackTokenizer import *
from VMWriter import *
from SymbolTable import *

CLASS = "class"
CLASS_VAR_DEC = "classVarDec"
CLASS_SUB_DEC = "subroutineDec"
PARAMETER_LIST = "parameterList"
SUBROUTINE_BODY = "subroutineBody"
VAR_DEC = "varDec"
EXPRESION = "expression"
EXPRESION_LIST = "expressionList"
TERM = "term"

STATEMENT = "statements"
LET_STATEMENT = "letStatement"
IF_STATEMENT = "ifStatement"
WHILE_STATEMENT = "whileStatement"
DO_STATEMENT = "doStatement"
RETURN_STATEMENT = "returnStatement"

ELSE = "else"

# var dec
FIELD = "field"
STATIC = "static"

CONSTANT = "constant"
MULTIPLY = "call Math.multiply 2"
DIVISION = "call Math.divide 2"
ALLOC = "Memory.alloc"
STRING_NEW = "String.new"
STRING_APPEND = "String.appendChar"

ZERO_ARGS = '0'
ONE_ARG = '1'
TWO_ARGS = '2'

NEG = "neg"

LABEL = "L{index}"
IF_TRUE = "IF_TRUE{index}"
IF_FALSE = "IF_FALSE{index}"
IF_END = "IF_END{index}"

WHILE_EXP = "WHILE_EXP{index}"
WHILE_END = "WHILE_END{index}"

NEW = "new"
FUNCTION_FORMAT = "{class_}.{name_}"

POINTER = "pointer"
TEMP = "temp"

THIS_VAL = '0'
THAT_VAL = '1'

ARITHMETIC_DICT = {'+': "add", '-': "sub", '=': "eq", '>': "gt", '<': "lt", "&": "and", '|': "or", ASTRIX: MULTIPLY,
                   SLASH: DIVISION}

SEGMENT_DICT = {ARG: 'argument', VAR: "local", FIELD: "this", STATIC: "static"}


class CompilationEngine:
    """"compile a single jack file to xml code"""

    def __init__(self, filepath, filename):
        """"Constructor of the CompilationEngine
        :param: __tokenizer - a tokenizer object
        :param __output_path - the path of the output
        :param __tree - xml tree of the tokens
        :param __root - the root of the xml tokens tree
        :param __cur_token - the current token
        :param __next_token - the next token"""
        self.__tokenizer = JackTokenizer(filepath, filename)
        self.__output_path = self.__tokenizer.parse()
        self.__root = iter(self.__tokenizer.get_root())
        self.__cur_token = True
        self.__next_token = next(self.__root)
        self.__class_symbol_table = SymbolTable()
        self.__subroutine_symbol_table = SymbolTable()

        self.__class_name = None

        self.__cur_index = 0
        self.__num_of_dec = 0
        self.__vm_writer = VMWriter(self.__output_path)  # later
        self.__is_void = False

        self.__xml_data = EMPTY_STRING

    def __advance_token(self):
        """"advance the current token"""
        self.__cur_token = self.__next_token
        self.__next_token = next(self.__root, None)

    def __add_cur_token(self):
        cur_token = self.__cur_token
        self.__advance_token()
        return cur_token.text

    def __append_tokens(self, parent, stop_condition=1, with_last_elem=True):
        """"append x tokens to the parent
        :param parent - the parent of the tokens
        :param: stop_condition - the num of the tokens to add
        :param - with_last_elem - in case we are adding till the next string if with_last_elem == True add the last
        element otherwise don't add it"""
        if type(stop_condition) == str:
            while with_last_elem or self.__cur_token.text != stop_condition:
                last_token = self.__cur_token
                ET.SubElement(parent, self.__cur_token.tag).text = self.__cur_token.text
                self.__advance_token()
                if last_token.text == stop_condition:
                    return
        else:
            for i in range(stop_condition):
                ET.SubElement(parent, self.__cur_token.tag).text = self.__cur_token.text
                self.__advance_token()

    def __get_type_and_index(self, name):
        if self.__subroutine_symbol_table.is_in(name):
            table = self.__subroutine_symbol_table
        elif self.__class_symbol_table.is_in(name):
            table = self.__class_symbol_table

        segment = SEGMENT_DICT[table.kind_of(name)]
        index = table.index_of(name)

        return segment, index

    def __compile_constructor(self, num_of_args):
        class_sub_dec = ET.Element(CLASS_SUB_DEC)

        func_name = FUNCTION_FORMAT.format(class_=self.__class_name, name_=NEW)
        self.__vm_writer.write_function(func_name, "{num}")
        self.__subroutine_symbol_table.clear()  # remove this from the constructor

        num_of_parameters = self.compile_parameter_list()

        self.__vm_writer.write_push(CONSTANT, self.__num_of_dec)  # push constant <n_Parmeters>
        self.__vm_writer.write_call(ALLOC, ONE_ARG)
        self.__vm_writer.write_pop(POINTER, THIS_VAL)

        self.__append_tokens(class_sub_dec)  # append the right bracket ')'

        num_of_locals = self.compile_subroutine_body()
        self.__vm_writer.edit_locals(num_of_locals)  # changes the number of locals the function has

        self.__subroutine_symbol_table.clear()

    def __compile_function(self, name):
        name = FUNCTION_FORMAT.format(class_=self.__class_name, name_=name)
        self.__vm_writer.write_function(name, "{num}")  # write a function without the number of locals
        self.compile_parameter_list()
        self.__advance_token()  # append the right bracket ')'
        num_of_locals = self.compile_subroutine_body()  # get the number of locals
        self.__vm_writer.edit_locals(num_of_locals)  # changes the number of locals the function has

    def __compile_method(self, name):
        class_sub_dec = ET.Element(CLASS_SUB_DEC)
        self.__subroutine_symbol_table.define(ARG, self.__class_name, THIS)

        name = FUNCTION_FORMAT.format(class_=self.__class_name, name_=name)
        self.__vm_writer.write_function(name, "{num}")  # write a function without the number of locals
        self.__vm_writer.write_push(ARG, 0)
        self.__vm_writer.write_pop(POINTER, THIS_VAL)
        self.compile_parameter_list()

        self.__append_tokens(class_sub_dec)  # append the right bracket ')'
        num_of_locals = self.compile_subroutine_body()  # get the number of locals
        self.__vm_writer.edit_locals(num_of_locals)  # changes the number of locals the function has

    def compile_class(self):
        """"compiles a complete class"""
        subroutine_dec = [CONSTRUCTOR, FUNCTION, METHOD]
        var_dec = [STATIC, FIELD]
        cur_class = ET.Element(CLASS)
        self.__advance_token()
        self.__class_name = self.__cur_token.text

        self.__append_tokens(cur_class, 2)  # add class main {
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text in var_dec:
            class_var_dec = self.compile_class_var_dec()
            cur_class.append(class_var_dec)
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text in subroutine_dec:
            class_sub_dec = self.compiles_subroutine_dec()
            cur_class.append(class_sub_dec)
        self.__append_tokens(cur_class, 1)  # add }

        self.__class_symbol_table.clear()
        self.__xml_data += minidom.parseString(ET.tostring(cur_class)).toprettyxml()[DECLARATION_LEN:]

    def compile_class_var_dec(self):
        """"compiles a static variable declaration or a field declaration"""
        class_var_dec = ET.Element(CLASS_VAR_DEC)
        kind = self.__add_cur_token()
        type_ = self.__add_cur_token()
        while self.__cur_token.text != SEMICOLON:
            self.__class_symbol_table.define(kind, type_, self.__add_cur_token())
            if self.__cur_token.text == COMMA:
                self.__advance_token()
            if kind == FIELD:
                self.__num_of_dec += 1
        self.__append_tokens(class_var_dec, SEMICOLON)

        return class_var_dec

    def compiles_subroutine_dec(self):
        """"compiles a complete method, function, or constructor"""
        class_sub_dec = ET.Element(CLASS_SUB_DEC)
        subroutine_type = self.__cur_token.text

        self.__advance_token()
        self.__advance_token()

        name = self.__add_cur_token()
        self.__advance_token()

        if subroutine_type == CONSTRUCTOR:
            self.__compile_constructor(5)
        elif subroutine_type == FUNCTION:
            self.__compile_function(name)
        else:
            self.__compile_method(name)

        self.__subroutine_symbol_table.clear()

        return class_sub_dec

    def compile_parameter_list(self):
        """"compile a (possibly empty) parameter list. does not handle the enclosing"""
        num_of_parameter = 0
        while self.__cur_token.text != RIGHT_BRACKET3:
            self.__subroutine_symbol_table.define(ARG, self.__add_cur_token(), self.__add_cur_token())
            if self.__cur_token.text == COMMA:
                self.__advance_token()
            num_of_parameter += 1

        return num_of_parameter

    def compile_subroutine_body(self):
        """"compiles a subroutine body"""
        subroutine_body = ET.Element(SUBROUTINE_BODY)
        self.__append_tokens(subroutine_body)  # add {

        num_of_locals = 0
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text == VAR:
            num_of_locals += self.compile_var_dec()
        statements = self.compile_statements()
        subroutine_body.append(statements)
        self.__append_tokens(subroutine_body)  # add }

        return num_of_locals

    def compile_var_dec(self):
        """"compiles a var declaration"""
        var_dec = ET.Element(VAR_DEC)
        kind = self.__add_cur_token()
        type_ = self.__add_cur_token()

        num_of_vars = 0
        while self.__cur_token.text != SEMICOLON:
            self.__subroutine_symbol_table.define(kind, type_, self.__add_cur_token())
            if self.__cur_token.text == COMMA:
                self.__advance_token()
            num_of_vars += 1

        self.__advance_token()
        return num_of_vars

    def compile_let(self):
        let_statement = ET.Element(LET_STATEMENT)
        self.__advance_token()

        if self.__next_token.text == LEFT_BRACKET2:
            self.__compile_arr()
            expression = self.compile_expression()
            self.__append_tokens(let_statement)  # append ;
            self.__vm_writer.write_pop(TEMP, 0)
            self.__vm_writer.write_pop(POINTER, 1)
            self.__vm_writer.write_push(TEMP, 0)
            self.__vm_writer.write_pop("that", 0)

            return let_statement
        else:
            var_name = self.__add_cur_token()
            segment, index = self.__get_type_and_index(var_name)  # get the segment and the index of the variable

            self.__append_tokens(let_statement)  # append =
            expression = self.compile_expression()
            self.__append_tokens(let_statement)  # append ;

            self.__vm_writer.write_pop(segment=segment, index=index)  # pop it into the variable

        return let_statement

    def compile_if(self):
        """"compile an if statement"""
        if_statement = ET.Element(IF_STATEMENT)
        self.__append_tokens(if_statement, 2)  # append if (
        expression = self.compile_expression()
        cur_index = self.__cur_index
        self.__cur_index += 1  # advance the index by 2

        self.__vm_writer.write_if(IF_TRUE.format(index=cur_index))
        self.__vm_writer.write_goto(IF_FALSE.format(index=cur_index))
        self.__append_tokens(if_statement, 2)  # append ) {

        self.__vm_writer.write_label(IF_TRUE.format(index=cur_index))
        statements = self.compile_statements()
        if_statement.append(statements)  # add the statements
        self.__append_tokens(if_statement)  # append ) {

        if self.__cur_token.text == ELSE:
            self.__vm_writer.write_goto(IF_END.format(index=cur_index))
            self.__vm_writer.write_label(IF_FALSE.format(index=cur_index))

            self.__append_tokens(if_statement, 2)  # append else {
            statements = self.compile_statements()
            if_statement.append(statements)  # add the statements
            self.__append_tokens(if_statement)
            self.__vm_writer.write_label(IF_END.format(index=cur_index))
        else:
            self.__vm_writer.write_label(IF_FALSE.format(index=cur_index))

        return if_statement

    def compile_while(self):
        """"compile a while statement"""
        cur_index = self.__cur_index
        self.__cur_index += 1
        self.__vm_writer.write_label(WHILE_EXP.format(index=cur_index))  # generate loop label
        while_statement = ET.Element(WHILE_STATEMENT)
        self.__append_tokens(while_statement, 2)  # append if (
        expression = self.compile_expression()

        self.__vm_writer.write_arithmetic("not")  # check if need to execute the loop
        self.__vm_writer.write_if(WHILE_END.format(index=cur_index))

        self.__append_tokens(while_statement, 2)  # append ) {
        statements = self.compile_statements()

        self.__append_tokens(while_statement)  # append }
        self.__vm_writer.write_goto(WHILE_EXP.format(index=cur_index))

        self.__vm_writer.write_label(WHILE_END.format(index=cur_index))  # generate end of the loop label

        self.__cur_index += 1
        return while_statement

    def compile_do(self):
        """"compile a do statement"""
        do_statement = ET.Element(DO_STATEMENT)
        self.__append_tokens(do_statement)  # append do
        self.term_helper(do_statement)
        self.__append_tokens(do_statement)  # append ;

        self.__vm_writer.write_pop(TEMP, 0)  # we call do when don't need the return value (for example in void methods)

        return do_statement

    def compile_return(self):
        """"compile a return statement"""
        return_statement = ET.Element(RETURN_STATEMENT)
        self.__append_tokens(return_statement)  # append return
        if self.__cur_token.text == THIS:  # return this
            self.__vm_writer.write_push(POINTER, THIS_VAL)
            self.__advance_token()
        elif self.__cur_token.text != SEMICOLON:  # return expression
            expression = self.compile_expression()
            return_statement.append(expression)  # add the expression
        else:  # for void method
            self.__is_void = True
            self.__vm_writer.write_push(CONSTANT, 0)

        self.__append_tokens(return_statement)  # append ;

        self.__vm_writer.write_return()

        return return_statement

    def compile_statements(self):
        """"compiles a sequences of statements does not handle the enclosing {}"""
        statements = ET.Element(STATEMENT)
        statements_dict = {LET: self.compile_let, IF: self.compile_if, WHILE: self.compile_while, DO: self.compile_do,
                           RETURN: self.compile_return}
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text in statements_dict:
            statement = statements_dict[self.__cur_token.text]()
            statements.append(statement)
        return statements

    def compile_string(self):
        string = self.__cur_token.text
        self.__vm_writer.write_push(CONSTANT, len(string))  # push constant <string_len>
        self.__vm_writer.write_call(STRING_NEW, ONE_ARG)
        #
        for char in string:
            asci_val = ord(char)
            self.__vm_writer.write_push(CONSTANT, asci_val)  # push constant <char>
            self.__vm_writer.write_call(STRING_APPEND, TWO_ARGS)

        self.__advance_token()

    def compile_expression(self):
        """"compile_expression"""
        expression = ET.Element(EXPRESION)
        operators = [PLUS, MINUS, SLASH, AMPERSAND, VERTICAL_BAR, GREATER_THEN, LESS_THAN, EQUAL, ASTRIX]
        unary_operators = [MINUS, TILDA]
        self.compile_term()
        while self.__cur_token.text in operators:
            operator = self.__cur_token.text
            self.__advance_token()
            self.compile_term()
            self.__write_op(operator)

        return expression

    def __write_op(self, operator):
        self.__vm_writer.write_arithmetic(ARITHMETIC_DICT[operator])

    def __write_var(self, table):
        segment = SEGMENT_DICT[table.kind_of(self.__cur_token.text)]
        index = table.index_of(self.__cur_token.text)
        self.__vm_writer.write_push(segment=segment, index=index)

    def __write_vm_num_or_var(self):
        if self.__cur_token.tag == INTEGER_CONSTANT:
            self.__vm_writer.write_push(CONSTANT, self.__cur_token.text)
        elif self.__subroutine_symbol_table.is_in(self.__cur_token.text):  # writes command in subroutine table
            self.__write_var(self.__subroutine_symbol_table)
        elif self.__cur_token.text in ARITHMETIC_DICT:  # writes arithmetic command
            self.__vm_writer.write_arithmetic(ARITHMETIC_DICT[self.__cur_token.text])
        elif self.__class_symbol_table.is_in(self.__cur_token.text):  # writes from class symbol table
            self.__write_var(self.__class_symbol_table)
        else:
            pass

    def __get_type(self, name):
        arg_type = self.__subroutine_symbol_table.type_of(name)
        if arg_type == name:
            arg_type = self.__class_symbol_table.type_of(name)
        return arg_type

    def __compile_subroutine(self):
        num_of_args = 1
        if self.__next_token.text == LEFT_BRACKET3:
            self.__vm_writer.write_push(POINTER, THIS_VAL)
            subroutine_name = FUNCTION_FORMAT.format(class_=self.__class_name, name_=self.__add_cur_token())
        elif self.__next_token.text == DOT:
            self.__write_vm_num_or_var()  # push xxx.
            arg_name = self.__cur_token.text
            arg_type = self.__get_type(arg_name)  # edit later can be in class
            self.__advance_token()
            subroutine_name = arg_type + self.__add_cur_token() + self.__add_cur_token()

            num_of_args = 1 if arg_type != arg_name else 0  # means we are adding this
        self.__advance_token()  # advance (
        num_of_args += self.compile_expression_list()
        self.__advance_token()  # advance )

        self.__vm_writer.write_call(subroutine_name, num_of_args)

    def __compile_arr(self):
        self.__write_vm_num_or_var()
        self.__advance_token()  # advance var name
        self.__advance_token()  # advance [
        self.compile_expression()
        self.__vm_writer.write_arithmetic("add")
        self.__advance_token()  # advance ]

        if self.__cur_token.text == EQUAL:
            self.__advance_token()
            self.compile_expression()

    def term_helper(self, parent):
        """"check which condition the func should compile and compile it"""
        unary_operators = {MINUS: "neg", TILDA: "not"}

        if self.__cur_token.text in unary_operators:
            op = self.__cur_token.text
            self.__append_tokens(parent)
            sub_term = self.compile_term()
            parent.append(sub_term)
            self.__vm_writer.write_arithmetic(unary_operators[op])
        elif self.__cur_token.text == LEFT_BRACKET3:  # can be a subroutine call of expression
            self.__append_tokens(parent)  # append (
            if self.__next_token != COMMA:
                expression = self.compile_expression()
                parent.append(expression)
            else:
                expression_list = self.compile_expression_list()
                parent.append(expression_list)
            self.__append_tokens(parent)  # append )
        elif self.__next_token.text == LEFT_BRACKET3:  # subroutine
            self.__compile_subroutine()
        elif self.__next_token.text == LEFT_BRACKET2:
            self.__compile_arr()
            self.__vm_writer.write_pop(POINTER, THAT_VAL)
            self.__vm_writer.write_push("that", 0)
        elif self.__next_token.text == DOT:
            self.__compile_subroutine()
        elif self.__cur_token.text == TRUE:
            self.__vm_writer.write_push(CONSTANT, 0)
            self.__vm_writer.write_arithmetic("not")
            self.__append_tokens(parent)
        elif self.__cur_token.text == FALSE or self.__cur_token.text == NULL:
            self.__vm_writer.write_push(CONSTANT, 0)
            self.__append_tokens(parent)
        else:
            self.__write_vm_num_or_var()
            self.__append_tokens(parent)

        return parent

    def compile_term(self):
        """"compiles a term. This method is faced with a slight difficulty when trying to decide between some of the
        alternative rules. Specifically, if the current token is an identifier, it must still distinguish between a
        variable, an array entry, and a subroutine call. The distinction can be made by looking ahead one extra
        token. A single look-ahead token, which may be one of [, (, ., suffices to distinguish between the
        three possibilities. Any other token is not part of this term and should not be advanced over. """
        term = ET.Element(TERM)
        if self.__cur_token.text == COMMA or self.__cur_token.text == SEMICOLON or self.__cur_token.text == RIGHT_BRACKET3:
            return False
        elif self.__cur_token.tag == STRING_CONSTANT:
            self.compile_string()
            return term
        self.term_helper(term)
        return term

    def compile_expression_list(self):
        """"compiles a (possibly empty) comma separated list of expressions. """
        expresion_list = ET.Element(EXPRESION_LIST)

        num_of_args = 0
        while self.__cur_token.text != RIGHT_BRACKET3:
            if self.__cur_token.text == COMMA:
                self.__append_tokens(expresion_list)  # add comma
                continue
            expression = self.compile_expression()
            num_of_args += 1
            expresion_list.append(expression)

        # Empty tag
        if len(expresion_list) == 0:
            expresion_list.text = NEW_LINE

        return num_of_args

    def start(self):
        """"start the compiling process, this function keep running until there is no more classes to compile and
        finally it export the output into xml file"""
        while self.__cur_token:
            self.__advance_token()
            if self.__cur_token.tag == KEYWORD and self.__cur_token.text == CLASS:
                self.compile_class()

        # export the output
        self.__vm_writer.export_output()
