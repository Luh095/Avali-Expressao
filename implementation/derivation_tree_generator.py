"""Implement a syntax analyzer"""
from token_model import Token
from tree import Tree

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
    
    def __is_expected_token(self, token, expected):
        if token.value == expected.value:
            return True
        return False

    def __get_token(self):
        return self.tokens[self.current_index]

    def __get_number(self):
        token = self.__get_token()
        if token.token_type == "number":
            self.current_index += 1
            return Tree(token, None, None)

    def __get_product(self):
        value_a = self.__get_number()

        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.value == "EOF":
            return value_a

        expected_token = Token("operator", "*")

        if self.__is_expected_token(token, expected_token):
            self.current_index += 1
            value_b = self.__get_product()
            return Tree(token, value_a, value_b)
        return value_a

    def __get_sum(self):
        value_a = self.__get_product()
        if value_a is None:
            return value_a

        token = self.__get_token()
        if token.value == "EOF":
            return value_a

        expected_token = Token("operator", "+")

        if self.__is_expected_token(token, expected_token):
            self.current_index += 1
            value_b = self.__get_sum()
            return Tree(token, value_a, value_b)

        return value_a

def parse(tree):
    if tree is not None:
        cargo = tree.cargo
        if cargo.token_type == "operator":
            left = parse(tree.left)
            right = parse(tree.right)
            return left + right if cargo.value == "+" else left * right
        
        if cargo.token_type == "number":
            return cargo.value
    
    return None

if __name__ == "__main__":
    syntax_analyzer = DerivationTreeGenerator([
        Token("number", 3),
        Token("operator", "+"),
        Token("number", 4),
        Token("operator", "*"),
        Token("number", 4),
        Token("end_of_source", "EOF")])
    derivation_tree = syntax_analyzer.create_tree()
    result = parse(derivation_tree)
    print(result)