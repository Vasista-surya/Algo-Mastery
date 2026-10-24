"""Dense-selection Dijkstra: O(V^2 + E) time, O(V + E) space.

Directed (u, v, weight) arcs, integer vertices [0, n), integer weights >= 0.
Supply both arcs for undirected edges. All negative edges are rejected,
including unreachable ones. Unreachable distances are math.inf. Python
integers avoid finite-distance overflow. Empty graphs have no valid source.
"""

from math import inf


def dijkstra(n, edges, source):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if type(source) is not int or not 0 <= source < n:
        raise ValueError("source outside [0, n)")
    adjacency = [[] for _ in range(n)]
    for u, v, weight in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        if type(weight) is not int or weight < 0:
            raise ValueError("weights must be nonnegative integers")
        adjacency[u].append((v, weight))
    distance = [inf] * n
    distance[source] = 0
    used = [False] * n
    for _ in range(n):
        u = min((v for v in range(n) if not used[v]),
                key=lambda v: (distance[v], v), default=None)
        if u is None or distance[u] == inf:
            break
        used[u] = True
        for v, weight in adjacency[u]:
            distance[v] = min(distance[v], distance[u] + weight)
    return distance


if __name__ == "__main__":
    result = dijkstra(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0)
    assert result == [0, 3, 1, inf]
    assert dijkstra(1, [], 0) == [0]
    try:
        dijkstra(2, [(1, 1, -1)], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("negative edge accepted")
    print("Distances:", result)
