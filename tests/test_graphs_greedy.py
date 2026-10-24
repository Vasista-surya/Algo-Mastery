"""Stdlib regression tests for all independent Graphs/ and Greedy/ modules.

Run: python -m unittest discover -s tests -p "test_graphs_greedy.py"
The shared _loader.py imports standalone modules. Randomized oracles use fixed seeds.
"""

from fractions import Fraction
from itertools import combinations
from math import inf
import random
import unittest

from _loader import load


BFS = load("Graphs/BFS/BFS.py")
DFS = load("Graphs/DFS/DFS.py")
TOPO = load("Graphs/TopologicalSort/TopologicalSort.py")
DIJKSTRA = load("Graphs/Dijkstra/Dijkstra.py")
KRUSKAL = load("Graphs/Kruskal/Kruskal.py")
PRIM = load("Graphs/Prim/Prim.py")
BELLMAN = load("Graphs/BellmanFord/BellmanFord.py")
FLOYD = load("Graphs/FloydWarshall/FloydWarshall.py")
ACTIVITY = load("Greedy/ActivitySelection/ActivitySelection.py")
KNAPSACK = load("Greedy/FractionalKnapsack/FractionalKnapsack.py")
HUFFMAN = load("Greedy/HuffmanCoding/HuffmanCoding.py")

TRAVERSALS = (BFS.bfs, DFS.dfs)
FORESTS = (KRUSKAL.kruskal, PRIM.prim)
SINGLE_SOURCE = (DIJKSTRA.dijkstra, BELLMAN.bellman_ford)
WEIGHTED_CALLS = (
    lambda n, edges: DIJKSTRA.dijkstra(n, edges, 0),
    lambda n, edges: BELLMAN.bellman_ford(n, edges, 0),
    FLOYD.floyd_warshall,
    KRUSKAL.kruskal,
    PRIM.prim,
)
ALL_CALLS = (
    lambda n, edges: BFS.bfs(n, edges, 0),
    lambda n, edges: DFS.dfs(n, edges, 0),
    TOPO.topological_sort,
) + WEIGHTED_CALLS


class GraphValidationTests(unittest.TestCase):
    def test_invalid_vertex_counts(self):
        for function in ALL_CALLS:
            for n in (-1, True, 2.0, "2", None):
                with self.subTest(function=function, n=n), self.assertRaises(ValueError):
                    function(n, [])

    def test_invalid_sources_including_empty(self):
        for function in TRAVERSALS + SINGLE_SOURCE:
            for n, source in ((0, 0), (2, -1), (2, 2), (2, True), (2, 0.0), (2, None)):
                with self.subTest(function=function, n=n, source=source), self.assertRaises(ValueError):
                    function(n, [], source)

    def test_invalid_unweighted_vertices_even_unreachable(self):
        for function in ALL_CALLS[:3]:
            for edge in ((1, 2), (-1, 1), (1, True), (1.0, 1), (1, "0")):
                with self.subTest(function=function, edge=edge), self.assertRaises(ValueError):
                    function(2, [edge])

    def test_invalid_weighted_vertices_even_unreachable(self):
        for function in WEIGHTED_CALLS:
            for edge in ((1, 2, 1), (-1, 1, 1), (1, True, 1), (1.0, 1, 1), (1, "0", 1)):
                with self.subTest(function=function, edge=edge), self.assertRaises(ValueError):
                    function(2, [edge])

    def test_weight_types_are_integral(self):
        for function in WEIGHTED_CALLS:
            for weight in (True, 1.5, inf, float("nan"), "1", None):
                with self.subTest(function=function, weight=weight), self.assertRaises(ValueError):
                    function(2, [(0, 1, weight)])

    def test_empty_graph_cannot_contain_edges(self):
        for function in (TOPO.topological_sort, FLOYD.floyd_warshall) + FORESTS:
            edge = (0, 0) if function is TOPO.topological_sort else (0, 0, 0)
            with self.subTest(function=function), self.assertRaises(ValueError):
                function(0, [edge])


