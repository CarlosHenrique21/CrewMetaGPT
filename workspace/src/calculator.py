"""
Calculator engine for evaluating expressions in Reverse Polish Notation (RPN).
"""
from errors import EvaluationError


def evaluate_expression(rpn_tokens):
    """
    Evaluate the expression given as RPN tokens.

    Args:
        rpn_tokens (list): List of tokens in RPN order

    Returns:
        float: Evaluation result

    Raises:
        EvaluationError: If evaluation fails (e.g., division by zero)
    """
    stack = []
    for token in rpn_tokens:
        if token in ('+', '-', '*', '/'):
            if len(stack) < 2:
                raise EvaluationError("Insufficient operands")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise EvaluationError("Division by zero")
                result = a / b
            stack.append(result)
        else:
            try:
                num = float(token)
            except ValueError:
                raise EvaluationError(f"Invalid number: {token}")
            stack.append(num)

    if len(stack) != 1:
        raise EvaluationError("Invalid expression evaluation")

    return stack[0]
