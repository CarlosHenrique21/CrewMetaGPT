"""
Expression parser for SimpleCalc CLI using Shunting Yard Algorithm.
"""
import re
from errors import ParseError

# Operator precedence and associativity definition
OPERATORS = {
    '+': {'precedence': 1, 'associativity': 'L'},
    '-': {'precedence': 1, 'associativity': 'L'},
    '*': {'precedence': 2, 'associativity': 'L'},
    '/': {'precedence': 2, 'associativity': 'L'},
}

NUMBER_PATTERN = re.compile(r'\d+(\.\d+)?')  # Integer or float number


def tokenize(expression):
    """Tokenize the arithmetic expression string into numbers, operators, and parentheses."""
    tokens = []
    i = 0
    length = len(expression)
    while i < length:
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char in OPERATORS or char in ('(', ')'):
            tokens.append(char)
            i += 1
        elif char.isdigit() or char == '.':
            match = NUMBER_PATTERN.match(expression, i)
            if match:
                tokens.append(match.group())
                i = match.end()
            else:
                raise ParseError(f"Invalid number starting at position {i}")
        else:
            raise ParseError(f"Invalid character '{char}' in expression")
    return tokens


def parse_expression(expression):
    """
    Parse the expression to Reverse Polish Notation (RPN) list of tokens.

    Args:
        expression (str): Arithmetic expression string

    Returns:
        list: Tokens in RPN order

    Raises:
        ParseError: If expression is invalid
    """
    tokens = tokenize(expression)
    output_queue = []
    operator_stack = []

    for token in tokens:
        if NUMBER_PATTERN.fullmatch(token):
            # Token is a number
            output_queue.append(token)
        elif token in OPERATORS:
            while operator_stack:
                top = operator_stack[-1]
                if top in OPERATORS:
                    top_op = OPERATORS[top]
                    token_op = OPERATORS[token]
                    if (top_op['precedence'] > token_op['precedence']) or \
                        (top_op['precedence'] == token_op['precedence'] and token_op['associativity'] == 'L'):
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                else:
                    break
            operator_stack.append(token)
        elif token == '(':  # Left parenthesis
            operator_stack.append(token)
        elif token == ')':  # Right parenthesis
            while operator_stack and operator_stack[-1] != '(':  
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ParseError("Mismatched parentheses")
            operator_stack.pop()  # Pop '('
        else:
            raise ParseError(f"Unknown token: {token}")

    while operator_stack:
        top = operator_stack.pop()
        if top in ('(', ')'):
            raise ParseError("Mismatched parentheses")
        output_queue.append(top)

    return output_queue
