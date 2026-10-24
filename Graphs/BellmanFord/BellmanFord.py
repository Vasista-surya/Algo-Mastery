"""Bellman-Ford on directed integer-weight arcs: O(VE + V^2) time.

Uses synchronous relaxation (copy each round), O(V + E) space. Vertices
are integers [0, n); use both arcs for undirected graphs. Negative weights
are allowed. A source-reachable negative cycle raises ValueError; an
unreachable cycle is ignored. Unreachable = math.inf; finite distances use
unbounded integers. An empty graph has no valid source.
"""

from math import inf


def bellman_ford(n, edges, source):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if type(source) is not int or not 0 <= source < n:
        raise ValueError("source outside [0, n)")
    edges = list(edges)
    for u, v, weight in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        if type(weight) is not int:
            raise ValueError("weights must be integers")
    distance = [inf] * n
    distance[source] = 0
    for _ in range(n - 1):
        updated = distance.copy()
        for u, v, weight in edges:
            if distance[u] != inf:
                updated[v] = min(updated[v], distance[u] + weight)
        if updated == distance:
            break
        distance = updated
    for u, v, weight in edges:
        if distance[u] != inf and distance[u] + weight < distance[v]:
            raise ValueError("source-reachable negative cycle")
    return distance


if __name__ == "__main__":
    result = bellman_ford(4, [(0, 1, 4), (1, 2, -6)], 0)
    assert result == [0, 4, -2, inf]
    assert bellman_ford(2, [(1, 1, -1)], 0) == [0, inf]
    try:
        bellman_ford(2, [(0, 1, 0), (1, 1, -1)], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("negative cycle accepted")
    print("Distances:", result)
