/* Sorted two-sum: O(n) time including validation, O(1) space.
 * Nondecreasing int32_t input, n <= INT32_MAX, any int64_t target.
 * NULL values allowed only when n=0. Output pointers must be distinct.
 * Return 1 with distinct zero-based indices, 0 if absent, -1 if invalid.
 * Output indices are unchanged unless a pair is found. Widen before addition.
 */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

int two_sum_sorted(const int32_t *values, size_t n, int64_t target,
                   size_t *left_index, size_t *right_index) {
    if ((values == NULL && n != 0) || n > INT32_MAX || left_index == NULL
            || right_index == NULL || left_index == right_index) return -1;
    for (size_t i = 1; i < n; ++i) {
        if (values[i - 1] > values[i]) return -1;
    }
    if (n < 2) return 0;
    size_t left = 0, right = n - 1;
    while (left < right) {
        int64_t sum = (int64_t) values[left] + values[right];
        if (sum == target) {
            *left_index = left;
            *right_index = right;
            return 1;
        }
        if (sum < target) ++left;
        else --right;
    }
    return 0;
}

int main(void) {
    const int32_t sample[] = {-4, -1, 0, 3, 5};
    const int32_t duplicates[] = {2, 2};
    const int32_t unsorted[] = {2, 1};
    const int32_t large[] = {INT32_MAX, INT32_MAX};
    size_t left = 0, right = 0;
    int status = two_sum_sorted(sample, 5, 2, &left, &right);
    assert(status == 1 && left == 1 && right == 3);
    if (status != 1) return 1;
    printf("Indices for sum 2: (%zu, %zu)\n", left, right);
    assert(two_sum_sorted(duplicates, 2, 4, &left, &right) == 1);
    assert(left == 0 && right == 1);
    assert(two_sum_sorted(NULL, 0, 0, &left, &right) == 0);
    assert(two_sum_sorted(sample, 1, -8, &left, &right) == 0);
    assert(two_sum_sorted(unsorted, 2, 3, &left, &right) == -1);
    assert(two_sum_sorted(large, 2, INT64_C(4294967294), &left, &right) == 1);
    return 0;
}
