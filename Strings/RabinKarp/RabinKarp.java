import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/** Rolling-hash search, verifying every hash hit to rule out collisions.
 * Literal UTF-16 code-unit offsets, all overlaps, n+1 empty-pattern matches.
 * O(n+m+h*m) time for h hash hits (worst O(n*m+n+m)); O(1) working space
 * plus O(k) output. Fixed modulus/base keep all long intermediates in range.
 */
public class RabinKarp {
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
        final long base = 257, modulus = 1000000007L;
        long power = 1, patternHash = 0, windowHash = 0;
        for (int i = 1; i < m; i++) power = power * base % modulus;
        for (int i = 0; i < m; i++) {
            patternHash = (patternHash * base + pattern.charAt(i)) % modulus;
            windowHash = (windowHash * base + text.charAt(i)) % modulus;
        }
        for (int start = 0; start <= n - m; start++) {
            if (windowHash == patternHash && text.regionMatches(start, pattern, 0, m)) {
                matches.add(start);
            }
            if (start < n - m) {
                long outgoing = text.charAt(start) * power % modulus;
                windowHash = (windowHash - outgoing + modulus) % modulus;
                windowHash = (windowHash * base + text.charAt(start + m)) % modulus;
            }
        }
        return matches;
    }

    public static void main(String[] args) {
        assert findMatches("aaaa", "aa").equals(Arrays.asList(0, 1, 2));
        assert findMatches("ab", "").equals(Arrays.asList(0, 1, 2));
        assert findMatches("", "").equals(Arrays.asList(0));
        assert findMatches("", "a").isEmpty();
        assert findMatches("a\0a\0", "a\0").equals(Arrays.asList(0, 2));
        assert findMatches("\0\u0101", "\1\0").isEmpty(); // Equal hash, different text.
        System.out.println("Matches: " + findMatches("aaaa", "aa"));
    }
}
