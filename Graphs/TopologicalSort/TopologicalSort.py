"""Kahn's topological sort: O(V + E) time and space.

Directed (u, v) arcs with integer vertices in [0, n). Includes isolated
vertices. FIFO ties: initial vertices ascending, then input-neighbor order.
Empty graph returns []; any cycle (including a self-loop) raises ValueError.
"""

from collections import deque


def topological_sort(n, edges):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    adjacency = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        if any(type(x) is not int or not 0 <= x < n for x in (u, v)):
            raise ValueError("vertex outside [0, n)")
        adjacency[u].append(v)
        indegree[v] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) != n:
        raise ValueError("directed cycle")
    return order


if __name__ == "__main__":
    result = topological_sort(4, [(0, 2), (1, 2), (2, 3)])
    assert result == [0, 1, 2, 3]
    assert topological_sort(0, []) == []
    try:
        topological_sort(2, [(0, 1), (1, 0)])
    except ValueError:
        pass
    else:
        raise AssertionError("cycle accepted")
    print("Topological order:", result)
