/* C99 Kahn topological sort of directed arcs; vertices [0,n).
 * O(V+E) time; fixed workspace, no allocation. V<=128, E<=4096.
 * FIFO ties: ascending initial vertices, then input-neighbor order.
 * Includes isolated vertices; empty succeeds. 0 success, 1 cycle,
 * -1 invalid, -2 output capacity < n. Ignore output on any nonzero status.
 * Caller owns buffers; NULL edges/output permitted for zero corresponding size.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

enum { MAX_VERTICES = 128, MAX_EDGES = 4096 };
typedef struct { int u, v; } Edge;

int topological_sort(int n, const Edge *edges, size_t m,
                     int *order, size_t capacity, size_t *count) {
    int offsets[MAX_VERTICES + 1] = {0}, cursor[MAX_VERTICES];
    int adjacency[MAX_EDGES], queue[MAX_VERTICES], indegree[MAX_VERTICES] = {0};
    int head = 0, tail = 0;
    if (!count) return -1;
    *count = 0;
    if (n < 0 || n > MAX_VERTICES || m > MAX_EDGES || (m && !edges)) return -1;
    if (capacity < (size_t)n || (n && !order)) return -2;
    for (size_t i = 0; i < m; ++i) {
        if (edges[i].u < 0 || edges[i].u >= n || edges[i].v < 0 || edges[i].v >= n)
            return -1;
        ++offsets[edges[i].u + 1];
        ++indegree[edges[i].v];
    }
    for (int v = 0; v < n; ++v) {
        offsets[v + 1] += offsets[v];
        cursor[v] = offsets[v];
        if (!indegree[v]) queue[tail++] = v;
    }
    for (size_t i = 0; i < m; ++i) adjacency[cursor[edges[i].u]++] = edges[i].v;
    while (head < tail) {
        int u = queue[head++];
        order[(*count)++] = u;
        for (int i = offsets[u]; i < offsets[u + 1]; ++i) {
            int v = adjacency[i];
            if (--indegree[v] == 0) queue[tail++] = v;
        }
    }
    if (*count != (size_t)n) { *count = 0; return 1; }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Edge edges[] = {{0, 2}, {1, 2}, {2, 3}}, cycle[] = {{0, 0}};
    int order[4];
    size_t count;
    int status = topological_sort(4, edges, 3, order, 4, &count);
    assert(status == 0 && count == 4);
    if (status != 0) return 1;
    for (int i = 0; i < 4; ++i) assert(order[i] == i);
    printf("Topological order:");
    for (size_t i = 0; i < count; ++i) printf(" %d", order[i]);
    puts("");
    assert(topological_sort(1, cycle, 1, order, 4, &count) == 1);
    assert(topological_sort(0, NULL, 0, NULL, 0, &count) == 0 && count == 0);
    assert(topological_sort(4, edges, 3, order, 1, &count) == -2);
    return 0;
}
#endif
