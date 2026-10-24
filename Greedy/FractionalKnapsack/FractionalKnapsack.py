"""Fractional (divisible-item) knapsack with exact rational arithmetic.

Items are (value, weight) integer pairs, value >= 0, weight > 0. Capacity
is a nonnegative integer. Return (Fraction total, list of Fraction shares
in ORIGINAL item order). Empty/zero capacity -> zero value and zero shares.
Zero-value items are skipped. Ratio ties use input order; no input mutation.
O(N log N) comparisons and O(N) space, excluding big-integer arithmetic cost.
"""

from fractions import Fraction


def fractional_knapsack(items, capacity):
    if type(capacity) is not int or capacity < 0:
        raise ValueError("capacity must be a nonnegative integer")
    items = list(items)
    for value, weight in items:
        if type(value) is not int or value < 0 or type(weight) is not int or weight <= 0:
            raise ValueError("integer value >= 0 and weight > 0 required")
    order = sorted(range(len(items)), key=lambda i: (-Fraction(*items[i]), i))
    shares = [Fraction(0)] * len(items)
    total = Fraction(0)
    for i in order:
        value, weight = items[i]
        if capacity == 0 or value == 0:
            break
        taken = min(capacity, weight)
        shares[i] = Fraction(taken, weight)
        total += shares[i] * value
        capacity -= taken
    return total, shares


if __name__ == "__main__":
    result = fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50)
    assert result == (240, [1, 1, Fraction(2, 3)])
    assert fractional_knapsack([], 5) == (0, [])
    assert fractional_knapsack([(8, 3)], 1) == (Fraction(8, 3), [Fraction(1, 3)])
    try:
        fractional_knapsack([(1, 0)], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero weight accepted")
    print("Value and shares:", result)
