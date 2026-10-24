/* C99 dense Prim minimum spanning FOREST, O(V^2+E) time, O(V^2) workspace.
 * Undirected edges, vertices [0,n), V<=128, E<=4096, weights [-10^9,10^9].
 * Supply each edge once. Parallel/negative edges allowed; loops ignored.
 * Restart at smallest unvisited vertex; ties by vertex then parent.
 * Empty/disconnected valid; normalized output. INF is internal missing edge.
 * 0 success, -1 invalid, -2 output capacity < max(n-1,0).
 * Caller owns nonoverlapping buffers; NULL for zero sizes. No allocation.
 * Fixed matrix uses about 128 KiB (8-byte long long); totals cannot overflow.
 */
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
typedef struct { int u, v; long long weight; } Edge;

int prim(int n, const Edge *edges, size_t m, Edge *forest,
         size_t capacity, size_t *count, long long *total) {
    long long matrix[MAX_VERTICES][MAX_VERTICES], key[MAX_VERTICES];
    int parent[MAX_VERTICES], used[MAX_VERTICES] = {0};
    size_t needed;
    if (!count || !total) return -1;
    *count = 0; *total = 0;
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges)) return -1;
    needed = n > 0 ? (size_t)(n - 1) : 0;
    if (capacity < needed || (needed && !forest)) return -2;
    for (int u = 0; u < n; ++u) {
        key[u] = LLONG_MAX; parent[u] = -1;
        for (int v = 0; v < n; ++v) matrix[u][v] = LLONG_MAX;
    }
    for (size_t i = 0; i < m; ++i) {
        const Edge e = edges[i];
        if (e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
            e.weight < -1000000000LL || e.weight > 1000000000LL) return -1;
        if (e.weight < matrix[e.u][e.v]) {
            /* Separate stores also handle self-loops without overlapping writes. */
            matrix[e.u][e.v] = e.weight;
            matrix[e.v][e.u] = e.weight;
        }
    }
    for (int step = 0; step < n; ++step) {
        int u = -1;
        for (int v = 0; v < n; ++v)
            if (!used[v] && (u == -1 || key[v] < key[u])) u = v;
        used[u] = 1;
        if (parent[u] != -1) {
            Edge e = {u < parent[u] ? u : parent[u], u > parent[u] ? u : parent[u], key[u]};
            forest[(*count)++] = e;
            *total += key[u];
        }
        for (int v = 0; v < n; ++v)
            if (!used[v] && matrix[u][v] != LLONG_MAX &&
                (matrix[u][v] < key[v] || (matrix[u][v] == key[v] && u < parent[v]))) {
                key[v] = matrix[u][v]; parent[v] = u;
            }
    }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Edge edges[] = {{0, 1, 4}, {0, 2, 1}, {1, 2, 2}, {3, 4, -1}};
    const Edge loop[] = {{0, 0, -9}};
    Edge forest[4];
    size_t count;
    long long total;
    int status = prim(5, edges, 4, forest, 4, &count, &total);
    assert(status == 0 && count == 3 && total == 2);
    if (status != 0) return 1;
    printf("Forest total: %lld; edges: %zu\n", total, count);
    assert(prim(0, NULL, 0, NULL, 0, &count, &total) == 0 && total == 0);
    assert(prim(1, loop, 1, NULL, 0, &count, &total) == 0 && count == 0);
    assert(prim(5, edges, 4, forest, 1, &count, &total) == -2);
    return 0;
}
#endif
