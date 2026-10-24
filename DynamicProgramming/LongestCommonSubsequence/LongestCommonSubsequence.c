/* LCS length of byte strings, O(m*n+m+n) time, O(min(m,n)+1) space.
 * Non-NULL NUL-terminated strings, <=2000 bytes each; empty gives zero.
 * Return 1 success, 0 invalid, -1 allocation failure; out unchanged on error.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int lcs_length(const char *a, const char *b, int *out) {
    if (!a || !b || !out) return 0;
    size_t m = strlen(a), n = strlen(b);
    if (m > 2000 || n > 2000) return 0;
    if (m < n) {
        const char *swap = a; a = b; b = swap;
        size_t length = m; m = n; n = length;
    }
    if (n + 1 > SIZE_MAX / sizeof(int)) return -1;
    int *row = calloc(n + 1, sizeof(*row));
    if (!row) return -1;
    for (size_t i = 0; i < m; ++i) {
        int diagonal = 0;
        for (size_t j = 1; j <= n; ++j) {
            int above = row[j];
            row[j] = a[i] == b[j - 1] ? diagonal + 1
                    : (row[j] > row[j - 1] ? row[j] : row[j - 1]);
            diagonal = above;
        }
    }
    *out = row[n];
    free(row);
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    int result = 0;
    int status = lcs_length("", "abc", &result);
    assert(status == 1 && result == 0);
    status = lcs_length("aaaa", "aa", &result);
    assert(status == 1 && result == 2);
    status = lcs_length(NULL, "a", &result);
    assert(status == 0);
    status = lcs_length("AGGTAB", "GXTXAYB", &result);
    assert(status == 1 && result == 4);
    if (status != 1) return 1;
    printf("LCS length: %d\n", result);
    return 0;
}
#endif
