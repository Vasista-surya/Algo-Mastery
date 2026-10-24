"""Exact directed TSP by depth-first branch-and-bound, start/end vertex 0.

Square integer matrix, n<=12, diagonal 0; -1 is absent, 0..10^9 are edge
weights (zero is an edge). Returns (cost, path_tuple), or None for no tour.
Empty graph -> (0, ()); singleton -> (0, (0,0)) with no edge traversal.
O(n^2*n!) worst time, O(n) auxiliary search space, besides the input.
Nonnegative weights and bounded n/weights keep all costs <=12*10^9.
"""


def traveling_salesman(matrix):
    if not isinstance(matrix, (list, tuple)) or len(matrix) > 12:
        raise ValueError("a square matrix of at most 12 vertices required")
    n = len(matrix)
    for i, row in enumerate(matrix):
        if not isinstance(row, (list, tuple)) or len(row) != n:
            raise ValueError("matrix must be square")
        for j, weight in enumerate(row):
            if type(weight) is not int or not -1 <= weight <= 10**9:
                raise ValueError("edge must be -1 (absent) or an integer in [0,10^9]")
            if i == j and weight != 0:
                raise ValueError("diagonal must be zero")
    if n == 0:
        return 0, ()
    if n == 1:
        return 0, (0, 0)
    visited = [False] * n
    visited[0] = True
    path = [0]
    best_cost, best_path = None, None

    def lower_bound(last, cost):
        # In any completion, last and every unvisited vertex need one outgoing
        # edge to an unvisited vertex or 0. Relaxing distinct destinations and
        # cycle order can only reduce the cost, hence this is a lower bound.
        bound = cost
        for source in range(n):
            if visited[source] and source != last:
                continue
            cheapest = None
            for destination in range(n):
                if destination == source or (visited[destination] and destination != 0):
                    continue
                weight = matrix[source][destination]
                if weight >= 0 and (cheapest is None or weight < cheapest):
                    cheapest = weight
            if cheapest is None:
                return None  # No completion can supply this required edge.
            bound += cheapest
        return bound

    def search(last, cost):
        nonlocal best_cost, best_path
        if len(path) == n:
            closing = matrix[last][0]
            if closing >= 0 and (best_cost is None or cost + closing < best_cost):
                best_cost, best_path = cost + closing, tuple(path) + (0,)
            return
        bound = lower_bound(last, cost)
        if bound is None or (best_cost is not None and bound >= best_cost):
            return
        for vertex in range(1, n):
            weight = matrix[last][vertex]
            if visited[vertex] or weight < 0:
                continue
            # A second, weaker bound is the already-paid nonnegative cost.
            if best_cost is not None and cost + weight >= best_cost:
                continue
            visited[vertex] = True
            path.append(vertex)
            search(vertex, cost + weight)
            path.pop()
            visited[vertex] = False

    search(0, 0)
    return None if best_cost is None else (best_cost, best_path)


def main():
    matrix = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    assert traveling_salesman(matrix) == (80, (0, 1, 3, 2, 0))
    assert traveling_salesman([]) == (0, ())
    assert traveling_salesman([[0]]) == (0, (0, 0))
    assert traveling_salesman([[0, 0, -1], [-1, 0, 2], [3, -1, 0]]) == (5, (0, 1, 2, 0))
    assert traveling_salesman([[0, 1], [-1, 0]]) is None
    assert traveling_salesman([[0, 0], [0, 0]]) == (0, (0, 1, 0))
    print("Minimum tour (cost, path):", traveling_salesman(matrix))


if __name__ == "__main__":
    main()
