/* Strict LIS length: O(n log n) time, O(n) space; n in [0,100000].
 * NULL values permitted for n=0. No input mutation. Caller provides n ints.
 * Return 1 success, 0 invalid, -1 allocation failure; out unchanged on error.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int lis_length(const int *values, int n, int *out) {
    if (!out || n < 0 || n > 100000 || (n > 0 && !values)) return 0;
    if (n == 0) { *out = 0; return 1; }
    if ((size_t)n > SIZE_MAX / sizeof(int)) return -1;
    int *tails = malloc((size_t)n * sizeof(*tails));
    if (!tails) return -1;
    int size = 0;
    for (int i = 0; i < n; ++i) {
        int low = 0, high = size;
        while (low < high) {
            int middle = low + (high - low) / 2;
            if (tails[middle] < values[i]) low = middle + 1;
            else high = middle;
        }
        tails[low] = values[i];
        if (low == size) ++size;
    }
    *out = size;
    free(tails);
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const int values[] = {10, 9, 2, 5, 3, 7, 101, 18}, equal[] = {2, 2, 2};
    int result = 0;
    int status = lis_length(NULL, 0, &result);
    assert(status == 1 && result == 0);
    status = lis_length(equal, 3, &result);
    assert(status == 1 && result == 1);
    status = lis_length(NULL, 1, &result);
    assert(status == 0);
    status = lis_length(values, 8, &result);
    assert(status == 1 && result == 4);
    if (status != 1) return 1;
    printf("LIS length: %d\n", result);
    return 0;
}
#endif
