"""A"""
from token_model import Token
from derivation_tree_generator import DerivationTreeGenerator


class Parser:
    """A"""

    def parse(self, tree):
        """A"""
        if tree is not None:
            cargo = tree.cargo
            if cargo.token_type == "operator":
                left = self.parse(tree.left)
                right = self.parse(tree.right)
                return left + right if cargo.value == "+" else left * right
            
            if cargo.token_type == "number":
                return cargo.value
        
        return None

if __name__ == "__main__":
    derivation_tree_generator = DerivationTreeGenerator([
        Token("number", 3),
        Token("operator", "+"),
        Token("number", 4),
        Token("operator", "*"),
        Token("number", 4),
        Token("end_of_source", "EOF")])
    derivation_tree = derivation_tree_generator.create_tree()
    parser = Parser()
    result = parser.parse(derivation_tree)
    print(result)