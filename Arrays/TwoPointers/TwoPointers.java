import java.util.Arrays;
import java.util.Objects;

/** Sorted two-sum: O(n) time (including validation), O(1) extra space.
 * Return distinct zero-based indices or null; input is unchanged.
 * Duplicates are valid. Empty/singleton arrays have no pair. Sums of int
 * elements are widened to long before addition; target can be any long.
 */
public class TwoPointers {
    public static int[] twoSumSorted(int[] values, long target) {
        Objects.requireNonNull(values, "values");
        for (int i = 1; i < values.length; i++) {
            if (values[i - 1] > values[i]) {
                throw new IllegalArgumentException("input must be nondecreasing");
            }
        }
        int left = 0, right = values.length - 1;
        while (left < right) {
            long sum = (long) values[left] + values[right];
            if (sum == target) return new int[] {left, right};
            if (sum < target) left++;
            else right--;
        }
        return null;
    }

    public static void main(String[] args) {
        int[] sample = {-4, -1, 0, 3, 5};
        assert Arrays.equals(twoSumSorted(sample, 2), new int[] {1, 3});
        assert Arrays.equals(twoSumSorted(new int[] {2, 2}, 4), new int[] {0, 1});
        assert twoSumSorted(new int[0], 0) == null;
        assert twoSumSorted(new int[] {2}, 4) == null;
        assert Arrays.equals(twoSumSorted(new int[] {Integer.MAX_VALUE,
                Integer.MAX_VALUE}, 4294967294L), new int[] {0, 1});
        boolean rejected = false;
        try {
            twoSumSorted(new int[] {2, 1}, 3);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected;
        System.out.println("Indices for sum 2: " + Arrays.toString(twoSumSorted(sample, 2)));
    }
}
