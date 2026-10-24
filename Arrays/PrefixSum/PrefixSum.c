/* Prefix sums: O(n) build time/space, O(1) half-open [start,end) query.
 * C99 int32_t inputs, n <= INT32_MAX: all genuine range sums fit int64_t.
 * NULL values is valid only for n=0. Builder returns a heap array of n+1
 * elements (including leading zero), owned by caller; free it after use.
 * Both APIs return 1 on success, 0 on invalid arguments/allocation/overflow.
 * Query requires a builder-produced array and its actual length.
 */
#include <assert.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int prefix_sums(const int32_t *values, size_t n, int64_t **out) {
    if (out == NULL) return 0;
    *out = NULL;
    if ((values == NULL && n != 0) || n > INT32_MAX || n == SIZE_MAX
            || n + 1 > SIZE_MAX / sizeof(int64_t)) return 0;
    int64_t *prefix = malloc((n + 1) * sizeof(*prefix));
    if (prefix == NULL) return 0;
    prefix[0] = 0;
    for (size_t i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + values[i];
    *out = prefix;
    return 1;
}

int range_sum(const int64_t *prefix, size_t length, size_t start,
              size_t end, int64_t *out) {
    if (prefix == NULL || out == NULL || length == 0
            || length - 1 > INT32_MAX || prefix[0] != 0
            || start > end || end >= length) return 0;
    int64_t a = prefix[end], b = prefix[start];
    /* Defensive checked subtraction, even for caller-crafted prefix arrays. */
    if ((b > 0 && a < INT64_MIN + b) || (b < 0 && a > INT64_MAX + b)) return 0;
    *out = a - b;
    return 1;
}

int main(void) {
    const int32_t values[] = {2, -1, 3, 5};
    int64_t *prefix = NULL;
    int64_t result = 0;
    int ok = prefix_sums(values, 4, &prefix);
    assert(ok);
    if (!ok) return 1;
    assert(prefix[0] == 0 && prefix[4] == 9);
    ok = range_sum(prefix, 5, 1, 3, &result);
    assert(ok && result == 2);
    printf("Sum of [1, 3): %" PRId64 "\n", result);
    assert(range_sum(prefix, 5, 4, 4, &result) && result == 0);
    assert(!range_sum(prefix, 5, 3, 2, &result));
    free(prefix);
    ok = prefix_sums(NULL, 0, &prefix);
    assert(ok);
    if (!ok) return 1;
    assert(range_sum(prefix, 1, 0, 0, &result) && result == 0);
    free(prefix);
    const int64_t invalid[] = {0, INT64_MIN, INT64_MAX};
    assert(!range_sum(invalid, 3, 1, 2, &result));
    assert(!prefix_sums(NULL, 1, &prefix) && prefix == NULL);
    return 0;
}
