import java.util.Arrays;
import java.util.Objects;

/** O(n) time/space construction, O(1) half-open range queries.
 * int[] values produce long[] sums; all int-array sums fit in long.
 * Query an unmodified builder result. Empty input produces {0}.
 */
public class PrefixSum {
    public static long[] prefixSums(int[] values) {
        Objects.requireNonNull(values, "values");
        if (values.length == Integer.MAX_VALUE) {
            throw new IllegalArgumentException("no room for leading zero");
        }
        long[] prefix = new long[values.length + 1];
        for (int i = 0; i < values.length; i++) {
            prefix[i + 1] = prefix[i] + values[i];
        }
        return prefix;
    }

    public static long rangeSum(long[] prefix, int start, int end) {
        Objects.requireNonNull(prefix, "prefix");
        if (prefix.length == 0 || prefix[0] != 0 || start < 0
                || start > end || end >= prefix.length) {
            throw new IllegalArgumentException("invalid prefix or half-open range");
        }
        // Also detect overflow if a caller supplies a malformed prefix array.
        return Math.subtractExact(prefix[end], prefix[start]);
    }

    public static void main(String[] args) {
        long[] sums = prefixSums(new int[] {2, -1, 3, 5});
        assert Arrays.equals(sums, new long[] {0, 2, 1, 4, 9});
        assert rangeSum(sums, 1, 3) == 2;
        assert rangeSum(sums, 4, 4) == 0;
        assert rangeSum(prefixSums(new int[0]), 0, 0) == 0;
        assert rangeSum(prefixSums(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE}),
                0, 2) == -4294967296L;
        boolean rejected = false;
        try {
            rangeSum(sums, 3, 2);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected;
        System.out.println("Sum of [1, 3): " + rangeSum(sums, 1, 3));
    }
}
