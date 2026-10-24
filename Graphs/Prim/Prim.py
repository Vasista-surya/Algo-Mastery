"""Dense-selection Prim minimum spanning FOREST, O(V^2 + E) time.

Undirected integer-weight edges, integer vertices [0, n). Supply each edge
once; parallel edges and loops accepted. Negative weights allowed. Restart
at the smallest unvisited vertex for disconnected components. Empty ->
([], 0). Return (selected_edges, total), normalized u <= v. Ties use vertex,
then parent order. O(V + E) space; unbounded integer totals; no mutation.
"""

from math import inf


def prim(n, edges):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    adjacency = [[] for _ in range(n)]
    for u, v, weight in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        if type(weight) is not int:
            raise ValueError("weights must be integers")
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))
    key, parent, used = [inf] * n, [-1] * n, [False] * n
    forest, total = [], 0
    for _ in range(n):
        u = min((v for v in range(n) if not used[v]),
                key=lambda v: (key[v], v))
        used[u] = True
        if parent[u] != -1:
            forest.append((min(u, parent[u]), max(u, parent[u]), key[u]))
            total += key[u]
        for v, weight in adjacency[u]:
            if not used[v] and (weight < key[v] or
                               (weight == key[v] and u < parent[v])):
                key[v], parent[v] = weight, u
    return forest, total


if __name__ == "__main__":
    result = prim(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (3, 4, -1)])
    assert result[1] == 2 and len(result[0]) == 3
    assert prim(0, []) == ([], 0)
    assert prim(1, [(0, 0, -9)]) == ([], 0)
    print("Forest and total:", result)
