/* Rabin-Karp byte matching: verify hash hits, include overlaps and NUL bytes.
 * Empty pattern matches all n+1 boundaries. O(n+m+h*m) time for h hash hits,
 * worst O(n*m+n+m); O(1) working space plus O(n) result storage.
 * Return 1 success, 0 invalid/allocation failure; reset outputs to NULL/0.
 * Caller frees *matches. NULL data only with length zero. For m <= n require
 * n+1 <= SIZE_MAX/sizeof(size_t). Reduced uint64_t products stay below 2^64.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int find_matches(const unsigned char *text, size_t n,
                 const unsigned char *pattern, size_t m,
                 size_t **matches, size_t *count) {
    if (matches == NULL || count == NULL) return 0;
    *matches = NULL;
    *count = 0;
    if ((text == NULL && n != 0) || (pattern == NULL && m != 0)) return 0;
    if (m > n) return 1;
    if (n == SIZE_MAX || n + 1 > SIZE_MAX / sizeof(size_t)) return 0;
    size_t *positions = malloc((n + 1) * sizeof(*positions));
    if (positions == NULL) return 0;
    if (m == 0) {
        for (size_t i = 0; i <= n; ++i) positions[i] = i;
        *matches = positions;
        *count = n + 1;
        return 1;
    }
    const uint64_t base = UINT64_C(257), modulus = UINT64_C(1000000007);
    uint64_t power = 1, pattern_hash = 0, window_hash = 0;
    for (size_t i = 1; i < m; ++i) power = power * base % modulus;
    for (size_t i = 0; i < m; ++i) {
        pattern_hash = (pattern_hash * base + pattern[i] % modulus) % modulus;
        window_hash = (window_hash * base + text[i] % modulus) % modulus;
    }
    for (size_t start = 0; start <= n - m; ++start) {
        if (window_hash == pattern_hash && memcmp(text + start, pattern, m) == 0) {
            positions[(*count)++] = start;
        }
        if (start < n - m) {
            uint64_t outgoing = (text[start] % modulus) * power % modulus;
            window_hash = (window_hash + modulus - outgoing) % modulus;
            window_hash = (window_hash * base + text[start + m] % modulus) % modulus;
        }
    }
    *matches = positions;
    return 1;
}

static void check_case(const unsigned char *text, size_t n,
                       const unsigned char *pattern, size_t m,
                       const size_t *expected, size_t expected_count) {
    size_t *matches = NULL, count = 0;
    int ok = find_matches(text, n, pattern, m, &matches, &count);
    assert(ok && count == expected_count);
    if (!ok || count != expected_count) {
        free(matches);
        exit(EXIT_FAILURE);
    }
    printf("Matches:");
    for (size_t i = 0; i < count; ++i) {
        assert(matches[i] == expected[i]);
        printf(" %zu", matches[i]);
    }
    putchar('\n');
    free(matches);
}

int main(void) {
    const size_t overlap[] = {0, 1, 2}, empty[] = {0}, binary[] = {0, 2};
    check_case((const unsigned char *) "aaaa", 4, (const unsigned char *) "aa", 2,
               overlap, 3);
    check_case((const unsigned char *) "ab", 2, NULL, 0, overlap, 3);
    check_case(NULL, 0, NULL, 0, empty, 1);
    check_case(NULL, 0, (const unsigned char *) "a", 1, NULL, 0);
    check_case((const unsigned char *) "a\0a\0", 4,
               (const unsigned char *) "a\0", 2, binary, 2);
    /* These four-byte sequences both hash to zero modulo 1000000007. */
    const unsigned char collision[] = {58, 234, 70, 157}, zero[] = {0, 0, 0, 0};
    check_case(collision, 4, zero, 4, NULL, 0);
    size_t *matches = NULL, count = 0;
    assert(!find_matches(NULL, 1, NULL, 0, &matches, &count));
    assert(matches == NULL && count == 0);
    return 0;
}
