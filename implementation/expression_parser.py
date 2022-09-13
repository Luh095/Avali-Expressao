"""Implements an expression parser."""

import re

class Token:
    """Represents the token"""

    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

class Lexer:
    """Implements the lexical analizer."""

    OPEN_PARENTHESES = 0
    CLOSE_PARENTHESES = 1
    OPERATOR = 2
    NUMBER = 3

    def put_back(self):
        """Inserts back the characters read."""
        self.current_index = self.previous_index

    def error(self, message = None):
        """Used to throw errors."""
        error = (
            f"Error at {self.current_index}: "
            f"{self.stream[self.current_index - 1:self.current_index + 10]}"
        )

        if message is not None:
            error = f"{message}\n{error}"

        raise Exception(error)

    def __init__(self, stream):
        """Class constructor, responsible for initializing the object."""
        self.stream = stream
        self.current_index = 0
        self.previous_index = -1
        self.number_regular_expression = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")
        self.potentiation_regular_expression = re.compile(r"\*\*")

    def __iter__(self):
        """Responsible for returning the iterator object."""
        self.current_index = 0
        return self

    def __next__(self):
        """Get the next token."""
        if self.current_index < len(self.stream):
            while self.stream[self.current_index] in " \t\n\r":
                self.current_index += 1

            self.previous_index = self.current_index

            characther = self.stream[self.current_index]
            self.current_index += 1
            
            if self.__is_open_parentheses(characther):
                return Token(Lexer.OPEN_PARENTHESES, characther)

            if self.__is_close_parentheses(characther):
                return Token(Lexer.CLOSE_PARENTHESES, characther)
            
            number_or_operator = self.__handle_number_or_operator(characther)
            if number_or_operator is not None:
                return number_or_operator

        raise StopIteration()          

    def __is_open_parentheses(self, characther):
        return characther == "("

    def __is_close_parentheses(self, characther):
        return characther == ")"

    def __handle_number_or_operator(self, characther):
        if characther in "+/":
            return Token(Lexer.OPERATOR, characther)
        
        # Finite automata can be created using a regular expression
        input_to_match = self.stream[self.current_index - 1 :]
        match_number = self.number_regular_expression.match(input_to_match)
        next_characther = None
        if self.current_index < len(self.stream):
            next_characther = self.stream[self.current_index]

        if characther == "*":
            if next_characther != "*":
                return Token(Lexer.OPERATOR, characther)
            else:
                self.current_index += 1
                return Token(Lexer.OPERATOR, "**")

        if match_number is None:
            if characther == "-":
                return Token(Lexer.OPERATOR, characther)
            
            self.error()

        self.current_index += match_number.end() - 1
        number_value = match_number.group().replace(" ", "")
        return Token(Lexer.NUMBER, number_value)

class Parser:
    """Implements the syntax analyzer and parser."""

    def parse(self, stream):
        """Parse the source code."""
        lexer = Lexer(stream)
        return self.__expression(lexer)

    def __expression(self, lexer):
        """Parse an expression."""
        left_expression = self.__left_addition_or_subtraction(lexer)
        right_addition_or_subtraction = self.__right_addition_or_subtraction(lexer)

        return left_expression if right_addition_or_subtraction is None else left_expression + right_addition_or_subtraction

    def __left_addition_or_subtraction(self, lexer):
        """Parse an left expression."""
        left_expression = self.__left_expression(lexer)
        right_multiplication_or_division = self.__right_multiplication_or_division(lexer)

        return left_expression if right_multiplication_or_division is None else left_expression * right_multiplication_or_division

    def __left_expression(self, lexer):
        """Parse an left expression"""
        terminal = self.__terminal(lexer)
        right_potenciation = self.__right_potenciation(lexer)

        return terminal if right_potenciation is None else terminal ** right_potenciation

    def __right_addition_or_subtraction(self, lexer):
        """Parse an right addition or subtraction expression."""
        try:
            token = next(lexer)
        except StopIteration:
            return None
        
        if token.token_type == Lexer.OPERATOR:
            if token.value not in "+-":
                lexer.error(f"Unexpected token: '{token.value}'")

            left_addition_or_subtraction = self.__left_addition_or_subtraction(lexer)
            _ = self.__right_addition_or_subtraction(lexer)

            return left_addition_or_subtraction if token.value == "+" else -1 * left_addition_or_subtraction

        lexer.put_back()
        return None

    def __right_multiplication_or_division(self, lexer):
        """Parse right multiplication or division expression"""
        try:
            token = next(lexer)
        except StopIteration:
            return None

        if token.token_type == Lexer.OPERATOR and token.value in "*/":
            left_expression = self.__left_expression(lexer)
            _ = self.__right_multiplication_or_division(lexer)

            return left_expression if token.value == "*" else 1 / left_expression
        
        lexer.put_back()
        return None

    def __right_potenciation(self, lexer):
        "Parse an right potenciation."
        try:
            token = next(lexer)
        except StopIteration:
            return None

        if token.token_type == Lexer.OPERATOR and token.value == "**":
            left_expression = self.__left_expression(lexer)
            _ = self.__right_potenciation(lexer)

            return left_expression

        lexer.put_back()
        return None

    def __terminal(self, lexer):
        """Parse an terminal member."""
        try:
            token = next(lexer)
        except StopIteration:
            raise Exception("Unexpected end of source.") from None
        
        if token.token_type is Lexer.OPEN_PARENTHESES:
            expression_result = self.__expression(lexer)
            next_token = next(lexer)
            if next_token.token_type != Lexer.CLOSE_PARENTHESES and next_token.value != ")":
                lexer.error("Unbalanced parenthesis.")
            
            return expression_result
        
        if token.token_type is Lexer.NUMBER:
            return float(token.value)

        raise lexer.error(f"Unexpected token: {token.value}.")


if __name__ == "__main__":
    # expressions = [
    #     "1 + 2 * 3"
    # ]

    expressions = [
        "1 + 1",
        "2 * 3",
        "5 / 4",
        "2 * 3 + 1",
        "1 + 2 * 3",
        "(2 * 3) + 1",
        "2 * (3 + 1)",
        "(2 + 1) * 3",
        "-2 + 3",
        "5 + (-2)",
        "5 * -2",
        "-1 - -2",
        "-1 - 2",
        "4 - 5",
        "3 - ((8 + 3) * -2)",
        "2.01e2 - 200",
        "3 ** 2"
    ]

    parser = Parser()

    for expression in expressions:
        print(f"Expression: {expression}\t Result: {parser.parse(expression)}")