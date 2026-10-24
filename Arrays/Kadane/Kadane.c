/* Maximum nonempty subarray sum: O(n) time, O(1) space, no allocation.
 * C99 with int32_t/int64_t. Require 1 <= n <= INT32_MAX and n readable
 * elements; this bounds all sums within int64_t. Return 1 on success,
 * 0 for invalid pointers/sizes; *result is unchanged on failure.
 */
#include <assert.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

int max_subarray(const int32_t *values, size_t n, int64_t *result) {
    if (values == NULL || result == NULL || n == 0 || n > INT32_MAX) {
        return 0;
    }
    int64_t current = values[0];
    int64_t best = current;
    for (size_t i = 1; i < n; ++i) {
        int64_t extended = current + values[i];
        current = extended > values[i] ? extended : values[i];
        if (current > best) best = current;
    }
    *result = best;
    return 1;
}

int main(void) {
    const int32_t sample[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    const int32_t negative[] = {-8, -2, -5};
    const int32_t large[] = {INT32_MAX, INT32_MAX};
    int64_t result = 0;
    int ok = max_subarray(sample, 9, &result);
    assert(ok && result == 6);
    if (!ok) return 1;
    printf("Maximum subarray sum: %" PRId64 "\n", result);
    assert(max_subarray(negative, 3, &result) && result == -2);
    assert(max_subarray(large, 2, &result) && result == INT64_C(4294967294));
    assert(!max_subarray(NULL, 0, &result));
    assert(!max_subarray(sample, 9, NULL));
    return 0;
}
