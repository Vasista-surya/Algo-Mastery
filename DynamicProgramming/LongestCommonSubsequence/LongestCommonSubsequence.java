/** LCS length (UTF-16 code units), O(m*n+m+n) time, O(min(m,n)+1) space.
 * Strings must be non-null, at most 2000 code units each; empty gives 0.
 */
public class LongestCommonSubsequence {
    public static int lcsLength(String a, String b) {
        if (a == null || b == null || a.length() > 2000 || b.length() > 2000) {
            throw new IllegalArgumentException("strings must have length <= 2000");
        }
        if (a.length() < b.length()) {
            String swap = a; a = b; b = swap;
        }
        int[] row = new int[b.length() + 1];
        for (int i = 0; i < a.length(); i++) {
            int diagonal = 0;
            for (int j = 1; j <= b.length(); j++) {
                int above = row[j];
                row[j] = a.charAt(i) == b.charAt(j - 1)
                        ? diagonal + 1 : Math.max(row[j], row[j - 1]);
                diagonal = above;
            }
        }
        return row[b.length()];
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("LCS self-check failed");
    }

    public static void main(String[] args) {
        check(lcsLength("AGGTAB", "GXTXAYB") == 4);
        check(lcsLength("", "abc") == 0);
        check(lcsLength("aaaa", "aa") == 2);
        check(lcsLength("abc", "xyz") == 0);
        System.out.println("LCS length: " + lcsLength("AGGTAB", "GXTXAYB"));
    }
}
