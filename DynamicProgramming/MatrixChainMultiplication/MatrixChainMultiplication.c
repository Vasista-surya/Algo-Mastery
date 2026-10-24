/* Matrix-chain minimum scalar multiplication count, O(n^3) time/O(n^2) space.
 * dimension_count in [0,101], dimensions in [1,100000]. Zero/one matrix: 0.
 * <=99 multiplications each <=10^15 => all costs fit signed long long.
 * Return 1 success, 0 invalid, -1 allocation error, -2 arithmetic overflow
 * (defensive, unreachable under limits). out unchanged on failure.
 */
#include <assert.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int matrix_chain_cost(const int *dimensions, int dimension_count, long long *out) {
    if (!out || dimension_count < 0 || dimension_count > 101
            || (dimension_count > 0 && !dimensions)) return 0;
    for (int i = 0; i < dimension_count; ++i) {
        if (dimensions[i] <= 0 || dimensions[i] > 100000) return 0;
    }
    int n = dimension_count - 1;
    if (n <= 1) { *out = 0; return 1; }
    size_t count = (size_t)n * (size_t)n;
    if (count > SIZE_MAX / sizeof(long long)) return -1;
    long long *best = calloc(count, sizeof(*best));
    if (!best) return -1;
    for (int length = 2; length <= n; ++length) {
        for (int left = 0; left + length <= n; ++left) {
            int right = left + length - 1;
            best[left * n + right] = LLONG_MAX;
            for (int split = left; split < right; ++split) {
                long long product = (long long)dimensions[left] * dimensions[split + 1];
                if (product > LLONG_MAX / dimensions[right + 1]) { free(best); return -2; }
                product *= dimensions[right + 1];
                long long a = best[left * n + split], b = best[(split + 1) * n + right];
                if (a > LLONG_MAX - b || a + b > LLONG_MAX - product) {
                    free(best);
                    return -2;
                }
                long long candidate = a + b + product;
                if (candidate < best[left * n + right]) best[left * n + right] = candidate;
            }
        }
    }
    *out = best[n - 1];
    free(best);
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const int dimensions[] = {40, 20, 30, 10, 30};
    const int large[] = {100000, 100000, 100000}, invalid[] = {10, -1};
    long long result = 0;
    int status = matrix_chain_cost(NULL, 0, &result);
    assert(status == 1 && result == 0);
    status = matrix_chain_cost(large, 3, &result);
    assert(status == 1 && result == 1000000000000000LL);
    status = matrix_chain_cost(invalid, 2, &result);
    assert(status == 0);
    status = matrix_chain_cost(dimensions, 5, &result);
    assert(status == 1 && result == 26000);
    if (status != 1) return 1;
    printf("Minimum scalar multiplications: %lld\n", result);
    return 0;
}
#endif
