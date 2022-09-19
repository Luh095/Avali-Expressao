"""A"""

import math

class SymbolTable:
    """A"""

    def __init__(self):
        functions = Functions()
        sin_function_attributes = Attributes(SymbolType.FUNCTION, functions.sin)
        cos_function_attributes = Attributes(SymbolType.FUNCTION, functions.cos)
        tan_function_attributes = Attributes(SymbolType.FUNCTION, functions.tan)
        self.symbols = {
            "sin": sin_function_attributes,
            "cos": cos_function_attributes,
            "tan": tan_function_attributes
        }

    def add(self, symbol):
        self.symbols[symbol.key] = symbol.attributes

    def get_symbol_by_key(self, key):
        return self.symbols.get(key)

class Symbol:
    """A"""

    def __init__(self, key, attributes):
        self.key = key
        self.attributes = attributes

class Attributes:
    """A"""

    def __init__(self, symbol_type, value, line = None):
        self.symbol_type = symbol_type
        self.value = value
        self.line = line

class Functions:
    """A"""

    def __init__(self):
        self.sin = lambda value: math.sin(value)
        self.cos = lambda value: math.cos(value)
        self.tan = lambda value: math.tan(value)

class SymbolType:
    """A"""

    IDENTIFIER = 0
    FUNCTION = 1
