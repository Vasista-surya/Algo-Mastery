import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/** KMP: O(n+m) time, O(m) working space plus O(k) result storage.
 * Literal UTF-16 code-unit matching includes every overlap. Empty pattern
 * matches every boundary. Null arguments are rejected; strings are unchanged.
 */
public class KMP {
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
        int[] lps = new int[m];
        int border = 0;
        for (int i = 1; i < m; i++) {
            while (border > 0 && pattern.charAt(i) != pattern.charAt(border)) {
                border = lps[border - 1];
            }
            if (pattern.charAt(i) == pattern.charAt(border)) border++;
            lps[i] = border;
        }
        int matched = 0;
        for (int i = 0; i < n; i++) {
            while (matched > 0 && text.charAt(i) != pattern.charAt(matched)) {
                matched = lps[matched - 1];
            }
            if (text.charAt(i) == pattern.charAt(matched)) matched++;
            if (matched == m) {
                matches.add(i - m + 1);
                matched = lps[matched - 1];
            }
        }
        return matches;
    }

    public static void main(String[] args) {
        assert findMatches("aaaa", "aa").equals(Arrays.asList(0, 1, 2));
        assert findMatches("abababacaba", "ababaca").equals(Arrays.asList(2));
        assert findMatches("ab", "").equals(Arrays.asList(0, 1, 2));
        assert findMatches("", "").equals(Arrays.asList(0));
        assert findMatches("", "a").isEmpty();
        assert findMatches("a\0a\0", "a\0").equals(Arrays.asList(0, 2));
        System.out.println("Matches: " + findMatches("aaaa", "aa"));
    }
}