class TraversalTests(unittest.TestCase):
    def setUp(self):
        self.edges = [(0, 2), (0, 1), (2, 3), (1, 4), (4, 0), (0, 2)]

    def test_bfs_layer_order(self):
        self.assertEqual(BFS.bfs(6, self.edges, 0), [0, 2, 1, 3, 4])

    def test_dfs_preorder(self):
        self.assertEqual(DFS.dfs(6, self.edges, 0), [0, 2, 3, 1, 4])

    def test_directed_and_undirected(self):
        edges = [(0, 1), (1, 2)]
        for function in TRAVERSALS:
            with self.subTest(function=function):
                self.assertEqual(function(3, edges, 2), [2])
                self.assertEqual(function(3, edges + [(1, 0), (2, 1)], 2), [2, 1, 0])

    def test_loops_parallel_arcs_and_cycles(self):
        for function in TRAVERSALS:
            with self.subTest(function=function):
                self.assertEqual(function(3, [(0, 0), (0, 1), (0, 1), (1, 0)], 0), [0, 1])

    def test_disconnected_and_isolated(self):
        for function in TRAVERSALS:
            with self.subTest(function=function):
                self.assertEqual(function(4, [(0, 1), (2, 3)], 2), [2, 3])
                self.assertEqual(function(4, [], 3), [3])
                self.assertEqual(function(1, [], 0), [0])

    def test_long_chain_has_no_recursion_dependency(self):
        edges = [(v, v + 1) for v in range(2999)]
        for function in TRAVERSALS:
            with self.subTest(function=function):
                self.assertEqual(function(3000, edges, 0), list(range(3000)))

    def test_generator_and_no_mutation(self):
        before = self.edges.copy()
        for function in TRAVERSALS:
            with self.subTest(function=function):
                self.assertEqual(function(6, iter(self.edges), 0), function(6, self.edges, 0))
                self.assertEqual(self.edges, before)


class TopologicalTests(unittest.TestCase):
    def test_normal_disconnected_and_ties(self):
        edges = [(0, 2), (1, 2), (2, 3)]
        order = TOPO.topological_sort(5, edges)
        self.assertEqual(order, [0, 1, 4, 2, 3])
        position = {v: i for i, v in enumerate(order)}
        self.assertTrue(all(position[u] < position[v] for u, v in edges))

    def test_empty_and_edgeless(self):
        self.assertEqual(TOPO.topological_sort(0, []), [])
        self.assertEqual(TOPO.topological_sort(4, []), [0, 1, 2, 3])

    def test_parallel_arcs(self):
        self.assertEqual(TOPO.topological_sort(2, [(0, 1), (0, 1)]), [0, 1])

    def test_cycles_anywhere(self):
        for n, edges in ((1, [(0, 0)]), (2, [(0, 1), (1, 0)]),
                         (5, [(0, 1), (3, 4), (4, 3)])):
            with self.subTest(n=n, edges=edges), self.assertRaisesRegex(ValueError, "cycle"):
                TOPO.topological_sort(n, edges)

    def test_generator_and_no_mutation(self):
        edges = [(2, 0), (2, 1)]
        before = edges.copy()
        self.assertEqual(TOPO.topological_sort(3, iter(edges)), [2, 0, 1])
        self.assertEqual(TOPO.topological_sort(3, edges), [2, 0, 1])
        self.assertEqual(edges, before)


