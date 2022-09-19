"""Implement a syntax analyzer"""
import token_type_compiler
import tree
import exceptions_compiler

class DerivationTreeGenerator:
    """Represents a sintax analyzer"""
    def __init__(self, tokens):
        self.current_index = 0
        self.tokens = tokens
        self.derivation_trees = []

    def create_tree(self):
        """Create the derivation tree"""
        program = self.__program()
        if program is None:
            raise exceptions_compiler.ExpressionError("No derivation tree was generated")
        return program

    def __program(self):
        statement = self.__statement()
        if statement is None:
            return None
        program = self.__program()
        return tree.Tree(None, statement, program)

    def __statement(self):
        identifier = self.__get_identifier()
        if identifier is not None:
            token = self.__get_token()
            if token.token_type == token_type_compiler.TokenType.OPERATOR and token.value == "=":
                self.current_index += 1
                expression = self.__expression()
                return tree.Tree(token, identifier, expression)
            self.current_index -= 1
        return self.__expression()
        
    def __expression(self):
        return self.__get_sum()

    def __get_token(self):
        return self.tokens[self.current_index]

    def __get_terminal(self):
        token = self.__get_token()
        if token.token_type == token_type_compiler.TokenType.END_OF_SOURCE:
            return None

        if token.token_type == token_type_compiler.TokenType.OPEN_PARENTHESE:
            self.current_index += 1
            expression = self.__expression()
            next_token = self.__get_token()
            if not next_token.token_type == token_type_compiler.TokenType.CLOSE_PARENTHESE:
                raise exceptions_compiler.ExpressionError("Unbalanced parentheses")
            self.current_index += 1
            return expression
        if token.token_type == token_type_compiler.TokenType.NUMBER:
            self.current_index += 1
            return tree.Tree(token, None, None)
        
        if token.token_type == token_type_compiler.TokenType.IDENTIFIER:
            self.current_index += 1
            next_token = self.__get_token()
            if next_token.token_type == token_type_compiler.TokenType.OPEN_PARENTHESE:
                self.current_index += 1
                expression = self.__expression()
                next_next_token = self.__get_token()
                if next_next_token.token_type == token_type_compiler.TokenType.CLOSE_PARENTHESE:
                    self.current_index += 1
                    identifier_tree = tree.Tree(token, None, None)
                    return tree.Tree(None, identifier_tree, expression)
                raise exceptions_compiler.ExpressionError("Unbalanced parentheses")
            return tree.Tree(token, None, None)

        raise exceptions_compiler.ExpressionError(f"Unexpected Token: {token.value}")

    def __get_identifier(self):
        token = self.__get_token()
        if token.token_type == token_type_compiler.TokenType.END_OF_SOURCE:
            return None

        if token.token_type == token_type_compiler.TokenType.IDENTIFIER:
            self.current_index += 1
            return tree.Tree(token, None, None)

    def __get_potenciation(self):
        value_a = self.__get_terminal()

        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.token_type == token_type_compiler.TokenType.END_OF_SOURCE:
            return value_a

        if token.token_type == token_type_compiler.TokenType.OPERATOR and token.value == "**":
            self.current_index += 1
            value_b = self.__get_potenciation()
            return tree.Tree(token, value_a, value_b)
        return value_a

    def __get_product(self):
        value_a = self.__get_potenciation()

        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.token_type == token_type_compiler.TokenType.END_OF_SOURCE:
            return value_a

        if token.token_type == token_type_compiler.TokenType.OPERATOR and token.value == "*" or token.value == "/":
            self.current_index += 1
            value_b = self.__get_product()
            return tree.Tree(token, value_a, value_b)
        return value_a

    def __get_sum(self):
        value_a = self.__get_product()
        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.token_type == token_type_compiler.TokenType.END_OF_SOURCE:
            return value_a

        if token.token_type == token_type_compiler.TokenType.OPERATOR and token.value in "+-":
            self.current_index += 1
            value_b = self.__get_sum()
            return tree.Tree(token, value_a, value_b)

        return value_a
