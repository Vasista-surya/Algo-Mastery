import java.util.Objects;

/** Maximum sum of exactly width consecutive int values.
 * O(n) time, O(1) space; input is unchanged. Require 1 <= width <= length.
 * long accumulators hold every possible sum of a Java int array.
 */
public class SlidingWindow {
    public static long maxWindowSum(int[] values, int width) {
        Objects.requireNonNull(values, "values");
        if (width < 1 || width > values.length) {
            throw new IllegalArgumentException("invalid window width");
        }
        long current = 0;
        for (int i = 0; i < width; i++) current += values[i];
        long best = current;
        for (int i = width; i < values.length; i++) {
            current = current - values[i - width] + values[i];
            best = Math.max(best, current);
        }
        return best;
    }

    public static void main(String[] args) {
        int[] sample = {2, -1, 3, 5, -2};
        assert maxWindowSum(sample, 2) == 8;
        assert maxWindowSum(new int[] {-5, -2, -8}, 2) == -7;
        assert maxWindowSum(sample, sample.length) == 7;
        assert maxWindowSum(new int[] {Integer.MIN_VALUE, Integer.MAX_VALUE}, 1)
                == Integer.MAX_VALUE;
        boolean rejected = false;
        try {
            maxWindowSum(new int[0], 1);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected;
        System.out.println("Maximum width-2 window sum: " + maxWindowSum(sample, 2));
    }
}
