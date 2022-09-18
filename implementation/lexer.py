"""A"""
import re
from token_model import Token
from exceptions import InvalidParameterError, EndOfSourceError, UnexpectedTokenError
from token_type import TokenType

class Lexer:
    """A"""

    def __init__(self, stream):
        if stream is None or stream == "":
            raise InvalidParameterError("stream cannot be empty or null")
        self.stream = stream
        self.stream_length = len(stream)

        self.current_index = 0
        self.tokens = []

        self.number_regular_expression = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")
        self.operator_regular_expression = re.compile(r"^[\+\-\*]{1}$")
        self.parentheses_regular_expression = re.compile(r"^\($|^\)$")
    
    def create_tokens(self):
        try:
            while True:
                if self.current_index >= self.stream_length:
                    end_of_source_token = self.__create_end_of_source_token()
                    self.tokens.append(end_of_source_token)
                    raise EndOfSourceError("No more data to read")

                character = self.__get_character()
                self.current_index += 1
                while character in " \t\n\r":
                    self.__validate_end_of_source()
                    character = self.__get_character()
                    self.current_index += 1

                try:
                    if character == "(":
                        self.tokens.append(self.__create_open_parenthese_token())
                        continue
                    elif character == ")":
                        self.tokens.append(self.__create_close_parenthese_token())
                        continue

                    index_of_white_space = self.stream.index(" ", self.current_index)
                    end_index = index_of_white_space - 1 if self.stream[index_of_white_space - 1] == ")" else index_of_white_space

                    lexeme = self.stream[self.current_index - 1 : end_index]

                    operator_match = self.operator_regular_expression.match(lexeme)
                    if operator_match is not None:
                        self.tokens.append(self.__create_operator_token(lexeme))
                        self.current_index += len(lexeme) - 1
                        continue
                    number_match = self.number_regular_expression.match(lexeme)
                    if number_match is not None:
                        self.tokens.append(self.__create_number_token(lexeme))
                        self.current_index += len(lexeme) - 1
                        continue

                    raise UnexpectedTokenError(f"Unexpected Token: {lexeme}")

                except ValueError as exception:
                    end_index = None
                    try:
                        end_index = self.stream.index(")", self.current_index)
                    except ValueError:
                        end_index = None

                    has_close_parenthese = True if end_index is not None else False
                    lexeme = self.stream[self.current_index - 1 : end_index] if has_close_parenthese else self.stream[self.current_index -1 :]

                    operator_match = self.operator_regular_expression.match(lexeme)
                    if operator_match is not None:
                        self.tokens.append(self.__create_operator_token(lexeme))
                        self.current_index += len(lexeme) - 1
                        continue
                    number_match = self.number_regular_expression.match(lexeme)
                    if number_match is not None:
                        self.tokens.append(self.__create_number_token(lexeme))
                        self.current_index += len(lexeme) -1
                        continue

                    raise UnexpectedTokenError(f"Unexpected Token: {lexeme}") from exception

        except EndOfSourceError:
            return self.tokens

    def __get_character(self):
        return self.stream[self.current_index]

    def __create_end_of_source_token(self):
        return Token(TokenType.END_OF_SOURCE, "EOF")

    def __create_operator_token(self, value):
        return Token(TokenType.OPERATOR, value)

    def __create_number_token(self, value):
        return Token(TokenType.NUMBER, float(value))

    def __create_open_parenthese_token(self):
        return Token(TokenType.OPEN_PARENTHESE, "(")

    def __create_close_parenthese_token(self):
        return Token(TokenType.CLOSE_PARENTHESE, ")")

    def __validate_end_of_source(self):
        if self.current_index >= self.stream_length:
            end_of_source_token = self.__create_end_of_source_token()
            self.tokens.append(end_of_source_token)
            raise EndOfSourceError("No more data to read")

# if __name__ == "__main__":
#     lexer = Lexer("(3 + 4) * 5")
#     tokens = lexer.create_tokens()
#     count = 0
#     token = tokens[count]
#     print(token.value)
#     count += 1
#     while token.token_type != TokenType.END_OF_SOURCE:
#         token = tokens[count]
#         count += 1
#         print(token.value)
