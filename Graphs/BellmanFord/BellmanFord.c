/* C99 synchronous Bellman-Ford, O(VE+V^2) time, fixed workspace.
 * Directed arcs, vertices [0,n), V<=128, E<=4096, weights [-10^9,10^9].
 * Both arcs for undirected graphs. INF=LLONG_MAX; empty has no source.
 * 0 success, 1 SOURCE-REACHABLE negative cycle, -1 invalid, -2 capacity < n.
 * Ignore output on nonzero status. Unreachable negative cycles are ignored.
 * Synchronous rounds use at most V edges, bounding sums by 128*10^9.
 * Caller-owned buffers, no allocation; NULL edges allowed only for m=0.
 */
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
#define INF LLONG_MAX
typedef struct { int u, v; long long weight; } Edge;

int bellman_ford(int n, const Edge *edges, size_t m, int source,
                 long long *distance, size_t capacity) {
    long long updated[MAX_VERTICES];
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges) ||
        source < 0 || source >= n) return -1;
    if (capacity < (size_t)n || !distance) return -2;
    for (size_t i = 0; i < m; ++i) {
        const Edge e = edges[i];
        if (e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
            e.weight < -1000000000LL || e.weight > 1000000000LL) return -1;
    }
    for (int v = 0; v < n; ++v) distance[v] = INF;
    distance[source] = 0;
    for (int step = 1; step < n; ++step) {
        int changed = 0;
        for (int v = 0; v < n; ++v) updated[v] = distance[v];
        for (size_t i = 0; i < m; ++i) {
            const Edge e = edges[i];
            if (distance[e.u] != INF) {
                long long candidate = distance[e.u] + e.weight;
                if (candidate < updated[e.v]) { updated[e.v] = candidate; changed = 1; }
            }
        }
        for (int v = 0; v < n; ++v) distance[v] = updated[v];
        if (!changed) break;
    }
    for (size_t i = 0; i < m; ++i) {
        const Edge e = edges[i];
        if (distance[e.u] != INF && distance[e.u] + e.weight < distance[e.v]) return 1;
    }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Edge edges[] = {{0, 1, 4}, {1, 2, -6}}, cycle[] = {{1, 1, -1}};
    long long distance[4];
    int status = bellman_ford(4, edges, 2, 0, distance, 4);
    assert(status == 0);
    if (status != 0) return 1;
    assert(distance[0] == 0 && distance[1] == 4 && distance[2] == -2 && distance[3] == INF);
    printf("Distances: %lld %lld %lld INF\n", distance[0], distance[1], distance[2]);
    assert(bellman_ford(2, cycle, 1, 0, distance, 4) == 0 && distance[1] == INF);
    assert(bellman_ford(2, cycle, 1, 1, distance, 4) == 1);
    assert(bellman_ford(0, NULL, 0, 0, distance, 4) == -1);
    return 0;
}
#endif
