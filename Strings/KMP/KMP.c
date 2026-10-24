/* KMP literal byte matching: O(n+m) time; O(m) working space + O(n) output.
 * All overlaps are returned; empty pattern matches all n+1 boundaries.
 * Explicit lengths support NUL bytes. NULL data only with zero length.
 * Return 1 on success, 0 on invalid arguments/allocation failure. Valid output
 * pointers are required; outputs reset to NULL/0. Caller frees *matches.
 * Require n+1 <= SIZE_MAX/sizeof(size_t) when m <= n; check all allocations.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

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
    if (m > SIZE_MAX / sizeof(size_t)) {
        free(positions);
        return 0;
    }
    size_t *lps = calloc(m, sizeof(*lps));
    if (lps == NULL) {
        free(positions);
        return 0;
    }
    size_t border = 0;
    for (size_t i = 1; i < m; ++i) {
        while (border != 0 && pattern[i] != pattern[border]) border = lps[border - 1];
        if (pattern[i] == pattern[border]) ++border;
        lps[i] = border;
    }
    size_t matched = 0;
    for (size_t i = 0; i < n; ++i) {
        while (matched != 0 && text[i] != pattern[matched]) matched = lps[matched - 1];
        if (text[i] == pattern[matched]) ++matched;
        if (matched == m) {
            positions[(*count)++] = i + 1 - m;
            matched = lps[matched - 1];
        }
    }
    free(lps);
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
    const size_t overlap[] = {0, 1, 2}, empty[] = {0}, fallback[] = {2};
    const size_t binary[] = {0, 2};
    check_case((const unsigned char *) "aaaa", 4, (const unsigned char *) "aa", 2,
               overlap, 3);
    check_case((const unsigned char *) "abababacaba", 11,
               (const unsigned char *) "ababaca", 7, fallback, 1);
    check_case((const unsigned char *) "ab", 2, NULL, 0, overlap, 3);
    check_case(NULL, 0, NULL, 0, empty, 1);
    check_case(NULL, 0, (const unsigned char *) "a", 1, NULL, 0);
    check_case((const unsigned char *) "a\0a\0", 4,
               (const unsigned char *) "a\0", 2, binary, 2);
    size_t *matches = NULL, count = 0;
    assert(!find_matches(NULL, 1, NULL, 0, &matches, &count));
    assert(matches == NULL && count == 0);
    return 0;
}
