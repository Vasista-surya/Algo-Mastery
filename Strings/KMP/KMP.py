"""Knuth-Morris-Pratt literal matching using a longest-prefix/suffix table.

Require str inputs; return all overlapping Unicode code-point offsets. Empty
pattern matches every boundary. O(n+m) time, O(m) working space plus O(k) output.
"""


def find_matches(text, pattern):
    """Return every match in ascending order, retaining borders after a match."""
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("text and pattern must be strings")
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    lps = [0] * m
    border = 0
    for i in range(1, m):
        while border and pattern[i] != pattern[border]:
            border = lps[border - 1]
        if pattern[i] == pattern[border]:
            border += 1
        lps[i] = border
    matches = []
    matched = 0
    for i, character in enumerate(text):
        while matched and character != pattern[matched]:
            matched = lps[matched - 1]
        if character == pattern[matched]:
            matched += 1
        if matched == m:
            matches.append(i - m + 1)
            matched = lps[matched - 1]
    return matches


if __name__ == "__main__":
    assert find_matches("aaaa", "aa") == [0, 1, 2]
    assert find_matches("abababacaba", "ababaca") == [2]
    assert find_matches("ab", "") == [0, 1, 2]
    assert find_matches("", "") == [0]
    assert find_matches("", "a") == []
    assert find_matches("a\0a\0", "a\0") == [0, 2]
    print("Matches:", find_matches("aaaa", "aa"))
