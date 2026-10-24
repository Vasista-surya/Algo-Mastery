"""Enumerate N-Queens as tuples of column indices, one per row.

Backtracking with column/diagonal sets: O(n*n! + S*n) time, O(n) auxiliary
space plus O(S*n) returned placements. Limit n to 0..10; enumeration is
exponential. n=0 has one empty placement; n=2 or n=3 has no solutions.
"""


def n_queens(n):
    if type(n) is not int or not 0 <= n <= 10:
        raise ValueError("n must be an integer in [0, 10]")
    solutions, placement = [], []
    columns, descending, ascending = set(), set(), set()

    def search(row):
        if row == n:
            solutions.append(tuple(placement))
            return
        for column in range(n):
            if column in columns or row - column in descending or row + column in ascending:
                continue
            placement.append(column)
            columns.add(column)
            descending.add(row - column)
            ascending.add(row + column)
            search(row + 1)
            ascending.remove(row + column)
            descending.remove(row - column)
            columns.remove(column)
            placement.pop()

    search(0)
    return solutions


def main():
    assert n_queens(0) == [()]
    assert n_queens(1) == [(0,)]
    assert n_queens(2) == []
    assert n_queens(4) == [(1, 3, 0, 2), (2, 0, 3, 1)]
    assert len(n_queens(8)) == 92
    print("4-Queens placements:", n_queens(4))


if __name__ == "__main__":
    main()
