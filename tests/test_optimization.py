"""Stdlib tests for the optimization/geometry examples; no compiler needed.

Run: python -m unittest discover -s tests -p test_optimization.py
The shared _loader provides path-based, side-effect-free module loading.
Small independent references protect recurrence, pruning, and boundary behavior.
"""
import collections
import itertools
import random
import unittest

from _loader import load


fibonacci = load("DynamicProgramming/Fibonacci/Fibonacci.py").fibonacci
knapsack_01 = load("DynamicProgramming/Knapsack01/Knapsack01.py").knapsack_01
lcs_length = load("DynamicProgramming/LongestCommonSubsequence/LongestCommonSubsequence.py").lcs_length
lis_length = load("DynamicProgramming/LongestIncreasingSubsequence/LongestIncreasingSubsequence.py").lis_length
min_coins = load("DynamicProgramming/CoinChange/CoinChange.py").min_coins
matrix_chain_cost = load("DynamicProgramming/MatrixChainMultiplication/MatrixChainMultiplication.py").matrix_chain_cost
n_queens = load("Backtracking/NQueens/NQueens.py").n_queens
solve_sudoku = load("Backtracking/SudokuSolver/SudokuSolver.py").solve_sudoku
enumeration = load("Backtracking/PermutationsAndCombinations/PermutationsAndCombinations.py")
traveling_salesman = load("BranchAndBound/TravelingSalesman/TravelingSalesman.py").traveling_salesman
convex_hull = load("DivideAndConquer/ConvexHull/ConvexHull.py").convex_hull


def subsequences(values):
    for mask in range(1 << len(values)):
        yield tuple(value for index, value in enumerate(values) if mask & (1 << index))


def brute_knapsack(weights, values, capacity):
    return max(
        sum(values[i] for i in range(len(weights)) if mask & (1 << i))
        for mask in range(1 << len(weights))
        if sum(weights[i] for i in range(len(weights)) if mask & (1 << i)) <= capacity
    )


def brute_coins(coins, amount):
    """BFS over reachable amounts, rather than the production DP recurrence."""
    queue = collections.deque([(0, 0)])
    seen = {0}
    while queue:
        subtotal, count = queue.popleft()
        if subtotal == amount:
            return count
        for coin in coins:
            following = subtotal + coin
            if following <= amount and following not in seen:
                seen.add(following)
                queue.append((following, count + 1))
    return -1


def brute_matrix_chain(dimensions):
    """Enumerate all parenthesizations without memoization, on tiny chains."""
    if len(dimensions) <= 2:
        return 0
    return min(
        brute_matrix_chain(dimensions[:split + 1])
        + brute_matrix_chain(dimensions[split:])
        + dimensions[0] * dimensions[split] * dimensions[-1]
        for split in range(1, len(dimensions) - 1)
    )


def brute_tsp(matrix):
    if not matrix:
        return 0, ()
    if len(matrix) == 1:
        return 0, (0, 0)
    best = None
    for middle in itertools.permutations(range(1, len(matrix))):
        path = (0,) + middle + (0,)
        edges = [matrix[a][b] for a, b in zip(path, path[1:])]
        if all(edge >= 0 for edge in edges):
            candidate = sum(edges), path
            if best is None or candidate < best:
                best = candidate
    return best


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def supporting_vertices(points):
    """Independent O(n^3) supporting-line reference, not monotone chain."""
    unique = sorted(set(points))
    if len(unique) <= 2:
        return set(unique)
    vertices = set()
    for a, b in itertools.combinations(unique, 2):
        orientations = [cross(a, b, point) for point in unique]
        if min(orientations) >= 0 or max(orientations) <= 0:
            on_line = [point for point in unique if cross(a, b, point) == 0]
            vertices.update((min(on_line), max(on_line)))
    return vertices


