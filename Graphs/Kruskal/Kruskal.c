/* C99 undirected minimum spanning FOREST. Vertices [0,n), V<=128,
 * E<=4096, weights [-10^9,10^9]. One entry per edge; parallel edges allowed,
 * loops ignored. Empty/disconnected valid. Normalized endpoints, deterministic
 * (weight,u,v) sorting. O(V+E log E) with O(E log E) qsort; fixed workspace.
 * 0 success, -1 invalid, -2 output capacity < max(n-1,0).
 * Caller-owned, nonoverlapping buffers; no allocation. NULL for zero sizes.
 * Bounded totals (at most 127 edges) cannot overflow long long.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
typedef struct { int u, v; long long weight; } Edge;

static int compare_edges(const void *left, const void *right) {
    const Edge *a = left, *b = right;
    if (a->weight != b->weight) return (a->weight > b->weight) ? 1 : -1;
    if (a->u != b->u) return (a->u > b->u) ? 1 : -1;
    return (a->v > b->v) - (a->v < b->v);
}

static int root(int *parent, int v) {
    while (parent[v] != v) { parent[v] = parent[parent[v]]; v = parent[v]; }
    return v;
}

int kruskal(int n, const Edge *edges, size_t m, Edge *forest,
            size_t capacity, size_t *count, long long *total) {
    Edge ordered[MAX_EDGES];
    int parent[MAX_VERTICES], size[MAX_VERTICES];
    size_t needed;
    if (!count || !total) return -1;
    *count = 0; *total = 0;
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges)) return -1;
    needed = n > 0 ? (size_t)(n - 1) : 0;
    if (capacity < needed || (needed && !forest)) return -2;
    for (size_t i = 0; i < m; ++i) {
        Edge e = edges[i];
        if (e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
            e.weight < -1000000000LL || e.weight > 1000000000LL) return -1;
        if (e.u > e.v) { int swap = e.u; e.u = e.v; e.v = swap; }
        ordered[i] = e;
    }
    qsort(ordered, m, sizeof(ordered[0]), compare_edges);
    for (int v = 0; v < n; ++v) { parent[v] = v; size[v] = 1; }
    for (size_t i = 0; i < m; ++i) {
        Edge e = ordered[i];
        int a = root(parent, e.u), b = root(parent, e.v);
        if (a == b) continue;
        if (size[a] < size[b]) { int swap = a; a = b; b = swap; }
        parent[b] = a;
        size[a] += size[b];
        forest[(*count)++] = e;
        *total += e.weight;
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
    int status = kruskal(5, edges, 4, forest, 4, &count, &total);
    assert(status == 0 && count == 3 && total == 2);
    if (status != 0) return 1;
    printf("Forest total: %lld; edges: %zu\n", total, count);
    assert(kruskal(0, NULL, 0, NULL, 0, &count, &total) == 0 && total == 0);
    assert(kruskal(1, loop, 1, NULL, 0, &count, &total) == 0 && count == 0);
    assert(kruskal(5, edges, 4, forest, 1, &count, &total) == -2);
    return 0;
}
#endif
