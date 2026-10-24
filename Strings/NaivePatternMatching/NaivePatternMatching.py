"""Literal pattern matching by checking every alignment.

Return all overlapping, zero-based Unicode code-point offsets. Empty pattern
matches every boundary, including len(text). Require str inputs. Worst-case
O(n*m + n + m) time, O(1) working space plus O(k) returned matches.
"""


def find_matches(text, pattern):
    """Return ascending offsets without changing either string."""
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("text and pattern must be strings")
    n, m = len(text), len(pattern)
    return [start for start in range(n - m + 1)
            if all(text[start + j] == pattern[j] for j in range(m))]


if __name__ == "__main__":
    assert find_matches("aaaa", "aa") == [0, 1, 2]
    assert find_matches("ab", "") == [0, 1, 2]
    assert find_matches("", "") == [0]
    assert find_matches("", "a") == []
    assert find_matches("abc", "abcd") == []
    assert find_matches("a\0a\0", "a\0") == [0, 2]
    print("Matches:", find_matches("aaaa", "aa"))
