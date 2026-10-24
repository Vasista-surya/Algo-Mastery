"""Z-array literal matching in O(n+m) time and working space, plus O(k) output.

Require str inputs; return all overlapping Unicode code-point offsets. Empty
pattern matches every boundary. A non-character separator avoids sentinel
collisions, including for input containing NUL, '$', or arbitrary Unicode.
"""


def find_matches(text, pattern):
    """Compute prefix-match lengths for pattern + sentinel + text."""
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("text and pattern must be strings")
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    combined = list(pattern) + [None] + list(text)
    z = [0] * len(combined)
    left = right = 0  # [left, right) is the current prefix-matching box.
    for i in range(1, len(combined)):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < len(combined) and combined[z[i]] == combined[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] >= m]


if __name__ == "__main__":
    assert find_matches("aaaa", "aa") == [0, 1, 2]
    assert find_matches("ab", "") == [0, 1, 2]
    assert find_matches("", "") == [0]
    assert find_matches("", "a") == []
    assert find_matches("a\0a\0", "a\0") == [0, 2]
    assert find_matches("$a$a$", "$a$") == [0, 2]
    print("Matches:", find_matches("aaaa", "aa"))
