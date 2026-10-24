"""Iterative DFS preorder on directed arcs; O(V + E) time and space.

Integer vertices lie in [0, n); supply both arcs for an undirected edge.
Visit only the source component, following input-neighbor order. An empty
graph has no valid source. No recursion-depth dependency; invalid input
raises ValueError.
"""


def dfs(n, edges, source):
    """Return DFS vertex order for an iterable of (u, v) edges."""
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
    order = [source]
    stack = [iter(adjacency[source])]
    while stack:
        v = next(stack[-1], None)
        if v is None:
            stack.pop()
        elif v not in seen:
            seen.add(v)
            order.append(v)
            stack.append(iter(adjacency[v]))
    return order


if __name__ == "__main__":
    result = dfs(5, [(0, 1), (0, 2), (1, 3), (3, 0)], 0)
    assert result == [0, 1, 3, 2]
    assert dfs(2, [], 1) == [1]
    try:
        dfs(2, [(1, 2)], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid vertex accepted")
    print("DFS:", result)
