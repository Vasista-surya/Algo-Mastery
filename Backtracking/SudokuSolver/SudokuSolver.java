import java.util.Arrays;

/** 9x9 Sudoku, 0 denotes empty. MRV backtracking, ascending digit order.
 * Returns a fresh solved board, null for no solution; invalid givens/shape throw.
 * Worst O(81*9^e) time, O(81+e) space, e<=81 empty cells. No uniqueness check.
 */
public class SudokuSolver {
    private static final class Search {
        final int[][] board = new int[9][9];
        final int[] rows = new int[9], columns = new int[9], boxes = new int[9];

        Search(int[][] input) {
            if (input == null || input.length != 9) {
                throw new IllegalArgumentException("board must have 9 rows");
            }
            for (int row = 0; row < 9; row++) {
                if (input[row] == null || input[row].length != 9) {
                    throw new IllegalArgumentException("rows must have 9 cells");
                }
                for (int column = 0; column < 9; column++) {
                    int value = input[row][column];
                    if (value < 0 || value > 9) {
                        throw new IllegalArgumentException("cells must be in [0,9]");
                    }
                    board[row][column] = value;
                    if (value == 0) continue;
                    int bit = 1 << (value - 1), box = (row / 3) * 3 + column / 3;
                    if (((rows[row] | columns[column] | boxes[box]) & bit) != 0) {
                        throw new IllegalArgumentException("conflicting Sudoku givens");
                    }
                    rows[row] |= bit;
                    columns[column] |= bit;
                    boxes[box] |= bit;
                }
            }
        }

        boolean solve() {
            int chosenRow = -1, chosenColumn = -1, chosenBox = -1, chosenMask = 0;
            int fewest = 10;
            for (int row = 0; row < 9; row++) {
                for (int column = 0; column < 9; column++) {
                    if (board[row][column] != 0) continue;
                    int box = (row / 3) * 3 + column / 3;
                    int mask = 511 & ~(rows[row] | columns[column] | boxes[box]);
                    int count = Integer.bitCount(mask);
                    if (count == 0) return false;
                    if (count < fewest) {
                        chosenRow = row; chosenColumn = column; chosenBox = box;
                        chosenMask = mask; fewest = count;
                    }
                }
            }
            if (chosenRow == -1) return true;
            for (int value = 1; value <= 9; value++) {
                int bit = 1 << (value - 1);
                if ((chosenMask & bit) == 0) continue;
                board[chosenRow][chosenColumn] = value;
                rows[chosenRow] |= bit;
                columns[chosenColumn] |= bit;
                boxes[chosenBox] |= bit;
                if (solve()) return true;
                rows[chosenRow] ^= bit;
                columns[chosenColumn] ^= bit;
                boxes[chosenBox] ^= bit;
                board[chosenRow][chosenColumn] = 0;
            }
            return false;
        }
    }

    public static int[][] solveSudoku(int[][] board) {
        Search search = new Search(board); // Validate ALL givens before searching.
        return search.solve() ? search.board : null;
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Sudoku self-check failed");
    }

    public static void main(String[] args) {
        int[][] puzzle = {
            {5,3,0,0,7,0,0,0,0}, {6,0,0,1,9,5,0,0,0}, {0,9,8,0,0,0,0,6,0},
            {8,0,0,0,6,0,0,0,3}, {4,0,0,8,0,3,0,0,1}, {7,0,0,0,2,0,0,0,6},
            {0,6,0,0,0,0,2,8,0}, {0,0,0,4,1,9,0,0,5}, {0,0,0,0,8,0,0,7,9}
        };
        int[][] solved = solveSudoku(puzzle);
        check(solved != null && Arrays.equals(solved[0], new int[]{5,3,4,6,7,8,9,1,2}));
        check(puzzle[0][2] == 0);
        check(Arrays.deepEquals(solveSudoku(solved), solved));
        int[][] impossible = new int[9][9];
        impossible[0] = new int[]{1,2,3,4,5,6,7,8,0};
        impossible[1][8] = 9;
        check(solveSudoku(impossible) == null);
        int[][] invalid = solveSudoku(solved);
        invalid[0][0] = invalid[0][1];
        boolean rejected = false;
        try { solveSudoku(invalid); } catch (IllegalArgumentException ex) { rejected = true; }
        check(rejected);
        for (int[] row : solved) System.out.println(Arrays.toString(row));
    }
}
