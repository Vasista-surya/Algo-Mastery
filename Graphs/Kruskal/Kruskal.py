"""Minimum spanning FOREST for undirected integer-weight edges.

Vertices are integers [0, n). Supply each edge once; duplicates and loops
are accepted (loops are never selected). Negative weights are allowed.
Disconnected and empty inputs are valid. Return (selected_edges, total),
with normalized endpoints u <= v. O(V + E log E) time, O(V + E) space.
Finite totals use unbounded integers. Input is not modified.
"""


def kruskal(n, edges):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    ordered = []
    for u, v, weight in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        if type(weight) is not int:
            raise ValueError("weights must be integers")
        ordered.append((weight, min(u, v), max(u, v)))
    ordered.sort()
    parent = list(range(n))
    size = [1] * n

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    forest, total = [], 0
    for weight, u, v in ordered:
        a, b = root(u), root(v)
        if a == b:
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        forest.append((u, v, weight))
        total += weight
    return forest, total


if __name__ == "__main__":
    result = kruskal(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (3, 4, -1)])
    assert result[1] == 2 and len(result[0]) == 3
    assert kruskal(0, []) == ([], 0)
    assert kruskal(1, [(0, 0, -9)]) == ([], 0)
    print("Forest and total:", result)
