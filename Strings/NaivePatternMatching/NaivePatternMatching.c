/* Naive literal byte matching, including overlaps and embedded NUL bytes.
 * Explicit lengths; empty pattern matches all n+1 boundaries.
 * O(n*m+n+m) time; O(1) working space plus an O(n) result buffer.
 * Return 1 on success, 0 on invalid arguments/allocation failure. Outputs
 * reset to NULL/0 on failure. Caller frees *matches even when *count is zero.
 * NULL data is allowed only with zero length; pointers must cover their lengths.
 * Result allocation requires n+1 <= SIZE_MAX/sizeof(size_t) when m <= n.
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
    for (size_t start = 0; start <= n - m; ++start) {
        size_t j = 0;
        while (j < m && text[start + j] == pattern[j]) ++j;
        if (j == m) positions[(*count)++] = start;
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
    size_t *matches = NULL, count = 0;
    assert(!find_matches(NULL, 1, NULL, 0, &matches, &count));
    assert(matches == NULL && count == 0);
    return 0;
}
