/* C99 divisible-item knapsack; N<=4096, integer value 0..10^9,
 * weight 1..10^9, capacity 0..10^9. Exact ratio order via bounded long long
 * cross-products; ties by input index. Approximate double total/shares in
 * original order; zero-value items skipped. Empty/zero capacity valid.
 * O(N log N) with O(N log N) qsort; fixed workspace, no allocation.
 * 0 success, -1 invalid, -2 shares capacity < n. Caller-owned nonoverlapping
 * buffers; NULL arrays only for n=0. Products <=10^18, total <=4096*10^9.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

enum { MAX_ITEMS = 4096 };
typedef struct { long long value, weight; } Item;
typedef struct { Item item; size_t index; } IndexedItem;

static int compare_items(const void *left, const void *right) {
    const IndexedItem *a = left, *b = right;
    long long lhs = a->item.value * b->item.weight;
    long long rhs = b->item.value * a->item.weight;
    if (lhs != rhs) return lhs > rhs ? -1 : 1;
    return (a->index > b->index) - (a->index < b->index);
}

int fractional_knapsack(const Item *items, size_t n, long long capacity,
                        double *shares, size_t shares_capacity, double *total) {
    IndexedItem ordered[MAX_ITEMS];
    if (!total) return -1;
    *total = 0;
    if (n > MAX_ITEMS || (n && !items) || capacity < 0 || capacity > 1000000000LL) return -1;
    if (shares_capacity < n || (n && !shares)) return -2;
    for (size_t i = 0; i < n; ++i) {
        if (items[i].value < 0 || items[i].value > 1000000000LL ||
            items[i].weight <= 0 || items[i].weight > 1000000000LL) return -1;
        ordered[i].item = items[i]; ordered[i].index = i;
    }
    for (size_t i = 0; i < n; ++i) shares[i] = 0;
    qsort(ordered, n, sizeof(ordered[0]), compare_items);
    for (size_t i = 0; i < n; ++i) {
        Item item = ordered[i].item;
        long long taken;
        if (capacity == 0 || item.value == 0) break;
        taken = capacity < item.weight ? capacity : item.weight;
        shares[ordered[i].index] = (double)taken / (double)item.weight;
        *total += shares[ordered[i].index] * (double)item.value;
        capacity -= taken;
    }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Item items[] = {{60, 10}, {100, 20}, {120, 30}}, invalid[] = {{1, 0}};
    double shares[3], total;
    int status = fractional_knapsack(items, 3, 50, shares, 3, &total);
    assert(status == 0 && total > 239.999999 && total < 240.000001);
    if (status != 0) return 1;
    assert(shares[0] == 1 && shares[1] == 1 && shares[2] > 0.666666 && shares[2] < 0.666667);
    printf("Value: %.6f; shares: %.6f %.6f %.6f\n", total, shares[0], shares[1], shares[2]);
    assert(fractional_knapsack(NULL, 0, 5, NULL, 0, &total) == 0 && total == 0);
    assert(fractional_knapsack(invalid, 1, 0, shares, 3, &total) == -1);
    assert(fractional_knapsack(items, 3, 50, shares, 1, &total) == -2);
    return 0;
}
#endif
