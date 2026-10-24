/* C99 iterative directed DFS preorder, O(V+E) time, no recursion/allocation.
 * Vertices [0,n); both arcs for undirected edges. Source component only,
 * input-neighbor order. Checked limits V<=128, E<=4096.
 * 0 success, -1 invalid input/source, -2 output capacity < n or NULL output.
 * Caller owns buffers; NULL edges only for m=0; empty has no valid source.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
typedef struct { int u, v; } Edge;

int dfs(int n, const Edge *edges, size_t m, int source,
        int *order, size_t capacity, size_t *count) {
    int offsets[MAX_VERTICES + 1] = {0}, next[MAX_VERTICES];
    int adjacency[MAX_EDGES], stack[MAX_VERTICES], seen[MAX_VERTICES] = {0};
    int depth = 0;
    if (!count) return -1;
    *count = 0;
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges) ||
        source < 0 || source >= n) return -1;
    if (capacity < (size_t)n || !order) return -2;
    for (size_t i = 0; i < m; ++i) {
        if (edges[i].u < 0 || edges[i].u >= n || edges[i].v < 0 || edges[i].v >= n)
            return -1;
        ++offsets[edges[i].u + 1];
    }
    for (int v = 0; v < n; ++v) {
        offsets[v + 1] += offsets[v];
        next[v] = offsets[v];
    }
    for (size_t i = 0; i < m; ++i) adjacency[next[edges[i].u]++] = edges[i].v;
    for (int v = 0; v < n; ++v) next[v] = offsets[v];
    seen[source] = 1;
    order[(*count)++] = source;
    stack[depth++] = source;
    while (depth) {
        int u = stack[depth - 1];
        if (next[u] == offsets[u + 1]) {
            --depth;
        } else {
            int v = adjacency[next[u]++];
            if (!seen[v]) {
                seen[v] = 1;
                order[(*count)++] = v;
                stack[depth++] = v;
            }
        }
    }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Edge edges[] = {{0, 1}, {0, 2}, {1, 3}, {3, 0}};
    int order[5];
    size_t count;
    int status = dfs(5, edges, 4, 0, order, 5, &count);
    assert(status == 0 && count == 4);
    if (status != 0) return 1;
    assert(order[0] == 0 && order[1] == 1 && order[2] == 3 && order[3] == 2);
    printf("DFS:");
    for (size_t i = 0; i < count; ++i) printf(" %d", order[i]);
    puts("");
    assert(dfs(0, NULL, 0, 0, order, 5, &count) == -1);
    assert(dfs(5, edges, 4, 0, order, 1, &count) == -2);
    assert(dfs(2, NULL, 0, 1, order, 5, &count) == 0 && count == 1);
    return 0;
}
#endif
