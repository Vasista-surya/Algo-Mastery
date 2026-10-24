/* C99 directed Dijkstra, O(V^2+E) time, fixed workspace, no allocation.
 * Vertices [0,n), V<=128, E<=4096; weights 0..10^9 (all arcs validated).
 * Both arcs for undirected graphs. INF=LLONG_MAX means unreachable.
 * Empty has no source. Limits bound all finite sums by 128*10^9.
 * 0 success, -1 invalid/negative weight, -2 output capacity < n.
 * Caller owns buffers; NULL edges allowed only for m=0.
 */
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
#define INF LLONG_MAX
typedef struct { int u, v; long long weight; } Edge;

int dijkstra(int n, const Edge *edges, size_t m, int source,
             long long *distance, size_t capacity) {
    int offsets[MAX_VERTICES + 1] = {0}, cursor[MAX_VERTICES];
    int adjacency[MAX_EDGES], used[MAX_VERTICES] = {0};
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges) ||
        source < 0 || source >= n) return -1;
    if (capacity < (size_t)n || !distance) return -2;
    for (size_t i = 0; i < m; ++i) {
        const Edge e = edges[i];
        if (e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
            e.weight < 0 || e.weight > 1000000000LL) return -1;
        ++offsets[e.u + 1];
    }
    for (int v = 0; v < n; ++v) {
        offsets[v + 1] += offsets[v];
        cursor[v] = offsets[v];
        distance[v] = INF;
    }
    for (size_t i = 0; i < m; ++i) adjacency[cursor[edges[i].u]++] = (int)i;
    distance[source] = 0;
    for (int step = 0; step < n; ++step) {
        int u = -1;
        for (int v = 0; v < n; ++v)
            if (!used[v] && (u == -1 || distance[v] < distance[u])) u = v;
        if (u == -1 || distance[u] == INF) break;
        used[u] = 1;
        for (int i = offsets[u]; i < offsets[u + 1]; ++i) {
            const Edge e = edges[adjacency[i]];
            long long candidate = distance[u] + e.weight;
            if (candidate < distance[e.v]) distance[e.v] = candidate;
        }
    }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Edge edges[] = {{0, 1, 4}, {0, 2, 1}, {2, 1, 2}};
    const Edge negative[] = {{1, 1, -1}};
    long long distance[4];
    int status = dijkstra(4, edges, 3, 0, distance, 4);
    assert(status == 0);
    if (status != 0) return 1;
    assert(distance[0] == 0 && distance[1] == 3 && distance[2] == 1 && distance[3] == INF);
    printf("Distances: %lld %lld %lld INF\n", distance[0], distance[1], distance[2]);
    assert(dijkstra(2, negative, 1, 0, distance, 4) == -1);
    assert(dijkstra(0, NULL, 0, 0, distance, 4) == -1);
    assert(dijkstra(4, edges, 3, 0, distance, 1) == -2);
    return 0;
}
#endif
