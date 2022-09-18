"""A"""
from token_model import Token
from derivation_tree_generator import DerivationTreeGenerator
from token_type import TokenType
from lexer import Lexer

class Parser:
    """A"""

    def parse(self, tree):
        """A"""
        if tree is not None:
            cargo = tree.cargo
            if cargo.token_type == TokenType.OPERATOR:
                left = self.parse(tree.left)
                right = self.parse(tree.right)

                if cargo.value in "+-":
                    return left + (right if cargo.value == "+" else (right * -1))
                if cargo.value in "*/":
                    return left * (right if cargo.value == "*" else (1/right))
            
            if cargo.token_type == TokenType.NUMBER:
                return cargo.value
        
        return None

if __name__ == "__main__":
    lexer = Lexer("(3 + 4) * 5")
    tokens = lexer.create_tokens()
    derivation_tree_generator = DerivationTreeGenerator(tokens)
    derivation_tree = derivation_tree_generator.create_tree()
    parser = Parser()
    result = parser.parse(derivation_tree)
    print(result)
