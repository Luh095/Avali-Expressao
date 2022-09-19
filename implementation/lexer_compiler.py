"""A"""
import re
import token_model
import exceptions_compiler
import token_type_compiler

class Lexer:
    """A"""

    def __init__(self, stream):
        if stream is None or stream == "":
            raise exceptions_compiler.InvalidParameterError("stream cannot be empty or null")
        self.stream = stream
        self.stream_length = len(stream)

        self.current_index = 0
        self.tokens = []
        self.current_line = 0

        self.number_regular_expression = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")
        self.operator_regular_expression = re.compile(r"\*{2}|[\+\-\*\/\=]{1}")
        self.parentheses_regular_expression = re.compile(r"\(|\)")
        self.identifier_regular_expression = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")
    
    def create_tokens(self):
        try:
            while True:
                if self.current_index >= self.stream_length:
                    end_of_source_token = self.__create_end_of_source_token(self.current_line)
                    self.tokens.append(end_of_source_token)
                    raise exceptions_compiler.EndOfSourceError("No more data to read")

                character = self.__get_character()
                self.current_index += 1
                while character in " \t\n\r":
                    if character == "\n":
                        self.current_line += 1
                    self.__validate_end_of_source()
                    character = self.__get_character()
                    self.current_index += 1

                lexeme = None

                number_match = self.number_regular_expression.match(self.stream[self.current_index - 1:])
                if number_match is not None:
                    lexeme = number_match.group(0)
                    self.tokens.append(self.__create_number_token(lexeme, self.current_line))
                    self.current_index += len(lexeme) - 1
                    continue

                operator_match = self.operator_regular_expression.match(self.stream[self.current_index - 1:])
                if operator_match is not None:
                    lexeme = operator_match.group(0)
                    self.tokens.append(self.__create_operator_token(lexeme, self.current_line))
                    self.current_index += len(lexeme) - 1
                    continue

                parentheses_match = self.parentheses_regular_expression.match(self.stream[self.current_index - 1:])
                if parentheses_match is not None:
                    lexeme = parentheses_match.group(0)
                    if lexeme == "(":
                        self.tokens.append(self.__create_open_parenthese_token(self.current_line))
                    else:
                        self.tokens.append(self.__create_close_parenthese_token(self.current_line))
                    self.current_index += len(lexeme) - 1
                    continue

                identifier_match = self.identifier_regular_expression.match(self.stream[self.current_index - 1:])
                if identifier_match is not None:
                    lexeme = identifier_match.group(0)
                    self.tokens.append(self.__create_identifier_token(lexeme, self.current_line))
                    self.current_index += len(lexeme) - 1
                    continue

                raise exceptions_compiler.UnexpectedTokenError(f"Unexpected Token in line {self.current_line}: {lexeme}")

        except exceptions_compiler.EndOfSourceError:
            return self.tokens

    def __get_character(self):
        return self.stream[self.current_index]

    def __create_end_of_source_token(self, line):
        return token_model.Token(token_type_compiler.TokenType.END_OF_SOURCE, "EOF", line)

    def __create_operator_token(self, value, line):
        return token_model.Token(token_type_compiler.TokenType.OPERATOR, value, line)

    def __create_number_token(self, value, line):
        return token_model.Token(token_type_compiler.TokenType.NUMBER, float(value), line)

    def __create_open_parenthese_token(self, line):
        return token_model.Token(token_type_compiler.TokenType.OPEN_PARENTHESE, "(", line)

    def __create_close_parenthese_token(self, line):
        return token_model.Token(token_type_compiler.TokenType.CLOSE_PARENTHESE, ")", line)

    def __create_identifier_token(self, value, line):
        return token_model.Token(token_type_compiler.TokenType.IDENTIFIER, value, line)

    def __validate_end_of_source(self):
        if self.current_index >= self.stream_length:
            end_of_source_token = self.__create_end_of_source_token(self.current_line)
            self.tokens.append(end_of_source_token)
            raise exceptions_compiler.EndOfSourceError("No more data to read")
