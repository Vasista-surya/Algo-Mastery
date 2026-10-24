import java.util.Arrays;

/** Minimum coins with unlimited reuse, O((k+1)*(amount+1)) time, O(amount+1) space.
 * Up to 1000 denominations in [1,10^9], amount in [0,100000].
 * Duplicates allowed. Empty coins: 0 for amount=0, otherwise -1 (unreachable).
 */
public class CoinChange {
    public static int minCoins(int[] coins, int amount) {
        if (coins == null || coins.length > 1000 || amount < 0 || amount > 100000) {
            throw new IllegalArgumentException("invalid coins or amount");
        }
        for (int coin : coins) {
            if (coin <= 0 || coin > 1000000000) {
                throw new IllegalArgumentException("denominations must be in [1,10^9]");
            }
        }
        int[] best = new int[amount + 1];
        Arrays.fill(best, amount + 1);
        best[0] = 0;
        for (int coin : coins) {
            for (int subtotal = coin; subtotal <= amount; subtotal++) {
                best[subtotal] = Math.min(best[subtotal], best[subtotal - coin] + 1);
            }
        }
        return best[amount] == amount + 1 ? -1 : best[amount];
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Coin change self-check failed");
    }

    public static void main(String[] args) {
        check(minCoins(new int[]{1, 3, 4}, 6) == 2);
        check(minCoins(new int[]{2}, 3) == -1);
        check(minCoins(new int[0], 0) == 0);
        check(minCoins(new int[0], 5) == -1);
        check(minCoins(new int[]{2, 2}, 4) == 2);
        boolean rejected = false;
        try { minCoins(new int[]{0}, 0); }
        catch (IllegalArgumentException ex) { rejected = true; }
        check(rejected);
        System.out.println("Minimum coins: " + minCoins(new int[]{1, 3, 4}, 6));
    }
}
