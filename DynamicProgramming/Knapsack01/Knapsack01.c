/* 0/1 maximum value; O((n+1)*(capacity+1)) time, O(capacity+1) space.
 * n<=1000, capacity<=100000, weights/values in [0,10^9]. Zero weights
 * contribute once each, also at capacity zero. Value <=10^12 fits long long.
 * Return 1 success, 0 invalid, -1 allocation failure; out unchanged on error.
 * NULL input arrays allowed only when n=0. Arrays must contain n elements.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int knapsack_01(const int *weights, const int *values, int n, int capacity,
                long long *out) {
    if (!out || n < 0 || n > 1000 || capacity < 0 || capacity > 100000
            || (n > 0 && (!weights || !values))) return 0;
    for (int i = 0; i < n; ++i) {
        if (weights[i] < 0 || weights[i] > 1000000000
                || values[i] < 0 || values[i] > 1000000000) return 0;
    }
    size_t count = (size_t)capacity + 1;
    if (count > SIZE_MAX / sizeof(long long)) return -1;
    long long *best = calloc(count, sizeof(*best));
    if (!best) return -1;
    for (int i = 0; i < n; ++i) {
        for (int room = capacity; room >= weights[i]; --room) {
            long long candidate = best[room - weights[i]] + values[i];
            if (candidate > best[room]) best[room] = candidate;
        }
    }
    *out = best[capacity];
    free(best);
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const int weights[] = {10, 20, 30}, values[] = {60, 100, 120};
    const int zero_weights[] = {0, 0, 1}, zero_values[] = {5, 7, 100};
    long long result = 0;
    int status = knapsack_01(zero_weights, zero_values, 3, 0, &result);
    assert(status == 1 && result == 12);
    status = knapsack_01(NULL, NULL, 0, 0, &result);
    assert(status == 1 && result == 0);
    status = knapsack_01(weights, values, 3, -1, &result);
    assert(status == 0);
    status = knapsack_01(weights, values, 3, 50, &result);
    assert(status == 1 && result == 220);
    if (status != 1) return 1;
    printf("Maximum value: %lld\n", result);
    return 0;
}
#endif
