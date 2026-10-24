import java.util.Objects;

/** Maximum nonempty subarray sum: O(n) time, O(1) extra space.
 * Input is an unmodified int array. Empty input is invalid; null is rejected.
 * Every possible sum of a Java int[] fits in long (at most 2^31-1 elements).
 */
public class Kadane {
    public static long maxSubarray(int[] values) {
        Objects.requireNonNull(values, "values");
        if (values.length == 0) {
            throw new IllegalArgumentException("a nonempty array is required");
        }
        long current = values[0];
        long best = current;
        for (int i = 1; i < values.length; i++) {
            current = Math.max((long) values[i], current + values[i]);
            best = Math.max(best, current);
        }
        return best;
    }

    public static void main(String[] args) {
        int[] sample = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        assert maxSubarray(sample) == 6;
        assert maxSubarray(new int[] {-8, -2, -5}) == -2;
        assert maxSubarray(new int[] {0}) == 0;
        assert maxSubarray(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE})
                == 4294967294L;
        boolean rejected = false;
        try {
            maxSubarray(new int[0]);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected;
        System.out.println("Maximum subarray sum: " + maxSubarray(sample));
    }
}
