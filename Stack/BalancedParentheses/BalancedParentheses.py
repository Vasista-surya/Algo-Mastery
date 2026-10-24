"""Match (), [], and {} with a stack in O(n) time and O(n) space.

Non-bracket characters are ignored (including quotes; this is not a parser).
Empty text is balanced. A non-string argument raises TypeError.
"""


def is_balanced(text):
    """Return whether every bracket has a correctly nested matching partner."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack


def main():
    assert is_balanced("")
    assert is_balanced("a * (b + [c - {d}])")
    assert not is_balanced("([)]")
    assert not is_balanced(")")
    assert not is_balanced("((")
    print(is_balanced("{[()]}"))


if __name__ == "__main__":
    main()
