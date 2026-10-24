"""Maximum sum of exactly width consecutive integers; O(n) time, O(1) space.

Input is an unmodified sequence of built-in ints (not bools). Python integers
are unbounded. Require integer 1 <= width <= len(values), so empty input fails.
"""


def max_window_sum(values, width):
    """Return a fixed-width maximum, including negative maxima."""
    if type(width) is not int:
        raise TypeError("width must be an integer")
    if not 1 <= width <= len(values):
        raise ValueError("width must be between 1 and the input length")
    if any(type(value) is not int for value in values):
        raise TypeError("values must be integers")
    current = sum(values[i] for i in range(width))
    best = current
    for i in range(width, len(values)):
        current = current - values[i - width] + values[i]
        best = max(best, current)
    return best


if __name__ == "__main__":
    sample = [2, -1, 3, 5, -2]
    assert max_window_sum(sample, 2) == 8
    assert max_window_sum([-5, -2, -8], 2) == -7
    assert max_window_sum(sample, len(sample)) == 7
    try:
        max_window_sum([], 1)
    except ValueError:
        pass
    else:
        raise AssertionError("an empty input has no positive-width window")
    print("Maximum width-2 window sum:", max_window_sum(sample, 2))
