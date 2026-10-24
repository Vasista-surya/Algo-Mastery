/* Unbounded minimum coins, NOT number of combinations.
 * O((k+1)*(amount+1)) time, O(amount+1) space. k<=1000, amount in [0,100000],
 * denominations in [1,10^9]. Duplicates allowed. Empty coins allowed.
 * Return 1 success (out=-1 means unreachable), 0 invalid, -1 allocation error.
 * Failure leaves out unchanged. NULL coins permitted only for k=0.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int min_coins(const int *coins, int k, int amount, int *out) {
    if (!out || k < 0 || k > 1000 || amount < 0 || amount > 100000
            || (k > 0 && !coins)) return 0;
    for (int i = 0; i < k; ++i) {
        if (coins[i] <= 0 || coins[i] > 1000000000) return 0;
    }
    size_t count = (size_t)amount + 1;
    if (count > SIZE_MAX / sizeof(int)) return -1;
    int *best = malloc(count * sizeof(*best));
    if (!best) return -1;
    best[0] = 0;
    for (int i = 1; i <= amount; ++i) best[i] = amount + 1;
    for (int i = 0; i < k; ++i) {
        for (int subtotal = coins[i]; subtotal <= amount; ++subtotal) {
            int candidate = best[subtotal - coins[i]] + 1;
            if (candidate < best[subtotal]) best[subtotal] = candidate;
        }
    }
    *out = best[amount] == amount + 1 ? -1 : best[amount];
    free(best);
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const int coins[] = {1, 3, 4}, even[] = {2}, invalid[] = {0};
    int result = 0;
    int status = min_coins(even, 1, 3, &result);
    assert(status == 1 && result == -1);
    status = min_coins(NULL, 0, 0, &result);
    assert(status == 1 && result == 0);
    status = min_coins(invalid, 1, 0, &result);
    assert(status == 0);
    status = min_coins(coins, 3, 6, &result);
    assert(status == 1 && result == 2);
    if (status != 1) return 1;
    printf("Minimum coins: %d\n", result);
    return 0;
}
#endif
