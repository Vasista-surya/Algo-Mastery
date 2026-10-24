"""Backtracking enumeration over input positions, with at most 8 integers.

Duplicates are deliberately retained when equal values occupy different
positions. Permutations cost O(n*n!) time/output space; combinations cost
O((k+1)*C(n,k)) time/output space. Auxiliary search space is O(n).
Empty permutation and k=0 each yield [()]; k>n yields []. Negative k is invalid.
"""


def _validate(items):
    if not isinstance(items, (list, tuple)) or len(items) > 8:
        raise ValueError("a list/tuple of at most 8 integers required")
    if any(type(item) is not int for item in items):
        raise ValueError("items must be integers")


def permutations(items):
    """Return tuples in input-index traversal order without mutating items."""
    _validate(items)
    results, path = [], []
    used = [False] * len(items)

    def search():
        if len(path) == len(items):
            results.append(tuple(path))
            return
        for index, item in enumerate(items):
            if not used[index]:
                used[index] = True
                path.append(item)
                search()
                path.pop()
                used[index] = False

    search()
    return results


def combinations(items, k):
    """Return length-k tuples, choosing positions in increasing order."""
    _validate(items)
    if type(k) is not int or k < 0:
        raise ValueError("k must be a nonnegative integer")
    if k > len(items):
        return []
    results, path = [], []

    def search(start):
        if len(path) == k:
            results.append(tuple(path))
            return
        for index in range(start, len(items) - (k - len(path)) + 1):
            path.append(items[index])
            search(index + 1)
            path.pop()

    search(0)
    return results


def main():
    assert permutations([]) == [()]
    assert permutations([1, 1]) == [(1, 1), (1, 1)]
    assert len(permutations([1, 2, 3])) == 6
    assert combinations([1, 2, 3], 2) == [(1, 2), (1, 3), (2, 3)]
    assert combinations([], 0) == [()]
    assert combinations([1], 2) == []
    print("Permutations:", permutations([1, 2, 3]))
    print("Combinations:", combinations([1, 2, 3], 2))


if __name__ == "__main__":
    main()
