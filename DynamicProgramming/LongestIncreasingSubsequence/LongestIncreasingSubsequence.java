/** Strict LIS length: O(n log n) time, O(n) space; at most 100000 ints.
 * Empty input gives 0; equal values do not extend a subsequence. No mutation.
 */
public class LongestIncreasingSubsequence {
    public static int lisLength(int[] values) {
        if (values == null || values.length > 100000) {
            throw new IllegalArgumentException("at most 100000 integers required");
        }
        int[] tails = new int[values.length];
        int size = 0;
        for (int value : values) {
            int low = 0, high = size;
            while (low < high) {
                int middle = low + (high - low) / 2;
                if (tails[middle] < value) low = middle + 1;
                else high = middle;
            }
            tails[low] = value;
            if (low == size) size++;
        }
        return size;
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("LIS self-check failed");
    }

    public static void main(String[] args) {
        int[] values = {10, 9, 2, 5, 3, 7, 101, 18};
        check(lisLength(values) == 4);
        check(lisLength(new int[0]) == 0);
        check(lisLength(new int[]{2, 2, 2}) == 1);
        check(lisLength(new int[]{-3, -2, -1}) == 3);
        System.out.println("LIS length: " + lisLength(values));
    }
}
