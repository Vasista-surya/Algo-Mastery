/** Iterative DP: O(n) time, O(1) space. Signed long supports F(0)..F(92). */
public class Fibonacci {
    public static long fibonacci(int n) {
        if (n < 0 || n > 92) {
            throw new IllegalArgumentException("n must be in [0, 92]");
        }
        if (n == 0) return 0;
        long previous = 0, current = 1;
        // Do not compute F(93) while returning F(92).
        for (int i = 2; i <= n; i++) {
            long next = Math.addExact(previous, current);
            previous = current;
            current = next;
        }
        return current;
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Fibonacci self-check failed");
    }

    public static void main(String[] args) {
        check(fibonacci(0) == 0);
        check(fibonacci(10) == 55);
        check(fibonacci(92) == 7540113804746346429L);
        boolean rejected = false;
        try { fibonacci(93); } catch (IllegalArgumentException ex) { rejected = true; }
        check(rejected);
        System.out.println("F(10) = " + fibonacci(10));
    }
}
