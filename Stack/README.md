# Stack algorithms

Each topic contains independent, matching `.py`, `.java`, and C99 `.c` files.
Python imports have no side effects. Java helpers are nested or private; the
public class matches the filename. Every entry point runs a deterministic demo
and self-check assertions, with no input required.

| Directory | Python API | Java static API | C API | Time / auxiliary space |
| --- | --- | --- | --- | --- |
| `InfixToPostfix` | `infix_to_postfix(expression) -> str` | `infixToPostfix(String)` | `infix_to_postfix(text, out, capacity)` | O(n) / O(n) |
| `ExpressionEvaluation` | `evaluate_postfix(expression) -> int` | `evaluatePostfix(String) -> long` | `evaluate_postfix(text, &result)` | O(n) / O(n) |
| `BalancedParentheses` | `is_balanced(text) -> bool` | `isBalanced(String)` | `is_balanced(text, &result)` | O(n) / O(depth), worst O(n) |

Here n is the number of input characters. C scratch arrays have fixed capacity
1024, so their physical storage is O(1024); the algorithms use stack space up to
the limits below. Conversion also produces O(n) output.

## Expression contracts

Infix grammar (ASCII digits and ASCII whitespace only):

```text
expression := term { ('+' | '-') term }
term       := atom { ('*' | '/') atom }
atom       := DIGITS | '(' expression ')'
DIGITS     := [0-9]+
```

Operators are binary and left-associative; multiplication/division bind more
tightly than addition/subtraction. Whitespace may separate tokens, not digits
within a literal. Leading zeros are allowed and preserved by conversion. No
variables, decimals, unary signs, implicit multiplication, or empty parentheses.

Evaluation consumes **postfix**, with every token separated by one or more ASCII
whitespace characters. Tokens are unsigned integer literals or `+ - * /`.
Conversion output can be passed directly to evaluation, but neither file imports
the other. For example, `12 + 3 * (4 - 2)` converts to `12 3 4 2 - * +`,
which evaluates to `18`. Negative results are allowed: `0 7 - 3 /` is `-2`.
Division truncates toward zero, never via floating point.

Literals are in **[0, 1,000,000,000]**, and every evaluated intermediate result
must be in **[-1,000,000,000, 1,000,000,000]**. These intentional educational
bounds make all languages agree and keep temporary products within C99
`long long` / Java `long` (at most 10^18). Conversion checks literal ranges, not
arithmetic; division by zero is rejected during evaluation. Empty expressions,
unmatched parentheses, invalid tokens, missing operands, and extra operands are
errors.

- Python: wrong argument type raises `TypeError`; syntax raises `ValueError`;
  range raises `OverflowError`; zero division raises `ZeroDivisionError`.
- Java: null raises `NullPointerException`; syntax raises
  `IllegalArgumentException`; range/zero division raises `ArithmeticException`.
- C: return `INFIX_OK` / `EVAL_OK` on success; otherwise `*_INVALID`,
  `*_CAPACITY`, `*_RANGE`, or `EVAL_DIV_ZERO`. Inputs must be NUL-terminated.
  At most 1024 input bytes; converter output capacity includes its NUL byte.
  A `2 * INFIX_LIMIT + 1` buffer suffices for any accepted input. Input and
  output must not overlap. Ignore conversion output after failure; evaluation
  leaves the result unchanged on failure. NULL arguments are invalid.

## Bracket contracts

Match `()`, `[]`, and `{}` with correct nesting. Ignore all other characters,
including quote marks: this is not a source-code parser. Empty text and text
without brackets are balanced; unmatched or crossed brackets return false.
Python rejects non-strings; Java rejects null. C returns `BRACKETS_INVALID` for
NULL arguments and `BRACKETS_CAPACITY` for more than 1024 simultaneously open
brackets; the result is unchanged on these errors. A mismatch returns
`BRACKETS_OK` with false, and may stop scanning immediately. No C allocations.

## Run a demo

From the relevant algorithm directory, substitute its matching name:

```text
python InfixToPostfix.py
javac InfixToPostfix.java
java -ea InfixToPostfix
cc -std=c99 -Wall -Wextra -pedantic InfixToPostfix.c -o InfixToPostfix
./InfixToPostfix
```

Use the corresponding `.exe` on Windows. Keep C assertions enabled (no
`-DNDEBUG`). Demo outputs: conversion `12 3 4 2 - * +`; evaluation `18`;
bracket check true (`True` in Python).

Python regression tests live in `tests/test_structures.py`; from the repository
root, use `python -m unittest discover -s tests -p test_structures.py` with the
shared `tests/_loader.py` included in this repository.
