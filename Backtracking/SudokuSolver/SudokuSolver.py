"""Solve a 9x9 Sudoku by MRV backtracking, trying digits in ascending order.

0 denotes an empty cell. Return a fresh solved board or None if no solution;
malformed boards or conflicting givens raise ValueError, even if fully filled.
Worst case O(81*9^e) time, O(81+e) space for e empty cells (e<=81).
Finds one solution; uniqueness is not checked. Hard puzzles can be expensive.
"""


def solve_sudoku(board):
    if not isinstance(board, (list, tuple)) or len(board) != 9:
        raise ValueError("board must have exactly 9 rows")
    if any(not isinstance(row, (list, tuple)) or len(row) != 9 for row in board):
        raise ValueError("each row must have exactly 9 cells")
    if any(type(cell) is not int or not 0 <= cell <= 9 for row in board for cell in row):
        raise ValueError("cells must be integers in [0,9]")
    result = [list(row) for row in board]
    rows, columns, boxes = [0] * 9, [0] * 9, [0] * 9
    for row in range(9):
        for column in range(9):
            value = result[row][column]
            if value == 0:
                continue
            bit = 1 << (value - 1)
            box = (row // 3) * 3 + column // 3
            if (rows[row] | columns[column] | boxes[box]) & bit:
                raise ValueError("conflicting Sudoku givens")
            rows[row] |= bit
            columns[column] |= bit
            boxes[box] |= bit

    def search():
        chosen = None
        fewest = 10
        for row in range(9):
            for column in range(9):
                if result[row][column] != 0:
                    continue
                box = (row // 3) * 3 + column // 3
                mask = 511 & ~(rows[row] | columns[column] | boxes[box])
                count = bin(mask).count("1")
                if count == 0:
                    return False
                if count < fewest:
                    chosen, fewest = (row, column, box, mask), count
        if chosen is None:
            return True
        row, column, box, mask = chosen
        for value in range(1, 10):
            bit = 1 << (value - 1)
            if not mask & bit:
                continue
            result[row][column] = value
            rows[row] |= bit
            columns[column] |= bit
            boxes[box] |= bit
            if search():
                return True
            rows[row] ^= bit
            columns[column] ^= bit
            boxes[box] ^= bit
            result[row][column] = 0
        return False

    return result if search() else None


def main():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    solved = solve_sudoku(puzzle)
    assert solved is not None and solved[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]
    assert puzzle[0][2] == 0
    assert solve_sudoku(solved) == solved
    impossible = [[0] * 9 for _ in range(9)]
    impossible[0] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    impossible[1][8] = 9
    assert solve_sudoku(impossible) is None
    invalid = [row[:] for row in solved]
    invalid[0][0] = invalid[0][1]
    try:
        solve_sudoku(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("fully filled invalid board accepted")
    for row in solved:
        print(*row)


if __name__ == "__main__":
    main()
