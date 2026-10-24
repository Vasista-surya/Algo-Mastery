"""Breadth-first traversal of directed arcs; O(V + E) time and space.

Vertices are integers in [0, n). For undirected graphs supply both arcs.
Only source-reachable vertices are returned, in input-neighbor order.
An empty graph has no valid source. Invalid input raises ValueError.
"""

from collections import deque


def bfs(n, edges, source):
    """Return BFS vertex order for an iterable of (u, v) edges."""
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if type(source) is not int or not 0 <= source < n:
        raise ValueError("source outside [0, n)")
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        adjacency[u].append(v)
    seen = {source}
    queue = deque([source])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return order


if __name__ == "__main__":
    result = bfs(5, [(0, 1), (0, 2), (1, 3), (2, 3)], 0)
    assert result == [0, 1, 2, 3]
    assert bfs(2, [], 1) == [1]
    try:
        bfs(0, [], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("empty graph accepted a source")
    print("BFS:", result)
