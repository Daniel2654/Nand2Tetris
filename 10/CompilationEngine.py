from JackTokenizerV2 import *

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


class CompilationEngine:

    def __init__(self, filepath, filename):
        self.__tokenizer = JackTokenizer(filepath, filename)
        self.__output_path = self.__tokenizer.parse()
        self.__tree = ET.parse(self.__output_path)
        self.__root = iter(self.__tree.getroot())
        self.__cur_token = True
        self.__next_token = next(self.__root)

        self.__xml_data = EMPTY_STRING

    def __advance_token(self):
        """"advance the current token"""
        self.__cur_token = self.__next_token
        self.__next_token = next(self.__root, None)

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

    def compile_class(self):
        """"compiles a complete class"""
        subroutine_dec = [CONSTRUCTOR, FUNCTION, METHOD]
        var_dec = [STATIC, FIELD]

        cur_class = ET.Element(CLASS)
        self.__append_tokens(cur_class, 3)  # add class main {
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text in var_dec:
            class_var_dec = self.compile_class_var_dec()
            cur_class.append(class_var_dec)
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text in subroutine_dec:
            class_sub_dec = self.compiles_subroutine_dec()
            cur_class.append(class_sub_dec)
        self.__append_tokens(cur_class, 1)  # add }

        self.__xml_data += minidom.parseString(ET.tostring(cur_class)).toprettyxml()[DECLARATION_LEN:]

    def compile_class_var_dec(self):
        """"compiles a static variable declaration or a field declaration"""
        class_var_dec = ET.Element(CLASS_VAR_DEC)
        self.__append_tokens(class_var_dec, SEMICOLON)

        return class_var_dec

    def compiles_subroutine_dec(self):
        """"compiles a complete method, function, or constructor"""
        subroutine_dec = [CONSTRUCTOR, FUNCTION, METHOD]
        class_sub_dec = ET.Element(CLASS_SUB_DEC)
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text in subroutine_dec:
            break
        self.__append_tokens(class_sub_dec, LEFT_BRACKET3)
        parameter_list = self.compile_parameter_list()
        class_sub_dec.append(parameter_list)
        self.__append_tokens(class_sub_dec)  # append the right bracket ')'
        subroutine_body = self.compile_subroutine_body()
        class_sub_dec.append(subroutine_body)

        return class_sub_dec

    def compile_parameter_list(self):
        """"compile a (possibly empty) parameter list. does not handle the enclosing"""
        parameter_list = ET.Element(PARAMETER_LIST)
        self.__append_tokens(parameter_list, RIGHT_BRACKET3, False)
        # empty parameter list
        if len(parameter_list) == 0:
            parameter_list.text = NEW_LINE
        return parameter_list

    def compile_subroutine_body(self):
        """"compiles a subroutine body"""
        subroutine_body = ET.Element(SUBROUTINE_BODY)
        self.__append_tokens(subroutine_body)  # add {
        while self.__cur_token.tag == KEYWORD and self.__cur_token.text == VAR:
            var_dec = self.compile_var_dec()
            subroutine_body.append(var_dec)
        statements = self.compile_statements()
        subroutine_body.append(statements)
        self.__append_tokens(subroutine_body)  # add }

        return subroutine_body

    def compile_var_dec(self):
        """"compiles a var declaration"""
        var_dec = ET.Element(VAR_DEC)
        self.__append_tokens(var_dec, SEMICOLON)
        return var_dec

    def compile_let(self):
        let_statement = ET.Element(LET_STATEMENT)
        self.__append_tokens(let_statement, 2)
        if self.__cur_token.text == LEFT_BRACKET2:
            self.__append_tokens(let_statement)  # append [
            expression = self.compile_expression()

            let_statement.append(expression)
            self.__append_tokens(let_statement)  # append ]
        self.__append_tokens(let_statement)  # append =
        expression = self.compile_expression()
        let_statement.append(expression)
        self.__append_tokens(let_statement)  # append ;

        return let_statement

    def compile_if(self):
        """"compile an if statement"""
        if_statement = ET.Element(IF_STATEMENT)
        self.__append_tokens(if_statement, 2)  # append if (
        expression = self.compile_expression()
        if_statement.append(expression)  # add the expression
        self.__append_tokens(if_statement, 2)  # append ) {

        statements = self.compile_statements()
        if_statement.append(statements)  # add the statements
        self.__append_tokens(if_statement)  # append ) {

        if self.__cur_token.text == ELSE:
            self.__append_tokens(if_statement, 2)  # append else {
            statements = self.compile_statements()
            if_statement.append(statements)  # add the statements
            self.__append_tokens(if_statement)

        return if_statement

    def compile_while(self):
        """"compile a while statement"""
        while_statement = ET.Element(WHILE_STATEMENT)
        self.__append_tokens(while_statement, 2)  # append if (
        expression = self.compile_expression()
        while_statement.append(expression)  # add the expression
        self.__append_tokens(while_statement, 2)  # append ) {
        statements = self.compile_statements()
        while_statement.append(statements)  # add the statements
        self.__append_tokens(while_statement)  # append }

        return while_statement

    def compile_do(self):
        """"compile a do statement"""
        do_statement = ET.Element(DO_STATEMENT)
        self.__append_tokens(do_statement)  # append do
        self.term_helper(do_statement)
        self.__append_tokens(do_statement)  # append ;

        return do_statement

    def compile_return(self):
        """"compile a return statement"""
        return_statement = ET.Element(RETURN_STATEMENT)
        self.__append_tokens(return_statement)  # append return
        if self.__cur_token.text != SEMICOLON:
            expression = self.compile_expression()
            return_statement.append(expression)  # add the expression
        self.__append_tokens(return_statement)  # append ;

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

    def compile_expression(self):
        """"compile_expression"""
        expression = ET.Element(EXPRESION)
        operators = [PLUS, MINUS, SLASH, AMPERSAND, VERTICAL_BAR, GREATER_THEN, LESS_THAN, EQUAL, ASTRIX]
        unary_operators = [MINUS, TILDA]

        while True:
            if self.__cur_token.text in unary_operators:
                term = self.compile_term()
                expression.append(term)
                x = minidom.parseString(ET.tostring(expression)).toprettyxml()[DECLARATION_LEN:]
                print(x)

                break

            term = self.compile_term()
            if not term:
                self.__append_tokens(expression)
                return expression
            expression.append(term)

            if self.__cur_token.text not in operators or self.__cur_token.text == SEMICOLON:
                break
            self.__append_tokens(expression)

        return expression

    def term_helper(self, parent, is_term=False):
        """"check which condition the func should compile and compile it"""
        unary_operators = [MINUS, TILDA]

        if self.__cur_token.text in unary_operators:
            self.__append_tokens(parent)
            sub_term = self.compile_term(True)
            parent.append(sub_term)

        elif self.__cur_token.text == LEFT_BRACKET3 and is_term:
            self.__append_tokens(parent)  # append (
            sub_expresion_list = self.compile_expression()
            parent.append(sub_expresion_list)
            self.__append_tokens(parent)  # append )
        elif self.__cur_token.text == LEFT_BRACKET3:
            self.__append_tokens(parent)  # append (
            sub_expresion_list = self.compile_expression_list()
            parent.append(sub_expresion_list)
            self.__append_tokens(parent)  # append )
        elif self.__next_token.text == LEFT_BRACKET3:
            self.__append_tokens(parent, 2)  # append x(
            sub_expresion_list = self.compile_expression_list()
            parent.append(sub_expresion_list)
            self.__append_tokens(parent)  # append )
        elif self.__next_token.text == LEFT_BRACKET2:
            self.__append_tokens(parent, 2)  # append x [
            sub_expresion = self.compile_expression()
            parent.append(sub_expresion)
            self.__append_tokens(parent)  # append ]
        elif self.__next_token.text == DOT:
            self.__append_tokens(parent, 4)  # append .xxx(
            sub_expresion_list = self.compile_expression_list()
            parent.append(sub_expresion_list)
            self.__append_tokens(parent, 1)  # append )
        else:
            self.__append_tokens(parent)

        return parent

    def compile_term(self, is_term=False):
        """"compiles a term. This method is faced with a slight difficulty when trying to decide between some of the
        alternative rules. Specifically, if the current token is an identifier, it must still distinguish between a
        variable, an array entry, and a subroutine call. The distinction can be made by looking ahead one extra
        token. A single look-ahead token, which may be one of [, (, ., suffices to distinguish between the
        three possibilities. Any other token is not part of this term and should not be advanced over. """
        term = ET.Element(TERM)
        if self.__cur_token.text == COMMA or self.__cur_token.text == SEMICOLON:
            return False
        self.term_helper(term, is_term)
        return term

    def compile_expression_list(self):
        """"compiles a (possibly empty) comma separated list of expressions. """
        expresion_list = ET.Element(EXPRESION_LIST)

        while self.__cur_token.text != RIGHT_BRACKET3:
            if self.__cur_token.text == COMMA:
                self.__append_tokens(expresion_list)  # add comma
                continue
            expression = self.compile_expression()
            expresion_list.append(expression)
        if len(expresion_list) == 0:
            expresion_list.text = NEW_LINE

        return expresion_list

    def start(self):
        """"start the compiling process, this function keep running until there is no more classes to compile and
        finally it export the output into xml file"""
        while self.__cur_token:
            self.__advance_token()
            if self.__cur_token.tag == KEYWORD and self.__cur_token.text == CLASS:
                self.compile_class()

        # export the output
        with open(self.__output_path, WRITE) as output:
            output.write(self.__xml_data)