class ShortestPathTests(unittest.TestCase):
    def test_dijkstra_normal_and_unreachable(self):
        self.assertEqual(DIJKSTRA.dijkstra(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0),
                         [0, 3, 1, inf])

    def test_zero_weights_parallel_edges_and_loops(self):
        edges = [(0, 0, 0), (0, 1, 10), (0, 1, 0), (1, 2, 0), (0, 2, 4)]
        for function in SINGLE_SOURCE:
            with self.subTest(function=function):
                self.assertEqual(function(3, edges, 0), [0, 0, 0])
        self.assertEqual(FLOYD.floyd_warshall(3, edges)[0], [0, 0, 0])

    def test_dijkstra_rejects_negative_edges_anywhere(self):
        for edges in ([(0, 1, -1)], [(1, 1, -1)]):
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                DIJKSTRA.dijkstra(2, edges, 0)

    def test_bellman_negative_weights_without_cycle(self):
        self.assertEqual(BELLMAN.bellman_ford(4, [(0, 1, 4), (1, 2, -6)], 0),
                         [0, 4, -2, inf])
        self.assertEqual(BELLMAN.bellman_ford(2, [(0, 1, -2), (1, 0, 3)], 0), [0, -2])

    def test_bellman_reachable_negative_cycles(self):
        for n, edges in ((1, [(0, 0, -1)]),
                         (3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)])):
            with self.subTest(edges=edges), self.assertRaisesRegex(ValueError, "negative cycle"):
                BELLMAN.bellman_ford(n, edges, 0)

    def test_bellman_ignores_unreachable_negative_cycle(self):
        self.assertEqual(BELLMAN.bellman_ford(4, [(0, 1, 7), (2, 3, -2), (3, 2, 1)], 0),
                         [0, 7, inf, inf])

    def test_floyd_normal_negative_edge_disconnected(self):
        self.assertEqual(FLOYD.floyd_warshall(4, [(0, 1, 4), (1, 2, -6)]),
                         [[0, 4, -2, inf], [inf, 0, -6, inf],
                          [inf, inf, 0, inf], [inf, inf, inf, 0]])

    def test_floyd_rejects_negative_cycles_anywhere(self):
        for edges in ([(3, 3, -1)], [(2, 3, -2), (3, 2, 1)],
                      [(0, 1, -1), (1, 0, -1)]):
            with self.subTest(edges=edges), self.assertRaisesRegex(ValueError, "negative cycle"):
                FLOYD.floyd_warshall(4, edges)

    def test_floyd_empty_and_positive_self_loop(self):
        self.assertEqual(FLOYD.floyd_warshall(0, []), [])
        self.assertEqual(FLOYD.floyd_warshall(1, [(0, 0, 4)]), [[0]])

    def test_singleton_and_edgeless_sources(self):
        for function in SINGLE_SOURCE:
            with self.subTest(function=function):
                self.assertEqual(function(1, [], 0), [0])
                self.assertEqual(function(3, [], 1), [inf, 0, inf])

    def test_large_integer_distances_do_not_become_float(self):
        huge = 10 ** 400
        edges = [(0, 1, huge), (1, 2, huge)]
        for function in SINGLE_SOURCE:
            with self.subTest(function=function):
                self.assertEqual(function(4, edges, 0), [0, huge, 2 * huge, inf])
        self.assertEqual(FLOYD.floyd_warshall(4, edges)[0], [0, huge, 2 * huge, inf])
        negative = [(0, 1, -huge), (1, 2, -huge)]
        self.assertEqual(BELLMAN.bellman_ford(3, negative, 0), [0, -huge, -2 * huge])
        self.assertEqual(FLOYD.floyd_warshall(3, negative)[0], [0, -huge, -2 * huge])

    def test_generators_and_no_mutation(self):
        edges = [(0, 1, 4), (1, 2, 2)]
        before = edges.copy()
        for function in SINGLE_SOURCE:
            self.assertEqual(function(3, iter(edges), 0), function(3, edges, 0))
        self.assertEqual(FLOYD.floyd_warshall(3, iter(edges)), FLOYD.floyd_warshall(3, edges))
        self.assertEqual(edges, before)

    def test_seeded_nonnegative_cross_check(self):
        rng = random.Random(7241)
        for _ in range(20):
            n = rng.randrange(1, 7)
            edges = [(u, v, rng.randrange(10)) for u in range(n) for v in range(n)
                     if rng.random() < 0.25]
            all_pairs = FLOYD.floyd_warshall(n, edges)
            for source in range(n):
                with self.subTest(n=n, edges=edges, source=source):
                    self.assertEqual(DIJKSTRA.dijkstra(n, edges, source), all_pairs[source])
                    self.assertEqual(BELLMAN.bellman_ford(n, edges, source), all_pairs[source])


def _components(n, edges):
    """Independent connectivity oracle based on explicit vertex sets."""
    groups = [{v} for v in range(n)]
    for u, v, _ in edges:
        left = next(group for group in groups if u in group)
        right = next(group for group in groups if v in group)
        if left is not right:
            left.update(right)
            groups.remove(right)
    return groups


def _brute_forest_total(n, edges):
    groups = {frozenset(group) for group in _components(n, edges)}
    needed = n - len(groups)
    return min(sum(weight for _, _, weight in selected)
               for selected in combinations(edges, needed)
               if {frozenset(group) for group in _components(n, selected)} == groups)


