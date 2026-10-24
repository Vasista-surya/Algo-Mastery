/* C99 directed all-pairs shortest paths, O(V^3+E) time, O(V^2) output.
 * Vertices [0,n), V<=128, E<=4096, weights [-10^9,10^9]. Both arcs for
 * undirected graphs. INF=LLONG_MAX; zero diagonal, minimum parallel arc.
 * Flat caller-owned output: distance[u*n+v], capacity in long long elements.
 * 0 success, 1 ANY negative cycle, -1 invalid, -2 capacity < n*n,
 * -3 numeric overflow/reserved infinity. Ignore output on nonzero status.
 * Empty succeeds; NULL buffers only for zero sizes. No allocation.
 */
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
#define INF LLONG_MAX
typedef struct { int u, v; long long weight; } Edge;

static int checked_add(long long a, long long b, long long *sum) {
    if ((b > 0 && a > LLONG_MAX - b) || (b < 0 && a < LLONG_MIN - b)) return 0;
    *sum = a + b;
    return *sum != INF;
}

int floyd_warshall(int n, const Edge *edges, size_t m,
                   long long *distance, size_t capacity) {
    size_t cells;
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges)) return -1;
    cells = (size_t)n * (size_t)n; /* bounded before multiplication */
    if (capacity < cells || (cells && !distance)) return -2;
    for (size_t i = 0; i < m; ++i) {
        const Edge e = edges[i];
        if (e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
            e.weight < -1000000000LL || e.weight > 1000000000LL) return -1;
    }
    for (size_t i = 0; i < cells; ++i) distance[i] = INF;
    for (int v = 0; v < n; ++v) distance[v * n + v] = 0;
    for (size_t i = 0; i < m; ++i) {
        const Edge e = edges[i];
        if (e.weight < distance[e.u * n + e.v]) distance[e.u * n + e.v] = e.weight;
    }
    for (int k = 0; k < n; ++k) {
        /* Check every round, avoiding amplification of negative cycles. */
        for (int v = 0; v < n; ++v) if (distance[v * n + v] < 0) return 1;
        for (int u = 0; u < n; ++u) {
            if (distance[u * n + k] == INF) continue;
            for (int v = 0; v < n; ++v) {
                long long candidate;
                if (distance[k * n + v] == INF) continue;
                if (!checked_add(distance[u * n + k], distance[k * n + v], &candidate)) return -3;
                if (candidate < distance[u * n + v]) distance[u * n + v] = candidate;
            }
        }
    }
    for (int v = 0; v < n; ++v) if (distance[v * n + v] < 0) return 1;
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Edge edges[] = {{0, 1, 4}, {1, 2, -6}}, cycle[] = {{1, 1, -1}};
    long long distance[9];
    int status = floyd_warshall(3, edges, 2, distance, 9);
    assert(status == 0);
    if (status != 0) return 1;
    assert(distance[0] == 0 && distance[1] == 4 && distance[2] == -2 && distance[6] == INF);
    printf("Row 0: %lld %lld %lld\n", distance[0], distance[1], distance[2]);
    assert(floyd_warshall(2, cycle, 1, distance, 9) == 1);
    assert(floyd_warshall(0, NULL, 0, NULL, 0) == 0);
    assert(floyd_warshall(3, edges, 2, distance, 1) == -2);
    return 0;
}
#endif
