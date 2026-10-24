"""Sorted two-sum with distinct zero-based indices; O(n) time, O(1) space.

Accept a nondecreasing sequence of built-in ints and an integer target (no
bools). Validate sortedness, leave input unchanged, and use unbounded sums.
"""


def two_sum_sorted(values, target):
    """Return (left, right) or None. Duplicates are allowed.

    Starting at both ends, move left for too-small sums and right for too-large
    sums; return the first equality encountered (not necessarily lexicographic).
    Empty and singleton inputs return None; unsorted inputs raise ValueError.
    """
    if type(target) is not int or any(type(value) is not int for value in values):
        raise TypeError("values and target must be integers")
    if any(values[i - 1] > values[i] for i in range(1, len(values))):
        raise ValueError("values must be sorted in nondecreasing order")
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left] + values[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None


if __name__ == "__main__":
    sample = [-4, -1, 0, 3, 5]
    assert two_sum_sorted(sample, 2) == (1, 3)
    assert two_sum_sorted([2, 2], 4) == (0, 1)
    assert two_sum_sorted([], 0) is None
    assert two_sum_sorted([2], 4) is None
    try:
        two_sum_sorted([2, 1], 3)
    except ValueError:
        pass
    else:
        raise AssertionError("unsorted input must be rejected")
    print("Indices for sum 2:", two_sum_sorted(sample, 2))
