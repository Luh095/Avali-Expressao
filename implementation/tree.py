from copyreg import constructor


"""Implements the tree algorithm"""

class Tree:
    """Represents a tree"""
    def __init__(self, cargo, left = None, right = None):
        self.cargo = cargo
        self.left = left
        self.right = right