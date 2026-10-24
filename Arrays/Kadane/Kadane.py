"""Maximum nonempty contiguous subarray sum; O(n) time, O(1) extra space.

Accepts a sequence of built-in integers (not bools); Python sums are unbounded.
The input is not modified. An empty sequence raises ValueError.
"""


def max_subarray(values):
    """Return the largest sum, including the largest element if all are negative."""
    if not values:
        raise ValueError("a nonempty sequence is required")
    if any(type(value) is not int for value in values):
        raise TypeError("values must be integers")
    current = best = values[0]
    for index in range(1, len(values)):
        current = max(values[index], current + values[index])
        best = max(best, current)
    return best


if __name__ == "__main__":
    sample = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    assert max_subarray(sample) == 6
    assert max_subarray([-8, -2, -5]) == -2
    assert max_subarray([0]) == 0
    try:
        max_subarray([])
    except ValueError:
        pass
    else:
        raise AssertionError("empty input must be rejected")
    print("Maximum subarray sum:", max_subarray(sample))
