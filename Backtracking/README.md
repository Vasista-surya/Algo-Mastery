# Backtracking

Standalone Python, Java, and C99 examples explore candidate choices and undo
them when returning from recursion. All demos use small deterministic inputs,
check expected results, and require no interactive input.

## APIs, results, and limits

| Directory | Python | Java static method | Result / constraints |
| --- | --- | --- | --- |
| `NQueens` | `n_queens(n)` | `NQueens.solveNQueens(int n)` | All column-per-row placements, n in `0..10` |
| `SudokuSolver` | `solve_sudoku(board)` | `SudokuSolver.solveSudoku(int[][] board)` | A fresh solved 9x9 board, or `None` / `null` for no solution |
| `PermutationsAndCombinations` | `permutations(items)` | `PermutationsAndCombinations.permutations(int[])` | All positional permutations, at most 8 integers |
| `PermutationsAndCombinations` | `combinations(items, k)` | `PermutationsAndCombinations.combinations(int[], int k)` | All increasing-index selections of k positions |

Python enumeration results are lists of tuples; Java returns `List<int[]>`
with independent arrays. Traversal order follows ascending columns, Sudoku
digits, or original input indices. Inputs are not modified. Invalid Python
inputs raise `ValueError`; invalid Java inputs throw `IllegalArgumentException`.
Python accepts list/tuple containers and rejects booleans/non-integer values.

- **N-Queens:** placement[row] is the column of its queen. n=0 has one empty
  placement, n=1 has `(0,)`, and n=2 or 3 has no solutions. The limit of 10
  keeps full materialization small (724 solutions at n=10). Columns and both
  diagonals are tracked during search. For S solutions, time is bounded by
  O(n*n! + S*n); auxiliary space O(n), plus O(S*n) materialized output.
- **Sudoku:** exactly 9 rows of 9 integers in `0..9`; zero is empty. Every given
  is checked for row, column, and 3x3-box conflicts **before** searching. A
  completely filled invalid board is rejected, not mistaken for a solution.
  A conflict-free but unsatisfiable board returns the distinct no-solution
  result. An all-zero 9x9 board is valid; an empty outer list is invalid.
  Minimum-remaining-values (MRV) cell choice and digit masks reduce branching.
  One solution is returned; uniqueness is not established. With e empty cells,
  worst-case time O(81*9^e), space O(81+e), e<=81. Hard puzzles may take time.
- **Permutations/combinations:** positions are distinct, even for equal values.
  Thus `[1,1]` has two identical-valued permutations, and duplicate-valued
  combinations may also repeat. Empty permutations and k=0 each yield one
  empty tuple; k>n yields no tuples. Negative k is invalid. No set deduplication
  or sorting is performed. Permutations take O(n*n!) time/output storage;
  combinations O((k+1)*C(n,k)), plus O(n) validation. Search space is O(n).
  At most 8!=40320 permutations are materialized; C streams instead.

## C99 APIs and ownership

```c
typedef void (*QueensVisitor)(const int *placement, int n, void *context);
int n_queens(int n, QueensVisitor visit, void *context, size_t *count);

int solve_sudoku(const int *input, int cells, int *output, int capacity);

typedef void (*TupleVisitor)(const int *tuple, int length, void *context);
int permutations(const int *items, int n, TupleVisitor visit,
                 void *context, size_t *count);
int combinations(const int *items, int n, int k, TupleVisitor visit,
                 void *context, size_t *count);
```

- Enumeration returns `1` on success, `0` for invalid inputs. `count` is required
  and remains unchanged on error. Null visitors count solutions without emitting
  them. Visitor tuples are borrowed **only for the duration of that call**;
  copy them if retaining results. Items must remain unchanged during callbacks.
  `items == NULL` is permitted only for n=0. Counts fit `size_t` under the limits.
- Sudoku uses **flat row-major arrays**, not pointers to rows. `cells` must equal
  81 and `capacity` must be at least 81, with non-null input/output. Returns
  `1` solved, `0` unsatisfiable, `-1` malformed input, conflicting givens, or
  insufficient output capacity. Only success changes the output. Input/output
  may alias because solving happens on an internal copy.
- Negative dimensions are rejected before indexing. These implementations use
  bounded local arrays and no heap allocations. Caller-provided counts and
  capacities must reflect actual buffers. C99 on ordinary 32-bit-or-wider
  `int`/`size_t` platforms is the target.

## Run and reuse

From the repository root (substitute another algorithm name as needed):

```sh
python Backtracking/NQueens/NQueens.py
javac Backtracking/NQueens/NQueens.java
java -cp Backtracking/NQueens NQueens
cc -std=c99 -Wall -Wextra -pedantic Backtracking/NQueens/NQueens.c -o queens_demo
./queens_demo
python -m unittest discover -s tests -p test_optimization.py
```

Python functions can be imported without running demos. Java helper classes are
nested within their public class, and checks throw `AssertionError` without
requiring `-ea`. C demos are guarded by `#ifndef ALGO_NO_MAIN` for reuse in a
consumer or separate object file. Keep C `NDEBUG` and Python `-O` off when
running demo assertions. Tests use the shared `tests/_loader.py`.
Run `python tools/check_examples.py` to also check every Java and C demo.
