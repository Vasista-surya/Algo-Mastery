/* Iterative Fibonacci DP: O(n) time, O(1) space.
 * unsigned long long (at least 64 bits in C99) supports F(0)..F(93).
 * Return 1 on success, 0 on invalid n or NULL out. Failure leaves out alone.
 */
#include <assert.h>
#include <stdio.h>

int fibonacci(int n, unsigned long long *out) {
    unsigned long long previous = 0, current = 1;
    if (!out || n < 0 || n > 93) return 0;
    if (n == 0) { *out = 0; return 1; }
    for (int i = 2; i <= n; ++i) {
        unsigned long long next = previous + current;
        previous = current;
        current = next;
    }
    *out = current;
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    unsigned long long value = 0;
    int ok = fibonacci(0, &value);
    assert(ok && value == 0);
    ok = fibonacci(93, &value);
    assert(ok && value == 12200160415121876738ULL);
    ok = fibonacci(94, &value);
    assert(!ok);
    ok = fibonacci(-1, &value);
    assert(!ok);
    ok = fibonacci(10, &value);
    assert(ok && value == 55);
    if (!ok) return 1;
    printf("F(10) = %llu\n", value);
    return 0;
}
#endif
