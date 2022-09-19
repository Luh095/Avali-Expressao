"""A"""
import types
import exceptions_compiler
import symbol_table_compiler
import token_type_compiler

class Parser:
    """A"""
    
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def parse(self, tree):
        """A"""
        if tree is not None:
            cargo = tree.cargo
            if cargo is None:
                left = self.parse(tree.left)
                right = self.parse(tree.right)

                if isinstance(left, types.FunctionType):
                    return left(right)

                return left if left is not None else right
            if cargo.token_type == token_type_compiler.TokenType.OPERATOR:
                left = self.parse(tree.left)
                right = self.parse(tree.right)

                if cargo.value == "=":
                    if isinstance(left, type(0)):
                        raise exceptions_compiler.ParserError(f"Unable to assign a new value to an identifier in line {cargo.line}")
                    attributes = symbol_table_compiler.Attributes("identifier", right, cargo.line)
                    symbol = symbol_table_compiler.Symbol(left, attributes)
                    self.symbol_table.add(symbol)
                    return None

                if isinstance(left, str):
                    raise exceptions_compiler.ParserError(f"The identifier {left} was not assigned a value in line {cargo.line}")

                if cargo.value in "+-":
                    return left + (right if cargo.value == "+" else right * -1)
            
                if cargo.value == "*" or cargo.value == "/":
                    return left * (right if cargo.value == "*" else 1/right)

                if cargo.value == "**":
                    return left ** right
            
            if cargo.token_type == token_type_compiler.TokenType.NUMBER:
                return cargo.value
        
            if cargo.token_type == token_type_compiler.TokenType.IDENTIFIER:
                identifier_value = self.symbol_table.get_symbol_by_key(cargo.value)
                if identifier_value is None:
                    return cargo.value
                else:
                    return identifier_value.value

        return None
