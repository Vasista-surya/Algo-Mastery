"""Convert validated integer infix expressions with the shunting-yard algorithm.

Grammar: expr = term {('+'|'-') term}; term = atom {('*'|'/') atom};
atom = DIGITS | '(' expr ')'. ASCII whitespace is allowed between tokens.
No unary operators or implicit multiplication. Literals are in [0, 10**9].
Time O(n), auxiliary/output space O(n), where n is the input length.
"""

MAX_VALUE = 1_000_000_000
WHITESPACE = " \t\n\r\v\f"


def infix_to_postfix(expression):
    """Return space-separated postfix; raise ValueError/OverflowError on errors."""
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    output, operators = [], []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    need_operand = True
    i = 0
    while i < len(expression):
        char = expression[i]
        if char in WHITESPACE:
            i += 1
            continue
        if "0" <= char <= "9":
            if not need_operand:
                raise ValueError("missing operator")
            start, value = i, 0
            while i < len(expression) and "0" <= expression[i] <= "9":
                value = value * 10 + ord(expression[i]) - ord("0")
                if value > MAX_VALUE:
                    raise OverflowError("integer literal exceeds 10**9")
                i += 1
            output.append(expression[start:i])
            need_operand = False
            continue
        if char == "(" and need_operand:
            operators.append(char)
        elif char == ")" and not need_operand:
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            if not operators:
                raise ValueError("unmatched closing parenthesis")
            operators.pop()
        elif char in precedence and not need_operand:
            while (operators and operators[-1] != "(" and
                   precedence[operators[-1]] >= precedence[char]):
                output.append(operators.pop())
            operators.append(char)
            need_operand = True
        else:
            raise ValueError("invalid token or missing operand/operator")
        i += 1
    if need_operand:
        raise ValueError("empty or incomplete expression")
    while operators:
        char = operators.pop()
        if char == "(":
            raise ValueError("unmatched opening parenthesis")
        output.append(char)
    return " ".join(output)


def main():
    result = infix_to_postfix("12 + 3 * (4 - 2)")
    assert result == "12 3 4 2 - * +"
    assert infix_to_postfix("8 / 2 / 2") == "8 2 / 2 /"
    for invalid in ("", "()", "1 2", "1+", "(1", "1)", "-2"):
        try:
            infix_to_postfix(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid expression accepted")
    print(result)


if __name__ == "__main__":
    main()
