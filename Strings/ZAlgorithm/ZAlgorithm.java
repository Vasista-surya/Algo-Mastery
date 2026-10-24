import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/** Z matching: O(n+m) time/working space, plus O(k) output.
 * Literal UTF-16 code-unit offsets; all overlaps and empty-pattern boundaries.
 * Uses a virtual -1 separator, outside the char domain. Null inputs fail;
 * nontrivial combined lengths greater than Integer.MAX_VALUE are rejected.
 */
public class ZAlgorithm {
    private static int symbolAt(String text, String pattern, int index) {
        int m = pattern.length();
        if (index < m) return pattern.charAt(index);
        if (index == m) return -1;
        return text.charAt(index - m - 1);
    }

    public static List<Integer> findMatches(String text, String pattern) {
        Objects.requireNonNull(text, "text");
        Objects.requireNonNull(pattern, "pattern");
        int n = text.length(), m = pattern.length();
        List<Integer> matches = new ArrayList<>();
        if (m == 0) {
            for (int i = 0; i < n; i++) matches.add(i);
            matches.add(n);
            return matches;
        }
        if (m > n) return matches;
        long combinedLength = (long) m + 1 + n;
        if (combinedLength > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("combined sequence is too large");
        }
        int length = (int) combinedLength;
        int[] z = new int[length];
        int left = 0, right = 0; // Half-open prefix-matching box.
        for (int i = 1; i < length; i++) {
            if (i < right) z[i] = Math.min(right - i, z[i - left]);
            while (z[i] < length - i
                    && symbolAt(text, pattern, z[i]) == symbolAt(text, pattern, i + z[i])) {
                z[i]++;
            }
            if (i + z[i] > right) {
                left = i;
                right = i + z[i];
            }
            if (i > m && z[i] >= m) matches.add(i - m - 1);
        }
        return matches;
    }

    public static void main(String[] args) {
        assert findMatches("aaaa", "aa").equals(Arrays.asList(0, 1, 2));
        assert findMatches("ab", "").equals(Arrays.asList(0, 1, 2));
        assert findMatches("", "").equals(Arrays.asList(0));
        assert findMatches("", "a").isEmpty();
        assert findMatches("a\0a\0", "a\0").equals(Arrays.asList(0, 2));
        assert findMatches("$a$a$", "$a$").equals(Arrays.asList(0, 2));
        System.out.println("Matches: " + findMatches("aaaa", "aa"));
    }
}