class ForestTests(unittest.TestCase):
    def assert_forest(self, function, n, edges, expected):
        forest, total = function(n, edges)
        self.assertEqual(total, expected)
        self.assertEqual(total, sum(weight for _, _, weight in forest))
        original = {(min(u, v), max(u, v), weight) for u, v, weight in edges}
        self.assertTrue(all(edge in original for edge in forest))
        self.assertTrue(all(u < v for u, v, _ in forest))
        target_components = {frozenset(group) for group in _components(n, edges)}
        self.assertEqual({frozenset(group) for group in _components(n, forest)}, target_components)
        self.assertEqual(len(forest), n - len(target_components))

    def test_connected_totals(self):
        edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
        for function in FORESTS:
            with self.subTest(function=function):
                self.assert_forest(function, 4, edges, 19)

    def test_disconnected_forests_with_isolate(self):
        edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (3, 4, -1)]
        for function in FORESTS:
            with self.subTest(function=function):
                self.assert_forest(function, 6, edges, 2)

    def test_empty_and_edgeless(self):
        for function in FORESTS:
            for n in (0, 1, 4):
                with self.subTest(function=function, n=n):
                    self.assertEqual(function(n, []), ([], 0))

    def test_negative_weights_loops_parallel_and_reversed_edges(self):
        edges = [(0, 0, -100), (1, 0, 5), (0, 1, -2), (2, 1, -3), (0, 2, 9)]
        for function in FORESTS:
            with self.subTest(function=function):
                self.assert_forest(function, 3, edges, -5)

    def test_large_integer_total(self):
        huge = 10 ** 400
        edges = [(0, 1, huge), (1, 2, huge), (2, 3, -3 * huge)]
        for function in FORESTS:
            with self.subTest(function=function):
                self.assert_forest(function, 4, edges, -huge)

    def test_determinism_generators_and_no_mutation(self):
        edges = [(1, 2, 1), (0, 2, 1), (0, 1, 1), (0, 1, 1)]
        before = edges.copy()
        for function in FORESTS:
            with self.subTest(function=function):
                result = function(3, edges)
                self.assertEqual(function(3, iter(edges)), result)
                self.assertEqual(function(3, list(reversed(edges))), result)
                self.assertEqual(edges, before)

    def test_seeded_exhaustive_optimality(self):
        rng = random.Random(9123)
        for _ in range(25):
            n = rng.randrange(1, 6)
            edges = [(u, v, rng.randrange(-5, 8)) for u, v in combinations(range(n), 2)
                     if rng.random() < 0.55]
            expected = _brute_forest_total(n, edges)
            for function in FORESTS:
                with self.subTest(function=function, n=n, edges=edges):
                    self.assert_forest(function, n, edges, expected)


class ActivityTests(unittest.TestCase):
    def test_normal_unsorted_input(self):
        activities = [(5, 9), (1, 2), (3, 4), (0, 6), (5, 7), (8, 9)]
        self.assertEqual(ACTIVITY.activity_selection(activities), [1, 2, 4, 5])

    def test_empty_negative_times_touching_and_ties(self):
        self.assertEqual(ACTIVITY.activity_selection([]), [])
        self.assertEqual(ACTIVITY.activity_selection([(-4, -2), (-2, 0), (1, 3)]), [0, 1, 2])
        self.assertEqual(ACTIVITY.activity_selection([(1, 3), (0, 3), (0, 3), (3, 4)]), [1, 3])

    def test_invalid_intervals(self):
        for activities in ([(2, 2)], [(3, 2)], [(0.0, 2)], [(False, 2)], [(0, "2")]):
            with self.subTest(activities=activities), self.assertRaises(ValueError):
                ACTIVITY.activity_selection(activities)

    def test_huge_times_generators_and_no_mutation(self):
        huge = 10 ** 400
        activities = [(-huge, 0), (0, huge)]
        before = activities.copy()
        self.assertEqual(ACTIVITY.activity_selection(iter(activities)), [0, 1])
        self.assertEqual(ACTIVITY.activity_selection(activities), [0, 1])
        self.assertEqual(activities, before)

    def test_seeded_exhaustive_maximum_cardinality(self):
        rng = random.Random(2187)
        for _ in range(25):
            activities = []
            for _ in range(7):
                start = rng.randrange(-4, 8)
                activities.append((start, start + rng.randrange(1, 6)))
            best = 0
            for mask in range(1 << len(activities)):
                subset = [activities[i] for i in range(len(activities)) if mask & (1 << i)]
                if all(a[1] <= b[0] or b[1] <= a[0] for a, b in combinations(subset, 2)):
                    best = max(best, len(subset))
            selected = ACTIVITY.activity_selection(activities)
            with self.subTest(activities=activities):
                self.assertEqual(len(selected), best)
                self.assertEqual(len(selected), len(set(selected)))
                self.assertTrue(all(activities[a][1] <= activities[b][0]
                                    for a, b in zip(selected, selected[1:])))


