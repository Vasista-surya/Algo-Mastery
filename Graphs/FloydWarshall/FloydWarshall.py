"""All-pairs shortest paths: O(V^3 + E) time, O(V^2) space.

Directed integer-weight (u, v, weight) arcs, vertices [0, n). Supply both
arcs for undirected graphs. Negative edges allowed; ANY negative cycle
raises ValueError. Unreachable = math.inf; finite integers cannot overflow.
Parallel arcs use their minimum; diagonal is initially zero; empty -> [].
"""

from math import inf


def floyd_warshall(n, edges):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    distance = [[inf] * n for _ in range(n)]
    for v in range(n):
        distance[v][v] = 0
    for u, v, weight in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        if type(weight) is not int:
            raise ValueError("weights must be integers")
        distance[u][v] = min(distance[u][v], weight)
    for k in range(n):
        if any(distance[v][v] < 0 for v in range(n)):
            raise ValueError("negative cycle")
        for u in range(n):
            if distance[u][k] == inf:
                continue
            for v in range(n):
                if distance[k][v] != inf:
                    distance[u][v] = min(distance[u][v],
                                         distance[u][k] + distance[k][v])
    if any(distance[v][v] < 0 for v in range(n)):
        raise ValueError("negative cycle")
    return distance


if __name__ == "__main__":
    result = floyd_warshall(3, [(0, 1, 4), (1, 2, -6)])
    assert result[0] == [0, 4, -2] and result[2][0] == inf
    assert floyd_warshall(0, []) == []
    try:
        floyd_warshall(1, [(0, 0, -1)])
    except ValueError:
        pass
    else:
        raise AssertionError("negative cycle accepted")
    print("Distances:", result)
