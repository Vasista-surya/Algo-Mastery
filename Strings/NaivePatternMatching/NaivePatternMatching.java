import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/** Literal matching of all overlaps; offsets count UTF-16 code units.
 * Empty pattern matches all n+1 boundaries; null arguments are rejected.
 * O(n*m+n+m) worst-case time, O(1) working space plus O(k) output.
 */
public class NaivePatternMatching {
    public static List<Integer> findMatches(String text, String pattern) {
        Objects.requireNonNull(text, "text");
        Objects.requireNonNull(pattern, "pattern");
        int n = text.length(), m = pattern.length();
        List<Integer> matches = new ArrayList<>();
        if (m == 0) {
            for (int i = 0; i < n; i++) matches.add(i);
            matches.add(n); // Avoid incrementing Integer.MAX_VALUE.
            return matches;
        }
        for (int start = 0; start <= n - m; start++) {
            int j = 0;
            while (j < m && text.charAt(start + j) == pattern.charAt(j)) j++;
            if (j == m) matches.add(start);
        }
        return matches;
    }

    public static void main(String[] args) {
        assert findMatches("aaaa", "aa").equals(Arrays.asList(0, 1, 2));
        assert findMatches("ab", "").equals(Arrays.asList(0, 1, 2));
        assert findMatches("", "").equals(Arrays.asList(0));
        assert findMatches("", "a").isEmpty();
        assert findMatches("abc", "abcd").isEmpty();
        assert findMatches("a\0a\0", "a\0").equals(Arrays.asList(0, 2));
        System.out.println("Matches: " + findMatches("aaaa", "aa"));
    }
}
