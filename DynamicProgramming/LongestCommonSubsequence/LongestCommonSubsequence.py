"""LCS length via rolling DP: O(m*n+m+n) time, O(min(m,n)+1) space.

Accept strings of at most 2000 Unicode code points each. Empty strings
have LCS length zero. This API returns a length, not a reconstructed LCS.
"""


def lcs_length(a, b):
    if not isinstance(a, str) or not isinstance(b, str) or max(len(a), len(b)) > 2000:
        raise ValueError("two strings of length at most 2000 required")
    if len(a) < len(b):
        a, b = b, a
    row = [0] * (len(b) + 1)
    for left in a:
        diagonal = 0
        for j, right in enumerate(b, 1):
            above = row[j]
            row[j] = diagonal + 1 if left == right else max(row[j], row[j - 1])
            diagonal = above
    return row[-1]


def main():
    assert lcs_length("AGGTAB", "GXTXAYB") == 4
    assert lcs_length("", "abc") == 0
    assert lcs_length("aaaa", "aa") == 2
    assert lcs_length("abc", "xyz") == 0
    print("LCS length:", lcs_length("AGGTAB", "GXTXAYB"))


if __name__ == "__main__":
    main()
