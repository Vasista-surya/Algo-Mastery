/** 0/1 maximum value. O((n+1)*(capacity+1)) time, O(capacity+1) space.
 * Up to 1000 items, capacity <=100000, weights/values in [0,10^9].
 * Empty items yield 0. Zero-weight items are each counted once, even at capacity 0.
 */
public class Knapsack01 {
    public static long knapsack01(int[] weights, int[] values, int capacity) {
        if (weights == null || values == null || weights.length != values.length
                || weights.length > 1000 || capacity < 0 || capacity > 100000) {
            throw new IllegalArgumentException("invalid arrays or capacity");
        }
        for (int i = 0; i < weights.length; i++) {
            if (weights[i] < 0 || weights[i] > 1000000000
                    || values[i] < 0 || values[i] > 1000000000) {
                throw new IllegalArgumentException("weight/value outside [0, 10^9]");
            }
        }
        long[] best = new long[capacity + 1];
        for (int i = 0; i < weights.length; i++) {
            for (int room = capacity; room >= weights[i]; room--) {
                best[room] = Math.max(best[room], best[room - weights[i]] + values[i]);
            }
        }
        return best[capacity]; // At most 10^12; fits long.
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Knapsack self-check failed");
    }

    public static void main(String[] args) {
        check(knapsack01(new int[]{10, 20, 30}, new int[]{60, 100, 120}, 50) == 220);
        check(knapsack01(new int[]{0, 0, 1}, new int[]{5, 7, 100}, 0) == 12);
        check(knapsack01(new int[0], new int[0], 0) == 0);
        check(knapsack01(new int[]{2}, new int[]{3}, 4) == 3);
        boolean rejected = false;
        try { knapsack01(new int[0], new int[0], -1); }
        catch (IllegalArgumentException ex) { rejected = true; }
        check(rejected);
        System.out.println("Maximum value: "
                + knapsack01(new int[]{10, 20, 30}, new int[]{60, 100, 120}, 50));
    }
}
