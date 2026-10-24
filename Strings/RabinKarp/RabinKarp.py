"""Rolling-hash literal search with exact verification of every hash hit.

Require str inputs; offsets count Unicode code points. Include overlaps; empty
pattern matches every boundary. Time O(n+m+h*m) for h hash hits (worst O(n*m+n+m));
working space O(1), output O(k). Python modular arithmetic cannot overflow.
"""


def find_matches(text, pattern):
    """Return ascending offsets; collisions never cause false matches."""
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("text and pattern must be strings")
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    base, modulus = 257, 1_000_000_007
    power = pow(base, m - 1, modulus)
    pattern_hash = window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % modulus
        window_hash = (window_hash * base + ord(text[i])) % modulus
    matches = []
    for start in range(n - m + 1):
        if window_hash == pattern_hash and text.startswith(pattern, start):
            matches.append(start)
        if start < n - m:
            window_hash = ((window_hash - ord(text[start]) * power) * base
                           + ord(text[start + m])) % modulus
    return matches


if __name__ == "__main__":
    assert find_matches("aaaa", "aa") == [0, 1, 2]
    assert find_matches("ab", "") == [0, 1, 2]
    assert find_matches("", "") == [0]
    assert find_matches("", "a") == []
    assert find_matches("a\0a\0", "a\0") == [0, 2]
    # Both length-two strings hash to 257, but their characters differ.
    assert find_matches("\x00\u0101", "\x01\x00") == []
    print("Matches:", find_matches("aaaa", "aa"))
