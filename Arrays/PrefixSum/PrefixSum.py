"""O(n)-time/space prefix construction and O(1) half-open range queries.

Inputs are sequences of built-in integers, excluding bools. Sums have Python's
arbitrary precision. Queries expect an unmodified prefix_sums result.
"""


def prefix_sums(values):
    """Return [0, a[0], a[0]+a[1], ...]; empty input produces [0]."""
    result = [0]
    for value in values:
        if type(value) is not int:
            raise TypeError("values must be integers")
        result.append(result[-1] + value)
    return result


def range_sum(prefix, start, end):
    """Sum [start, end), requiring 0 <= start <= end < len(prefix).

    Validate the bounds and accessed entries, not the entire prefix array, so
    queries remain O(1). Empty ranges are valid and return zero.
    """
    if type(start) is not int or type(end) is not int:
        raise TypeError("range bounds must be integers")
    if not prefix or type(prefix[0]) is not int or prefix[0] != 0:
        raise ValueError("prefix must start with integer zero")
    if not 0 <= start <= end < len(prefix):
        raise ValueError("invalid half-open range")
    if type(prefix[start]) is not int or type(prefix[end]) is not int:
        raise TypeError("prefix entries must be integers")
    return prefix[end] - prefix[start]


if __name__ == "__main__":
    sums = prefix_sums([2, -1, 3, 5])
    assert sums == [0, 2, 1, 4, 9]
    assert range_sum(sums, 1, 3) == 2
    assert range_sum(sums, 4, 4) == 0
    assert range_sum(prefix_sums([]), 0, 0) == 0
    try:
        range_sum(sums, 3, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("reversed bounds must be rejected")
    print("Sum of [1, 3):", range_sum(sums, 1, 3))