class FibonacciTests(unittest.TestCase):
    def test_known_values_and_recurrence(self):
        self.assertEqual([fibonacci(n) for n in range(11)], [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
        self.assertEqual(fibonacci(92), 7540113804746346429)
        self.assertEqual(fibonacci(93), 12200160415121876738)
        self.assertEqual(fibonacci(94), 19740274219868223167)
        for n in range(2, 100):
            self.assertEqual(fibonacci(n), fibonacci(n - 1) + fibonacci(n - 2))

    def test_practical_limit(self):
        self.assertEqual(fibonacci(10000), fibonacci(9999) + fibonacci(9998))

    def test_invalid_indices(self):
        for n in (-1, 10001, 1.5, True, "5", None):
            with self.subTest(n=n), self.assertRaises(ValueError):
                fibonacci(n)


class KnapsackTests(unittest.TestCase):
    def test_examples_empty_and_zero_weights(self):
        self.assertEqual(knapsack_01([10, 20, 30], [60, 100, 120], 50), 220)
        self.assertEqual(knapsack_01([], [], 0), 0)
        self.assertEqual(knapsack_01([], [], 100000), 0)
        self.assertEqual(knapsack_01([0, 0, 1], [5, 7, 100], 0), 12)
        self.assertEqual(knapsack_01([0, 2, 0], [5, 3, 7], 2), 15)
        self.assertEqual(knapsack_01([2], [3], 4), 3)
        self.assertEqual(knapsack_01([10**9], [10**9], 3), 0)
        self.assertEqual(knapsack_01([0] * 1000, [10**9] * 1000, 0), 10**12)

    def test_small_bruteforce(self):
        options = ((0, 0), (0, 4), (1, 2), (2, 3))
        for n in range(5):
            for items in itertools.product(options, repeat=n):
                weights = [item[0] for item in items]
                values = [item[1] for item in items]
                for capacity in range(5):
                    self.assertEqual(knapsack_01(weights, values, capacity),
                                     brute_knapsack(weights, values, capacity), (items, capacity))

    def test_invalid(self):
        cases = [([], [], -1), ([], [], 100001), ([], [], True), ([1], [], 0),
                 ([-1], [1], 2), ([1], [-1], 2), ([True], [1], 0),
                 ([1], [1.5], 0), ([10**9 + 1], [1], 0), ([1], [10**9 + 1], 0),
                 ([0] * 1001, [0] * 1001, 0), (None, [], 0)]
        for weights, values, capacity in cases:
            with self.subTest(capacity=capacity, weights=weights), self.assertRaises(ValueError):
                knapsack_01(weights, values, capacity)

    def test_no_mutation(self):
        weights, values = [0, 2, 1], [7, 3, 4]
        knapsack_01(weights, values, 2)
        self.assertEqual(weights, [0, 2, 1])
        self.assertEqual(values, [7, 3, 4])


class LCSTests(unittest.TestCase):
    def test_examples_and_unicode(self):
        self.assertEqual(lcs_length("AGGTAB", "GXTXAYB"), 4)
        self.assertEqual(lcs_length("", "abc"), 0)
        self.assertEqual(lcs_length("aaaa", "aa"), 2)
        self.assertEqual(lcs_length("abc", "xyz"), 0)
        self.assertEqual(lcs_length("\U0001f600x", "\U0001f600"), 1)
        self.assertEqual(lcs_length("a" * 2000, ""), 0)

    def test_small_bruteforce(self):
        words = ["".join(chars) for n in range(5) for chars in itertools.product("ab", repeat=n)]
        for a in words:
            left = set(subsequences(a))
            for b in words:
                expected = max(map(len, left.intersection(subsequences(b))))
                self.assertEqual(lcs_length(a, b), expected, (a, b))

    def test_invalid(self):
        for a, b in ((None, ""), ([], "a"), ("a", 1), ("x" * 2001, ""), ("", "x" * 2001)):
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                lcs_length(a, b)


class LISTests(unittest.TestCase):
    def test_examples_strictness_and_no_mutation(self):
        values = [10, 9, 2, 5, 3, 7, 101, 18]
        self.assertEqual(lis_length(values), 4)
        self.assertEqual(values, [10, 9, 2, 5, 3, 7, 101, 18])
        self.assertEqual(lis_length([]), 0)
        self.assertEqual(lis_length([2, 2, 2]), 1)
        self.assertEqual(lis_length([3, 2, 1]), 1)
        self.assertEqual(lis_length([-10**100, 0, 10**100]), 3)
        self.assertEqual(lis_length(list(range(100000))), 100000)

    def test_small_bruteforce(self):
        for n in range(6):
            for values in itertools.product((-1, 0, 1), repeat=n):
                expected = max(len(seq) for seq in subsequences(values)
                               if all(a < b for a, b in zip(seq, seq[1:])))
                self.assertEqual(lis_length(values), expected, values)

    def test_invalid(self):
        for values in (None, "123", [1, True], [1, 2.5], [0] * 100001):
            with self.subTest(kind=type(values).__name__), self.assertRaises(ValueError):
                lis_length(values)


class CoinChangeTests(unittest.TestCase):
    def test_examples_empty_and_duplicates(self):
        self.assertEqual(min_coins([1, 3, 4], 6), 2)
        self.assertEqual(min_coins([2], 3), -1)
        self.assertEqual(min_coins([], 0), 0)
        self.assertEqual(min_coins([], 5), -1)
        self.assertEqual(min_coins([2, 2], 4), 2)
        self.assertEqual(min_coins([10**9], 5), -1)
        self.assertEqual(min_coins([1], 100000), 100000)
        coins = [4, 1, 3, 1]
        self.assertEqual(min_coins(coins, 6), 2)
        self.assertEqual(coins, [4, 1, 3, 1])

    def test_small_bfs_reference(self):
        for n in range(4):
            for coins in itertools.product(range(1, 6), repeat=n):
                for amount in range(13):
                    self.assertEqual(min_coins(coins, amount), brute_coins(coins, amount), (coins, amount))

    def test_invalid_even_for_zero_amount(self):
        cases = [([0], 0), ([-1], 0), ([True], 0), ([1.5], 0), ([10**9 + 1], 0),
                 ([1], -1), ([1], 100001), ([1], True), ([1], 1.5),
                 ([1] * 1001, 0), (None, 0)]
        for coins, amount in cases:
            with self.subTest(coins=coins, amount=amount), self.assertRaises(ValueError):
                min_coins(coins, amount)


class MatrixChainTests(unittest.TestCase):
    def test_examples_and_empty(self):
        dimensions = [40, 20, 30, 10, 30]
        self.assertEqual(matrix_chain_cost(dimensions), 26000)
        self.assertEqual(dimensions, [40, 20, 30, 10, 30])
        self.assertEqual(matrix_chain_cost([30, 35, 15, 5, 10, 20, 25]), 15125)
        for dimensions in ([], [10], [10, 20]):
            self.assertEqual(matrix_chain_cost(dimensions), 0)

    def test_small_parenthesization_reference(self):
        for count in range(2, 6):
            for dimensions in itertools.product((1, 2, 3), repeat=count):
                self.assertEqual(matrix_chain_cost(dimensions), brute_matrix_chain(dimensions), dimensions)

    def test_numeric_limit(self):
        self.assertEqual(matrix_chain_cost([100000] * 101), 99 * 10**15)

    def test_invalid_dimensions(self):
        for dimensions in (None, [-1], [0], [10, -1, 20], [10, 0], [100001],
                           [True], [1.5], [1] * 102):
            with self.subTest(dimensions=dimensions), self.assertRaises(ValueError):
                matrix_chain_cost(dimensions)


class NQueensTests(unittest.TestCase):
    def test_known_counts_and_order(self):
        self.assertEqual(n_queens(0), [()])
        self.assertEqual(n_queens(1), [(0,)])
        self.assertEqual(n_queens(2), [])
        self.assertEqual(n_queens(3), [])
        self.assertEqual(n_queens(4), [(1, 3, 0, 2), (2, 0, 3, 1)])
        self.assertEqual(len(n_queens(8)), 92)
        self.assertEqual(len(n_queens(10)), 724)

    def test_small_permutation_reference(self):
        for n in range(8):
            expected = [placement for placement in itertools.permutations(range(n))
                        if len({row - column for row, column in enumerate(placement)}) == n
                        and len({row + column for row, column in enumerate(placement)}) == n]
            self.assertEqual(n_queens(n), expected)

    def test_invalid(self):
        for n in (-1, 11, 2.5, True, None):
            with self.subTest(n=n), self.assertRaises(ValueError):
                n_queens(n)


SUDOKU_PUZZLE = [
    [5,3,0,0,7,0,0,0,0], [6,0,0,1,9,5,0,0,0], [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0], [0,0,0,4,1,9,0,0,5], [0,0,0,0,8,0,0,7,9],
]
SUDOKU_SOLUTION = [
    [5,3,4,6,7,8,9,1,2], [6,7,2,1,9,5,3,4,8], [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3], [4,2,6,8,5,3,7,9,1], [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4], [2,8,7,4,1,9,6,3,5], [3,4,5,2,8,6,1,7,9],
]


class SudokuTests(unittest.TestCase):
    def assert_valid_solution(self, board, givens):
        self.assertIsNotNone(board)
        digits = set(range(1, 10))
        for row in board:
            self.assertEqual(set(row), digits)
        for column in zip(*board):
            self.assertEqual(set(column), digits)
        for row in range(0, 9, 3):
            for column in range(0, 9, 3):
                self.assertEqual({board[r][c] for r in range(row, row + 3)
                                  for c in range(column, column + 3)}, digits)
        for row in range(9):
            for column in range(9):
                if givens[row][column]:
                    self.assertEqual(board[row][column], givens[row][column])

    def test_solution_and_no_mutation(self):
        puzzle = [row[:] for row in SUDOKU_PUZZLE]
        result = solve_sudoku(puzzle)
        self.assertEqual(result, SUDOKU_SOLUTION)
        self.assert_valid_solution(result, puzzle)
        self.assertEqual(puzzle, SUDOKU_PUZZLE)
        self.assertTrue(all(result[row] is not puzzle[row] for row in range(9)))

    def test_filled_board_is_validated_and_copied(self):
        result = solve_sudoku(SUDOKU_SOLUTION)
        self.assertEqual(result, SUDOKU_SOLUTION)
        self.assertIsNot(result, SUDOKU_SOLUTION)
        invalid = [row[:] for row in SUDOKU_SOLUTION]
        invalid[0][0] = invalid[0][1]
        with self.assertRaises(ValueError):
            solve_sudoku(invalid)
        # Rows and columns are permutations, but the 3x3 boxes are invalid.
        latin_square = [[(row + column) % 9 + 1 for column in range(9)] for row in range(9)]
        with self.assertRaises(ValueError):
            solve_sudoku(latin_square)

    def test_empty_board_and_partial_valid_boards(self):
        empty = [[0] * 9 for _ in range(9)]
        self.assert_valid_solution(solve_sudoku(empty), empty)
        for modulus in (2, 3, 5):
            board = [[value if (row * 9 + column) % modulus else 0
                      for column, value in enumerate(values)]
                     for row, values in enumerate(SUDOKU_SOLUTION)]
            self.assert_valid_solution(solve_sudoku(board), board)

    def test_valid_givens_but_no_solution(self):
        impossible = [[0] * 9 for _ in range(9)]
        impossible[0] = [1,2,3,4,5,6,7,8,0]
        impossible[1][8] = 9
        before = [row[:] for row in impossible]
        self.assertIsNone(solve_sudoku(impossible))
        self.assertEqual(impossible, before)

    def test_conflicting_givens(self):
        for second in ((0, 8), (8, 0), (1, 1)):
            board = [[0] * 9 for _ in range(9)]
            board[0][0] = 1
            board[second[0]][second[1]] = 1
            with self.subTest(second=second), self.assertRaises(ValueError):
                solve_sudoku(board)

    def test_invalid_shape_and_cells(self):
        for board in (None, [], [[0] * 9 for _ in range(8)], [[0] * 8 for _ in range(9)],
                      [None] * 9):
            with self.subTest(board=board), self.assertRaises(ValueError):
                solve_sudoku(board)
        for value in (-1, 10, True, 1.5, "1"):
            board = [[0] * 9 for _ in range(9)]
            board[8][8] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                solve_sudoku(board)


class EnumerationTests(unittest.TestCase):
    def test_matches_itertools_including_duplicates(self):
        for items in ([], [1], [1, 1], [3, 1, 2], [2, 1, 2, 1], list(range(6))):
            before = items[:]
            self.assertEqual(enumeration.permutations(items), list(itertools.permutations(items)))
            for k in range(len(items) + 2):
                self.assertEqual(enumeration.combinations(items, k), list(itertools.combinations(items, k)))
            self.assertEqual(items, before)

    def test_limits_and_independent_calls(self):
        self.assertEqual(len(enumeration.permutations(list(range(8)))), 40320)
        self.assertEqual(enumeration.combinations([], 0), [()])
        self.assertEqual(enumeration.combinations([1], 10**20), [])
        result = enumeration.permutations([1, 2])
        result.clear()
        self.assertEqual(enumeration.permutations([1, 2]), [(1, 2), (2, 1)])

    def test_invalid(self):
        for items in (None, "123", [True], [1.5], list(range(9))):
            with self.subTest(items=items):
                with self.assertRaises(ValueError):
                    enumeration.permutations(items)
                with self.assertRaises(ValueError):
                    enumeration.combinations(items, 0)
        for k in (-1, True, 1.5, None):
            with self.subTest(k=k), self.assertRaises(ValueError):
                enumeration.combinations([1, 2], k)


class TravelingSalesmanTests(unittest.TestCase):
    def test_examples_empty_singleton_and_no_tour(self):
        matrix = [[0,10,15,20], [10,0,35,25], [15,35,0,30], [20,25,30,0]]
        before = [row[:] for row in matrix]
        self.assertEqual(traveling_salesman(matrix), (80, (0,1,3,2,0)))
        self.assertEqual(matrix, before)
        self.assertEqual(traveling_salesman([]), (0, ()))
        self.assertEqual(traveling_salesman([[0]]), (0, (0,0)))
        self.assertEqual(traveling_salesman([[0,0], [0,0]]), (0, (0,1,0)))
        self.assertIsNone(traveling_salesman([[0,1], [-1,0]]))
        self.assertIsNone(traveling_salesman([[0,-1], [-1,0]]))
        # Each vertex has incoming/outgoing edges, but there is no global tour.
        self.assertIsNone(traveling_salesman([[0,1,-1,-1], [1,0,-1,-1],
                                             [-1,-1,0,1], [-1,-1,1,0]]))

    def test_directed_zero_edges_and_large_cost(self):
        self.assertEqual(traveling_salesman([[0,0,-1], [-1,0,2], [3,-1,0]]), (5, (0,1,2,0)))
        self.assertEqual(traveling_salesman([[0,10**9,10**9], [10**9,0,10**9],
                                            [10**9,10**9,0]]), (3 * 10**9, (0,1,2,0)))

    def test_all_small_directed_graphs(self):
        positions = [(i, j) for i in range(3) for j in range(3) if i != j]
        for edges in itertools.product((-1, 0, 2), repeat=6):
            matrix = [[0] * 3 for _ in range(3)]
            for (i, j), edge in zip(positions, edges):
                matrix[i][j] = edge
            self.assertEqual(traveling_salesman(matrix), brute_tsp(matrix), matrix)

    def test_seeded_small_bruteforce(self):
        rng = random.Random(20261024)
        for n in range(2, 8):
            for _ in range(20):
                matrix = [[0 if i == j else rng.choice((-1, 0, 1, 2, 7, 20))
                           for j in range(n)] for i in range(n)]
                self.assertEqual(traveling_salesman(matrix), brute_tsp(matrix), matrix)

    def test_equal_cost_graph_is_pruned(self):
        # Observe external matrix accesses: a bound should cut equal-cost
        # subtrees after the first tour, instead of visiting all 7! tours.
        accesses = [0]

        class CountingRow(list):
            def __getitem__(self, index):
                accesses[0] += 1
                return super().__getitem__(index)

        matrix = [CountingRow(0 if i == j else 1 for j in range(8)) for i in range(8)]
        self.assertEqual(traveling_salesman(matrix), (8, tuple(range(8)) + (0,)))
        self.assertLess(accesses[0], 5000)

    def test_invalid(self):
        cases = [None, [[0,1]], [[0], [1,0]], [[0,1], None], [[1]], [[-1]],
                 [[0,-2], [1,0]], [[0,True], [1,0]], [[0,1.5], [1,0]],
                 [[0,float("inf")], [1,0]], [[0,10**9 + 1], [1,0]],
                 [[0] * 13 for _ in range(13)]]
        for matrix in cases:
            with self.subTest(matrix=matrix), self.assertRaises(ValueError):
                traveling_salesman(matrix)


class ConvexHullTests(unittest.TestCase):
    def assert_hull_properties(self, points, hull):
        self.assertEqual(set(hull), supporting_vertices(points))
        self.assertEqual(len(hull), len(set(hull)))
        if hull:
            self.assertEqual(hull[0], min(points))
        if len(hull) >= 3:
            for index, a in enumerate(hull):
                b, c = hull[(index + 1) % len(hull)], hull[(index + 2) % len(hull)]
                self.assertGreater(cross(a, b, c), 0)
                for point in points:
                    self.assertGreaterEqual(cross(a, b, point), 0)

    def test_empty_duplicates_collinear_and_square(self):
        self.assertEqual(convex_hull([]), [])
        self.assertEqual(convex_hull([(1,1), (1,1)]), [(1,1)])
        self.assertEqual(convex_hull([(2,2), (0,0), (1,1)]), [(0,0), (2,2)])
        self.assertEqual(convex_hull([(1,2), (1,-2), (1,0)]), [(1,-2), (1,2)])
        points = [(0,0), (2,0), (2,2), (0,2), (1,1), (0,0), (1,0)]
        self.assertEqual(convex_hull(points), [(0,0), (2,0), (2,2), (0,2)])
        self.assert_hull_properties(points, convex_hull(points))

    def test_all_small_grid_subsets(self):
        grid = list(itertools.product((-1, 0, 1), repeat=2))
        for mask in range(1 << len(grid)):
            points = [point for index, point in enumerate(grid) if mask & (1 << index)]
            hull = convex_hull(points)
            self.assert_hull_properties(points, hull)
            self.assertEqual(convex_hull(list(reversed(points))), hull)

    def test_large_coordinates_and_no_mutation(self):
        limit = 10**9
        points = [[limit, limit], [-limit, -limit], [limit, -limit], [-limit, limit], [0, 0]]
        before = [point[:] for point in points]
        hull = convex_hull(points)
        self.assertEqual(hull, [(-limit,-limit), (limit,-limit), (limit,limit), (-limit,limit)])
        self.assertEqual(points, before)
        self.assert_hull_properties(list(map(tuple, points)), hull)

    def test_invalid(self):
        for points in (None, [(1,)], [(1,2,3)], [None], [(1.0,2)], [(True,2)],
                       [(10**9 + 1,0)], [(0,-10**9 - 1)], [(0,0)] * 100001):
            with self.subTest(kind=type(points).__name__), self.assertRaises(ValueError):
                convex_hull(points)


if __name__ == "__main__":
    unittest.main()
