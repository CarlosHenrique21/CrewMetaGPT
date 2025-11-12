"""
Custom exceptions for SimpleCalc CLI.
"""

class SimpleCalcError(Exception):
    """Base class for exceptions in SimpleCalc."""
    pass

class ParseError(SimpleCalcError):
    """Exception raised for errors during parsing expressions."""
    def __init__(self, message="Invalid expression"):
        self.message = message
        super().__init__(self.message)

class EvaluationError(SimpleCalcError):
    """Exception raised for errors during evaluation of expressions."""
    def __init__(self, message="Error during evaluation"):
        self.message = message
        super().__init__(self.message)
