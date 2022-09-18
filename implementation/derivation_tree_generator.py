"""Implement a syntax analyzer"""
from token_type import TokenType
from token_model import Token
from tree import Tree
from exceptions import ExpressionError

class DerivationTreeGenerator:
    """Represents a sintax analyzer"""
    def __init__(self, tokens):
        self.current_index = 0
        self.tokens = tokens

    def create_tree(self):
        """Create the derivation tree"""
        return self.__expression()
        
    def __expression(self):
        return self.__get_sum()

    def __get_token(self):
        return self.tokens[self.current_index]

    def __get_number(self):
        token = self.__get_token()
        if token.token_type == TokenType.OPEN_PARENTHESE:
            self.current_index += 1
            expression = self.__expression()
            next_token = self.__get_token()
            if not next_token.token_type == TokenType.CLOSE_PARENTHESE:
                raise ExpressionError("Unbalanced parentheses")
            self.current_index += 1
            return expression
        if token.token_type == TokenType.NUMBER:
            self.current_index += 1
            return Tree(token, None, None)

    def __get_product(self):
        value_a = self.__get_number()

        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.token_type == TokenType.END_OF_SOURCE:
            return value_a

        if token.token_type == TokenType.OPERATOR and token.value in "*/":
            self.current_index += 1
            value_b = self.__get_product()
            return Tree(token, value_a, value_b)
        return value_a

    def __get_sum(self):
        value_a = self.__get_product()
        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.token_type == TokenType.END_OF_SOURCE:
            return value_a

        if token.token_type == TokenType.OPERATOR and token.value in "+-":
            self.current_index += 1
            value_b = self.__get_sum()
            return Tree(token, value_a, value_b)

        return value_a

def parse(tree):
    if tree is not None:
        cargo = tree.cargo
        if cargo.token_type == TokenType.OPERATOR:
            left = parse(tree.left)
            right = parse(tree.right)
            return left + right if cargo.value == "+" else left * right
        
        if cargo.token_type == TokenType.NUMBER:
            return cargo.value
    
    return None

# if __name__ == "__main__":
#     syntax_analyzer = DerivationTreeGenerator([
#         Token(TokenType.OPEN_PARENTHESE, "("),
#         Token(TokenType.NUMBER, 3),
#         Token(TokenType.OPERATOR, "+"),
#         Token(TokenType.NUMBER, 4),
#         Token(TokenType.CLOSE_PARENTHESE, ")"),
#         Token(TokenType.OPERATOR, "*"),
#         Token(TokenType.NUMBER, 5),
#         Token(TokenType.END_OF_SOURCE, "EOF")])
#     derivation_tree = syntax_analyzer.create_tree()
#     result = parse(derivation_tree)
#     print(result)