class KnapsackTests(unittest.TestCase):
    def test_normal_exact_value_and_shares(self):
        self.assertEqual(KNAPSACK.fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50),
                         (240, [1, 1, Fraction(2, 3)]))
        self.assertEqual(KNAPSACK.fractional_knapsack([(8, 3)], 1),
                         (Fraction(8, 3), [Fraction(1, 3)]))

    def test_empty_zero_capacity_and_zero_value(self):
        self.assertEqual(KNAPSACK.fractional_knapsack([], 5), (0, []))
        self.assertEqual(KNAPSACK.fractional_knapsack([(10, 1)], 0), (0, [0]))
        self.assertEqual(KNAPSACK.fractional_knapsack([(0, 1), (4, 2)], 5), (4, [0, 1]))

    def test_ratio_ties_and_original_indices(self):
        self.assertEqual(KNAPSACK.fractional_knapsack([(2, 2), (9, 3), (4, 4)], 4),
                         (10, [Fraction(1, 2), 1, 0]))
        self.assertEqual(KNAPSACK.fractional_knapsack([(2, 2), (4, 4)], 1),
                         (1, [Fraction(1, 2), 0]))

    def test_invalid_domains_even_zero_capacity(self):
        for capacity in (-1, True, 1.0, inf, None):
            with self.subTest(capacity=capacity), self.assertRaises(ValueError):
                KNAPSACK.fractional_knapsack([], capacity)
        for item in ((1, 0), (1, -1), (-1, 2), (True, 2), (1, False), (1.5, 2), (1, inf)):
            with self.subTest(item=item), self.assertRaises(ValueError):
                KNAPSACK.fractional_knapsack([item], 0)

    def test_huge_values_generators_and_no_mutation(self):
        huge = 10 ** 400
        items = [(huge + 1, huge), (huge, huge)]
        before = items.copy()
        expected = (huge + 1, [1, 0])
        self.assertEqual(KNAPSACK.fractional_knapsack(iter(items), huge), expected)
        self.assertEqual(KNAPSACK.fractional_knapsack(items, huge), expected)
        self.assertEqual(items, before)

    def test_seeded_exhaustive_extreme_point_optimality(self):
        rng = random.Random(4512)
        for _ in range(20):
            items = [(rng.randrange(12), rng.randrange(1, 8)) for _ in range(5)]
            capacity = rng.randrange(20)
            best = Fraction(0)
            # An extreme point has full/empty items and at most one fractional item.
            for mask in range(1 << len(items)):
                full = [i for i in range(len(items)) if mask & (1 << i)]
                weight = sum(items[i][1] for i in full)
                if weight > capacity:
                    continue
                value = sum(items[i][0] for i in full)
                best = max(best, value)
                for i, (item_value, item_weight) in enumerate(items):
                    if i not in full:
                        share = min(Fraction(1), Fraction(capacity - weight, item_weight))
                        best = max(best, value + item_value * share)
            total, shares = KNAPSACK.fractional_knapsack(items, capacity)
            with self.subTest(items=items, capacity=capacity):
                self.assertEqual(total, best)
                self.assertTrue(all(0 <= share <= 1 for share in shares))
                self.assertLessEqual(sum(weight * share for (_, weight), share in zip(items, shares)), capacity)
                self.assertEqual(sum(value * share for (value, _), share in zip(items, shares)), total)


