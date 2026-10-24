/* Maximum sum of exactly width consecutive int32_t values.
 * O(n) time, O(1) space. Require 1 <= width <= n <= INT32_MAX, readable
 * n-element input and writable result. int64_t safely holds all sums.
 * Return 1 on success; 0 on invalid arguments, leaving result unchanged.
 */
#include <assert.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

int max_window_sum(const int32_t *values, size_t n, size_t width, int64_t *result) {
    if (values == NULL || result == NULL || n > INT32_MAX
            || width == 0 || width > n) return 0;
    int64_t current = 0;
    for (size_t i = 0; i < width; ++i) current += values[i];
    int64_t best = current;
    for (size_t i = width; i < n; ++i) {
        current = current - values[i - width] + values[i];
        if (current > best) best = current;
    }
    *result = best;
    return 1;
}

int main(void) {
    const int32_t sample[] = {2, -1, 3, 5, -2};
    const int32_t negative[] = {-5, -2, -8};
    const int32_t extremes[] = {INT32_MIN, INT32_MAX};
    int64_t result = 0;
    int ok = max_window_sum(sample, 5, 2, &result);
    assert(ok && result == 8);
    if (!ok) return 1;
    printf("Maximum width-2 window sum: %" PRId64 "\n", result);
    assert(max_window_sum(negative, 3, 2, &result) && result == -7);
    assert(max_window_sum(sample, 5, 5, &result) && result == 7);
    assert(max_window_sum(extremes, 2, 1, &result) && result == INT32_MAX);
    assert(!max_window_sum(NULL, 0, 1, &result));
    assert(!max_window_sum(sample, 5, 0, &result));
    assert(!max_window_sum(sample, 5, 6, &result));
    return 0;
}
