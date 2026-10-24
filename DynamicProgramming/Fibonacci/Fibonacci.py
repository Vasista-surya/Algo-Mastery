"""Iterative Fibonacci DP: O(n) additions, O(1) integer slots.

Python integers are exact; bit space is O(n), bit time O(n^2). Accept
0 <= n <= 10_000 as a practical limit. F(0) = 0, F(1) = 1.
"""


def fibonacci(n):
    """Return F(n); reject non-integers (including bool) and out-of-range n."""
    if type(n) is not int or not 0 <= n <= 10_000:
        raise ValueError("n must be an integer in [0, 10000]")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    assert fibonacci(93) == 12200160415121876738
    try:
        fibonacci(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative index accepted")
    print("F(10) =", fibonacci(10))


if __name__ == "__main__":
    main()