class HuffmanTests(unittest.TestCase):
    def assert_prefix_free(self, codes):
        words = list(codes.values())
        self.assertEqual(len(words), len(set(words)))
        self.assertTrue(all(word and set(word) <= {"0", "1"} for word in words))
        self.assertTrue(all(not b.startswith(a) and not a.startswith(b)
                            for a, b in combinations(words, 2)))

    def test_normal_codes_prefix_free_and_roundtrip(self):
        frequencies = {"a": 5, "b": 2, "c": 1}
        codes = HUFFMAN.huffman_codes(frequencies)
        self.assertEqual(codes, {"a": "1", "b": "01", "c": "00"})
        self.assert_prefix_free(codes)
        self.assertEqual(HUFFMAN.decode(HUFFMAN.encode("abaca", codes), codes), "abaca")

    def test_empty_alphabet(self):
        self.assertEqual(HUFFMAN.huffman_codes({}), {})
        self.assertEqual(HUFFMAN.encode("", {}), "")
        self.assertEqual(HUFFMAN.decode("", {}), "")
        with self.assertRaises(ValueError):
            HUFFMAN.encode("x", {})
        with self.assertRaises(ValueError):
            HUFFMAN.decode("0", {})

    def test_single_symbol_preserves_repetitions(self):
        codes = HUFFMAN.huffman_codes({"x": 7})
        self.assertEqual(codes, {"x": "0"})
        self.assertEqual(HUFFMAN.encode("xxxxx", codes), "00000")
        self.assertEqual(HUFFMAN.decode("00000", codes), "xxxxx")
        self.assertEqual(HUFFMAN.decode("", codes), "")
        with self.assertRaises(ValueError):
            HUFFMAN.decode("1", codes)

    def test_ties_are_insertion_order_independent(self):
        frequencies = {"d": 1, "b": 1, "a": 1, "c": 1}
        expected = {"a": "00", "b": "01", "c": "10", "d": "11"}
        self.assertEqual(HUFFMAN.huffman_codes(frequencies), expected)
        self.assertEqual(HUFFMAN.huffman_codes(dict(reversed(list(frequencies.items())))), expected)
        self.assertEqual(HUFFMAN.huffman_codes({"a": 1, "b": 1, "c": 2}),
                         {"a": "00", "b": "01", "c": "1"})

    def test_unicode_and_nul_symbols(self):
        text = "\x00é🙂é\x00"
        frequencies = {symbol: text.count(symbol) for symbol in set(text)}
        codes = HUFFMAN.huffman_codes(frequencies)
        self.assert_prefix_free(codes)
        self.assertEqual(HUFFMAN.decode(HUFFMAN.encode(text, codes), codes), text)

    def test_invalid_frequencies_and_symbols(self):
        for frequencies in ({"a": 0}, {"a": -1}, {"a": True}, {"a": 1.0},
                            {"a": inf}, {"a": None}, {"": 1}, {"ab": 1}, {1: 1}):
            with self.subTest(frequencies=frequencies), self.assertRaises(ValueError):
                HUFFMAN.huffman_codes(frequencies)

    def test_malformed_external_codebooks(self):
        codebooks = [
            {"a": ""}, {"a": "2"}, {"a": 0}, {"": "0"}, {"ab": "0"},
            {"a": "0", "b": "0"}, {"a": "0", "b": "01"},
            {"b": "01", "a": "0"}, {"a": "00", "b": "001"},
        ]
        for codes in codebooks:
            for function in (HUFFMAN.encode, HUFFMAN.decode):
                with self.subTest(codes=codes, function=function), self.assertRaises(ValueError):
                    function("", codes)

    def test_invalid_unknown_and_truncated_streams(self):
        codes = {"a": "0", "b": "10", "c": "11"}
        for bits in ("1", "01", "2", "10x", " 0"):
            with self.subTest(bits=bits), self.assertRaises(ValueError):
                HUFFMAN.decode(bits, codes)
        with self.assertRaises(ValueError):
            HUFFMAN.decode("11", {"a": "00", "b": "01"})
        with self.assertRaises(ValueError):
            HUFFMAN.encode("z", codes)
        for function in (HUFFMAN.encode, HUFFMAN.decode):
            with self.subTest(function=function), self.assertRaises(ValueError):
                function(None, codes)

    def test_known_optimal_weighted_length(self):
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        codes = HUFFMAN.huffman_codes(frequencies)
        self.assert_prefix_free(codes)
        self.assertEqual(sum(frequencies[symbol] * len(code) for symbol, code in codes.items()), 224)

    def test_huge_frequencies_and_no_mutation(self):
        frequencies = {"a": 10 ** 400, "b": 10 ** 400, "c": 1}
        before = frequencies.copy()
        codes = HUFFMAN.huffman_codes(frequencies)
        snapshot = codes.copy()
        self.assert_prefix_free(codes)
        self.assertEqual(HUFFMAN.decode(HUFFMAN.encode("cab", codes), codes), "cab")
        self.assertEqual(frequencies, before)
        self.assertEqual(codes, snapshot)

    def test_skewed_tree_and_seeded_roundtrips(self):
        frequencies = {chr(i): 1 << i for i in range(80)}
        codes = HUFFMAN.huffman_codes(frequencies)
        self.assert_prefix_free(codes)
        self.assertGreater(max(map(len, codes.values())), 50)
        rng = random.Random(8719)
        for alphabet_size in range(1, 15):
            alphabet = [chr(65 + i) for i in range(alphabet_size)]
            frequencies = {symbol: rng.randrange(1, 100) for symbol in alphabet}
            codes = HUFFMAN.huffman_codes(frequencies)
            text = "".join(rng.choice(alphabet) for _ in range(100))
            with self.subTest(alphabet_size=alphabet_size):
                self.assert_prefix_free(codes)
                self.assertEqual(HUFFMAN.decode(HUFFMAN.encode(text, codes), codes), text)


if __name__ == "__main__":
    unittest.main()
