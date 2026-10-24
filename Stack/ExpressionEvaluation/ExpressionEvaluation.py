"""Evaluate whitespace-separated postfix integers with a stack, O(n) time/space.

Tokens are unsigned ASCII integer literals or binary + - * /. No parentheses
or unary signs. Literals and every intermediate result are bounded by 10**9
in magnitude. Division truncates toward zero without floating-point arithmetic.
"""

MAX_VALUE = 1_000_000_000


def evaluate_postfix(expression):
    """Return an int; reject syntax, zero division, and range violations explicitly."""
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    if any(c not in "0123456789+-*/ \t\n\r\v\f" for c in expression):
        raise ValueError("invalid character")
    stack = []
    for token in expression.split():
        if all("0" <= c <= "9" for c in token):
            value = 0
            for char in token:
                value = value * 10 + ord(char) - ord("0")
                if value > MAX_VALUE:
                    raise OverflowError("integer literal exceeds 10**9")
            stack.append(value)
            continue
        if token not in ("+", "-", "*", "/") or len(stack) < 2:
            raise ValueError("invalid token or insufficient operands")
        right, left = stack.pop(), stack.pop()
        if token == "+":
            value = left + right
        elif token == "-":
            value = left - right
        elif token == "*":
            value = left * right
        else:
            if right == 0:
                raise ZeroDivisionError("division by zero")
            value = abs(left) // abs(right)
            if (left < 0) != (right < 0):
                value = -value
        if not -MAX_VALUE <= value <= MAX_VALUE:
            raise OverflowError("intermediate result exceeds +/-10**9")
        stack.append(value)
    if len(stack) != 1:
        raise ValueError("expression must leave exactly one result")
    return stack[0]


def main():
    result = evaluate_postfix("12 3 4 2 - * +")
    assert result == 18
    assert evaluate_postfix("0 7 - 3 /") == -2
    for expression, error in (("", ValueError), ("1 2", ValueError),
                              ("1 +", ValueError), ("1 0 /", ZeroDivisionError),
                              ("1000000000 1 +", OverflowError)):
        try:
            evaluate_postfix(expression)
        except error:
            pass
        else:
            raise AssertionError("invalid expression accepted")
    print(result)


if __name__ == "__main__":
    main()
