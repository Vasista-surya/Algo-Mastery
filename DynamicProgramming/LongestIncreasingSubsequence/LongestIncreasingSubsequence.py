"""Strict LIS length using binary-searched tails: O(n log n) time, O(n) space.

Accept a list/tuple of at most 100000 integers. Duplicates do not extend
the subsequence; empty input returns zero. The input is not modified.
"""
from bisect import bisect_left


def lis_length(values):
    if not isinstance(values, (list, tuple)) or len(values) > 100_000:
        raise ValueError("at most 100000 integers required")
    if any(type(value) is not int for value in values):
        raise ValueError("values must be integers")
    tails = []
    for value in values:
        index = bisect_left(tails, value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value
    return len(tails)


def main():
    assert lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_length([]) == 0
    assert lis_length([2, 2, 2]) == 1
    assert lis_length([-3, -2, -1]) == 3
    print("LIS length:", lis_length([10, 9, 2, 5, 3, 7, 101, 18]))


if __name__ == "__main__":
    main()
