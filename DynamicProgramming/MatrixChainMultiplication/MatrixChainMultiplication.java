/** Minimum scalar multiplication count; O(n^3) time, O(n^2) space.
 * Up to 101 dimensions in [1,100000]. Zero/one matrix costs zero.
 * Every candidate <=99*10^15, within long; exact operations guard arithmetic.
 */
public class MatrixChainMultiplication {
    public static long matrixChainCost(int[] dimensions) {
        if (dimensions == null || dimensions.length > 101) {
            throw new IllegalArgumentException("at most 101 dimensions required");
        }
        for (int dimension : dimensions) {
            if (dimension <= 0 || dimension > 100000) {
                throw new IllegalArgumentException("dimensions must be in [1,100000]");
            }
        }
        int n = dimensions.length - 1;
        if (n <= 1) return 0;
        long[][] best = new long[n][n];
        for (int length = 2; length <= n; length++) {
            for (int left = 0; left + length <= n; left++) {
                int right = left + length - 1;
                best[left][right] = Long.MAX_VALUE;
                for (int split = left; split < right; split++) {
                    long product = Math.multiplyExact((long) dimensions[left], dimensions[split + 1]);
                    product = Math.multiplyExact(product, dimensions[right + 1]);
                    long candidate = Math.addExact(best[left][split], best[split + 1][right]);
                    candidate = Math.addExact(candidate, product);
                    best[left][right] = Math.min(best[left][right], candidate);
                }
            }
        }
        return best[0][n - 1];
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Matrix-chain self-check failed");
    }

    public static void main(String[] args) {
        int[] dimensions = {40, 20, 30, 10, 30};
        check(matrixChainCost(dimensions) == 26000);
        check(matrixChainCost(new int[0]) == 0);
        check(matrixChainCost(new int[]{10, 20}) == 0);
        check(matrixChainCost(new int[]{100000, 100000, 100000}) == 1000000000000000L);
        boolean rejected = false;
        try { matrixChainCost(new int[]{10, -1}); }
        catch (IllegalArgumentException ex) { rejected = true; }
        check(rejected);
        System.out.println("Minimum scalar multiplications: " + matrixChainCost(dimensions));
    }
}
