"""Minimum scalar multiplications for an ordered matrix chain.

For n matrices, O(n^3) time and O(n^2) space. dimensions describes
matrices dimensions[i] x dimensions[i+1]; [] or [d] has cost zero.
At most 101 dimensions, each integer 1..100000. These conservative limits
bound every parenthesization cost by 99*10^15, fitting signed 64-bit.
No matrices are actually multiplied and no parenthesization is returned.
"""


def matrix_chain_cost(dimensions):
    if not isinstance(dimensions, (list, tuple)) or len(dimensions) > 101:
        raise ValueError("at most 101 dimensions required")
    if any(type(d) is not int or not 1 <= d <= 100_000 for d in dimensions):
        raise ValueError("dimensions must be integers in [1, 100000]")
    n = len(dimensions) - 1
    if n <= 1:
        return 0
    best = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            best[left][right] = min(
                best[left][split] + best[split + 1][right]
                + dimensions[left] * dimensions[split + 1] * dimensions[right + 1]
                for split in range(left, right)
            )
    return best[0][n - 1]


def main():
    assert matrix_chain_cost([40, 20, 30, 10, 30]) == 26000
    assert matrix_chain_cost([]) == 0
    assert matrix_chain_cost([10]) == 0
    assert matrix_chain_cost([10, 20]) == 0
    assert matrix_chain_cost([100000, 100000, 100000]) == 10**15
    print("Minimum scalar multiplications:", matrix_chain_cost([40, 20, 30, 10, 30]))


if __name__ == "__main__":
    main()
