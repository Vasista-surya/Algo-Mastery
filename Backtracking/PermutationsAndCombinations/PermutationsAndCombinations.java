import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Backtracking over positions, at most 8 ints; equal values retain duplicates.
 * Permutations: O(n*n!) time/output; combinations: O((k+1)*C(n,k)) time/output.
 * O(n) auxiliary space. Empty permutation/k=0 yields one empty array; k>n none.
 */
public class PermutationsAndCombinations {
    private static void validate(int[] items) {
        if (items == null || items.length > 8) {
            throw new IllegalArgumentException("at most 8 integers required");
        }
    }

    public static List<int[]> permutations(int[] items) {
        validate(items);
        List<int[]> results = new ArrayList<>();
        permute(items, new boolean[items.length], new int[items.length], 0, results);
        return results;
    }

    private static void permute(int[] items, boolean[] used, int[] path, int depth,
            List<int[]> results) {
        if (depth == path.length) {
            results.add(path.clone());
            return;
        }
        for (int index = 0; index < items.length; index++) {
            if (used[index]) continue;
            used[index] = true;
            path[depth] = items[index];
            permute(items, used, path, depth + 1, results);
            used[index] = false;
        }
    }

    public static List<int[]> combinations(int[] items, int k) {
        validate(items);
        if (k < 0) throw new IllegalArgumentException("k must be nonnegative");
        List<int[]> results = new ArrayList<>();
        if (k <= items.length) combine(items, new int[k], 0, 0, results);
        return results;
    }

    private static void combine(int[] items, int[] path, int start, int depth,
            List<int[]> results) {
        if (depth == path.length) {
            results.add(path.clone());
            return;
        }
        int last = items.length - (path.length - depth);
        for (int index = start; index <= last; index++) {
            path[depth] = items[index];
            combine(items, path, index + 1, depth + 1, results);
        }
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Enumeration self-check failed");
    }

    public static void main(String[] args) {
        check(permutations(new int[0]).size() == 1);
        check(permutations(new int[]{1, 1}).size() == 2);
        check(permutations(new int[]{1, 2, 3}).size() == 6);
        List<int[]> pairs = combinations(new int[]{1, 2, 3}, 2);
        check(pairs.size() == 3 && Arrays.equals(pairs.get(1), new int[]{1, 3}));
        check(combinations(new int[0], 0).size() == 1);
        check(combinations(new int[]{1}, 2).isEmpty());
        for (int[] pair : pairs) System.out.println(Arrays.toString(pair));
    }
}
