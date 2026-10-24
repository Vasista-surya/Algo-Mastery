import java.util.*;

/** Divisible-item knapsack, O(N log N) time/O(N) space.
 * Integer values 0..10^9, weights 1..10^9, capacity 0..10^9.
 * Exact ratio ordering via bounded long cross-products; input-order ties.
 * Result contains approximate double total/shares in original input order.
 * Zero-value items skipped; empty/zero capacity valid. Input not modified.
 * Invalid input throws IllegalArgumentException; bounds prevent overflow.
 */
public class FractionalKnapsack {
    public static final class Item {
        public final long value, weight;
        public Item(long value, long weight) { this.value = value; this.weight = weight; }
    }
    public static final class Result {
        public final double total;
        public final double[] shares;
        private Result(double total, double[] shares) { this.total = total; this.shares = shares; }
    }

    public static Result fractionalKnapsack(Item[] items, long capacity) {
        if (items == null || capacity < 0 || capacity > 1_000_000_000L)
            throw new IllegalArgumentException("invalid items/capacity");
        Integer[] order = new Integer[items.length];
        for (int i = 0; i < items.length; i++) {
            Item item = items[i];
            if (item == null || item.value < 0 || item.value > 1_000_000_000L ||
                item.weight <= 0 || item.weight > 1_000_000_000L)
                throw new IllegalArgumentException("invalid value/weight");
            order[i] = i;
        }
        Arrays.sort(order, (a, b) -> {
            int comparison = Long.compare(items[b].value * items[a].weight,
                                          items[a].value * items[b].weight);
            return comparison != 0 ? comparison : Integer.compare(a, b);
        });
        double total = 0;
        double[] shares = new double[items.length];
        for (int i : order) {
            if (capacity == 0 || items[i].value == 0) break;
            long taken = Math.min(capacity, items[i].weight);
            shares[i] = (double)taken / items[i].weight;
            total += shares[i] * items[i].value;
            capacity -= taken;
        }
        return new Result(total, shares);
    }

    public static void main(String[] args) {
        Result result = fractionalKnapsack(new Item[] {
            new Item(60, 10), new Item(100, 20), new Item(120, 30)}, 50);
        assert Math.abs(result.total - 240) < 1e-9;
        assert result.shares[0] == 1 && result.shares[1] == 1;
        assert Math.abs(result.shares[2] - 2.0 / 3) < 1e-12;
        assert fractionalKnapsack(new Item[0], 5).total == 0;
        boolean rejected = false;
        try { fractionalKnapsack(new Item[] {new Item(1, 0)}, 0); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("Value: " + result.total + "; shares: " + Arrays.toString(result.shares));
    }
}
