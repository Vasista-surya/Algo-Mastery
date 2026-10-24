import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Enumerate column-per-row placements, n in [0,10].
 * O(n*n! + S*n) time, O(n) search space + O(S*n) output space.
 * n=0: one empty placement; n=2,3: empty list. All result arrays are independent.
 */
public class NQueens {
    public static List<int[]> solveNQueens(int n) {
        if (n < 0 || n > 10) throw new IllegalArgumentException("n must be in [0,10]");
        List<int[]> results = new ArrayList<>();
        search(0, new int[n], new boolean[n], new boolean[2 * n + 1],
                new boolean[2 * n + 1], results);
        return results;
    }

    private static void search(int row, int[] placement, boolean[] columns,
            boolean[] descending, boolean[] ascending, List<int[]> results) {
        int n = placement.length;
        if (row == n) {
            results.add(placement.clone());
            return;
        }
        for (int column = 0; column < n; column++) {
            int down = row - column + n, up = row + column;
            if (columns[column] || descending[down] || ascending[up]) continue;
            placement[row] = column;
            columns[column] = descending[down] = ascending[up] = true;
            search(row + 1, placement, columns, descending, ascending, results);
            columns[column] = descending[down] = ascending[up] = false;
        }
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("N-Queens self-check failed");
    }

    public static void main(String[] args) {
        check(solveNQueens(0).size() == 1 && solveNQueens(0).get(0).length == 0);
        check(solveNQueens(2).isEmpty());
        List<int[]> results = solveNQueens(4);
        check(results.size() == 2);
        check(Arrays.equals(results.get(0), new int[]{1, 3, 0, 2}));
        check(solveNQueens(8).size() == 92);
        for (int[] placement : results) System.out.println(Arrays.toString(placement));
    }
}
