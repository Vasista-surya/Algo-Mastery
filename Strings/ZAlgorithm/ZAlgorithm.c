/* Z matching: O(n+m) time/working space, plus O(n) result storage.
 * Explicit byte lengths allow NULs; a virtual separator cannot collide with
 * input bytes. Include all overlaps and all n+1 empty-pattern boundaries.
 * Return 1 success, 0 invalid/allocation failure; reset outputs to NULL/0.
 * Caller frees *matches. NULL data is valid only with zero length. Check n+1,
 * n+m+1 and all size_t allocation products before computing/allocating them.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int same_symbol(const unsigned char *text, const unsigned char *pattern,
                       size_t m, size_t a, size_t b) {
    if (a == m || b == m) return a == b; // Only the separator equals itself.
    unsigned char first = a < m ? pattern[a] : text[a - m - 1];
    unsigned char second = b < m ? pattern[b] : text[b - m - 1];
    return first == second;
}

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
    if (m == SIZE_MAX || n > SIZE_MAX - m - 1) {
        free(positions);
        return 0;
    }
    size_t length = m + 1 + n;
    if (length > SIZE_MAX / sizeof(size_t)) {
        free(positions);
        return 0;
    }
    size_t *z = calloc(length, sizeof(*z));
    if (z == NULL) {
        free(positions);
        return 0;
    }
    size_t left = 0, right = 0;
    for (size_t i = 1; i < length; ++i) {
        if (i < right) z[i] = z[i - left] < right - i ? z[i - left] : right - i;
        while (z[i] < length - i && same_symbol(text, pattern, m, z[i], i + z[i])) {
            ++z[i];
        }
        if (i + z[i] > right) {
            left = i;
            right = i + z[i];
        }
        if (i > m && z[i] >= m) positions[(*count)++] = i - m - 1;
    }
    free(z);
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
    check_case((const unsigned char *) "$a$a$", 5,
               (const unsigned char *) "$a$", 3, binary, 2);
    size_t *matches = NULL, count = 0;
    assert(!find_matches(NULL, 1, NULL, 0, &matches, &count));
    assert(matches == NULL && count == 0);
    return 0;
}
