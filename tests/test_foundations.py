"""Regression tests for the standalone Arrays, Strings, and LinkedList modules.

Run from the repository root: python -m unittest discover -s tests
The shared _loader imports modules by repository-relative path.
Only the standard library is used; randomized cases have fixed seeds.
"""

import random
import unittest

from _loader import load


KADANE = load("Arrays/Kadane/Kadane.py")
PREFIX = load("Arrays/PrefixSum/PrefixSum.py")
WINDOW = load("Arrays/SlidingWindow/SlidingWindow.py")
TWO_SUM = load("Arrays/TwoPointers/TwoPointers.py")
MATCHERS = {
    name: load("Strings/{0}/{0}.py".format(name))
    for name in ("NaivePatternMatching", "KMP", "RabinKarp", "ZAlgorithm")
}
REVERSE = load("LinkedList/ReverseLinkedList/ReverseLinkedList.py")
CYCLE = load("LinkedList/CycleDetection/CycleDetection.py")
MERGE = load("LinkedList/MergeSortedLists/MergeSortedLists.py")


class ArrayTests(unittest.TestCase):
    def test_kadane_boundaries(self):
        cases = [
            ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
            ([-8, -2, -5], -2), ([0], 0), ([-7], -7),
            ([1, 2, 3], 6), ([3, -100, 4], 4),
            ([10**100, 10**100, -1], 2 * 10**100),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                before = values.copy()
                self.assertEqual(KADANE.max_subarray(values), expected)
                self.assertEqual(values, before)
        self.assertEqual(KADANE.max_subarray((1, -2, 3)), 3)

    def test_kadane_invalid(self):
        for values in ([], ()):
            with self.subTest(values=values), self.assertRaises(ValueError):
                KADANE.max_subarray(values)
        for values in ([True], [1.5], ["1"], [None]):
            with self.subTest(values=values), self.assertRaises(TypeError):
                KADANE.max_subarray(values)

    def test_kadane_randomized(self):
        rng = random.Random(1101)
        for _ in range(200):
            values = [rng.randint(-20, 20) for _ in range(rng.randint(1, 18))]
            expected = max(sum(values[start:end])
                           for start in range(len(values))
                           for end in range(start + 1, len(values) + 1))
            with self.subTest(values=values):
                self.assertEqual(KADANE.max_subarray(values), expected)

    def test_prefix_boundaries(self):
        values = [2, -1, 3, 5]
        prefix = PREFIX.prefix_sums(values)
        self.assertEqual(prefix, [0, 2, 1, 4, 9])
        self.assertEqual(values, [2, -1, 3, 5])
        self.assertEqual(PREFIX.range_sum(prefix, 1, 3), 2)
        self.assertEqual(PREFIX.range_sum(prefix, 0, 4), 9)
        self.assertEqual(PREFIX.range_sum(prefix, 0, 0), 0)
        self.assertEqual(PREFIX.range_sum(prefix, 4, 4), 0)
        self.assertEqual(prefix, [0, 2, 1, 4, 9])
        self.assertEqual(PREFIX.prefix_sums([]), [0])
        self.assertEqual(PREFIX.range_sum([0], 0, 0), 0)
        self.assertEqual(PREFIX.prefix_sums((10**100, -2 * 10**100)),
                         [0, 10**100, -10**100])
        self.assertEqual(PREFIX.range_sum([0, 10**100, -10**100], 1, 2),
                         -2 * 10**100)

    def test_prefix_invalid(self):
        for value in (True, 1.5, "1", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                PREFIX.prefix_sums([value])
        for prefix in ([], [1], [False]):
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                PREFIX.range_sum(prefix, 0, 0)
        for start, end in ((-1, 1), (2, 1), (0, 4), (3, 4), (4, 4), (0, -1)):
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                PREFIX.range_sum([0, 1, 3, 6], start, end)
        for start, end in ((True, 1), (0, False), (0.0, 1), (0, "1"), (None, 1)):
            with self.subTest(start=start, end=end), self.assertRaises(TypeError):
                PREFIX.range_sum([0, 1], start, end)
        for prefix in ([0, "bad"], [0, True], [0, 1.5]):
            with self.subTest(prefix=prefix), self.assertRaises(TypeError):
                PREFIX.range_sum(prefix, 0, 1)

    def test_prefix_randomized(self):
        rng = random.Random(1102)
        for _ in range(100):
            values = [rng.randint(-30, 30) for _ in range(rng.randint(0, 16))]
            prefix = PREFIX.prefix_sums(values)
            self.assertEqual(prefix, [sum(values[:i]) for i in range(len(values) + 1)])
            for start in range(len(values) + 1):
                for end in range(start, len(values) + 1):
                    with self.subTest(values=values, start=start, end=end):
                        self.assertEqual(PREFIX.range_sum(prefix, start, end),
                                         sum(values[start:end]))

    def test_window_boundaries(self):
        cases = [
            ([2, -1, 3, 5, -2], 2, 8), ([-5, -2, -8], 2, -7),
            ([2, -1, 3, 5, -2], 5, 7), ([-4], 1, -4),
            ([5, -10, 1], 1, 5), ([1, -10, 5], 1, 5),
            ([10**100, 10**100], 2, 2 * 10**100),
        ]
        for values, width, expected in cases:
            with self.subTest(values=values, width=width):
                before = values.copy()
                self.assertEqual(WINDOW.max_window_sum(values, width), expected)
                self.assertEqual(values, before)
        self.assertEqual(WINDOW.max_window_sum((1, 2), 2), 3)

    def test_window_invalid(self):
        for values, width in (([], 0), ([], 1), ([1], 0), ([1], -1), ([1], 2)):
            with self.subTest(values=values, width=width), self.assertRaises(ValueError):
                WINDOW.max_window_sum(values, width)
        for width in (True, False, 1.0, "1", None):
            with self.subTest(width=width), self.assertRaises(TypeError):
                WINDOW.max_window_sum([1], width)
        for value in (True, 1.5, "1", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                WINDOW.max_window_sum([value], 1)

    def test_window_randomized(self):
        rng = random.Random(1103)
        for _ in range(150):
            values = [rng.randint(-30, 30) for _ in range(rng.randint(1, 18))]
            for width in range(1, len(values) + 1):
                expected = max(sum(values[i:i + width])
                               for i in range(len(values) - width + 1))
                with self.subTest(values=values, width=width):
                    self.assertEqual(WINDOW.max_window_sum(values, width), expected)

    def test_two_sum_boundaries(self):
        cases = [
            ([], 0, None), ([2], 4, None), ([2, 2], 4, (0, 1)),
            ([-4, -1, 0, 3, 5], 2, (1, 3)),
            ([1, 2, 3, 4], 5, (0, 3)), ([1, 1, 1], 2, (0, 2)),
            ([-4, -2, 0], -6, (0, 1)), ([1, 2, 3], 100, None),
            ([10**100, 10**100], 2 * 10**100, (0, 1)),
        ]
        for values, target, expected in cases:
            with self.subTest(values=values, target=target):
                before = values.copy()
                self.assertEqual(TWO_SUM.two_sum_sorted(values, target), expected)
                self.assertEqual(values, before)
        self.assertEqual(TWO_SUM.two_sum_sorted((1, 2), 3), (0, 1))

    def test_two_sum_invalid(self):
        for values in ([2, 1], [0, 2, 1], [3, 1, 2]):
            before = values.copy()
            with self.subTest(values=values), self.assertRaises(ValueError):
                TWO_SUM.two_sum_sorted(values, 3)
            self.assertEqual(values, before)
        for target in (True, 3.0, "3", None):
            with self.subTest(target=target), self.assertRaises(TypeError):
                TWO_SUM.two_sum_sorted([1, 2], target)
        for value in (True, 1.5, "1", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                TWO_SUM.two_sum_sorted([value], 1)

    def test_two_sum_randomized(self):
        rng = random.Random(1104)
        for _ in range(300):
            values = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 20)))
            target = rng.randint(-45, 45)
            pairs = {(i, j) for i in range(len(values)) for j in range(i + 1, len(values))
                     if values[i] + values[j] == target}
            result = TWO_SUM.two_sum_sorted(values, target)
            with self.subTest(values=values, target=target):
                if pairs:
                    self.assertIn(result, pairs)
                else:
                    self.assertIsNone(result)


class StringTests(unittest.TestCase):
    def test_examples_and_boundaries(self):
        cases = [
            ("", "", [0]), ("", "a", []), ("ab", "", [0, 1, 2]),
            ("aaaa", "aa", [0, 1, 2]), ("aaa", "a", [0, 1, 2]),
            ("abc", "abc", [0]), ("abc", "abcd", []), ("abc", "x", []),
            ("abc", "c", [2]), ("abababa", "aba", [0, 2, 4]),
            ("abababacaba", "ababaca", [2]), ("ABCabc", "abc", [3]),
            ("$a$a$", "$a$", [0, 2]), ("\0\0\0", "\0\0", [0, 1]),
            ("a\0a\0", "a\0", [0, 2]),
            ("\U0001f600a\U0001f600a", "\U0001f600a", [0, 2]),
            ("\U0001f600a", "a", [1]),
            ("\U0001f600", "", [0, 1]), ("\u00e9\u00e9", "\u00e9", [0, 1]),
            ("\ud800x\ud800", "\ud800", [0, 2]),
        ]
        for name, module in MATCHERS.items():
            for text, pattern, expected in cases:
                with self.subTest(algorithm=name, text=text, pattern=pattern):
                    self.assertEqual(module.find_matches(text, pattern), expected)

    def test_invalid_types(self):
        for name, module in MATCHERS.items():
            for invalid in (None, 1, True, b"a", ["a"]):
                with self.subTest(algorithm=name, invalid=invalid):
                    with self.assertRaises(TypeError):
                        module.find_matches(invalid, "a")
                    with self.assertRaises(TypeError):
                        module.find_matches("a", invalid)

    def test_repeated_borders(self):
        text, pattern = "ab" * 100, "ababab"
        for name, module in MATCHERS.items():
            with self.subTest(algorithm=name):
                self.assertEqual(module.find_matches(text, pattern), list(range(0, 195, 2)))
                self.assertEqual(module.find_matches("a" * 200 + "b", "a" * 20 + "b"), [180])

    def test_rabin_karp_collision_verification(self):
        # Base-257 hashes agree, but literal strings do not.
        self.assertEqual(0 * 257 + 257, 1 * 257 + 0)
        self.assertEqual(MATCHERS["RabinKarp"].find_matches("\0\u0101", "\1\0"), [])
        # A byte-domain collision as well: 58*257^3 + 234*257^2 + 70*257 + 157 = modulus.
        text = "".join(map(chr, (58, 234, 70, 157)))
        self.assertEqual(MATCHERS["RabinKarp"].find_matches(text, "\0" * 4), [])
        self.assertEqual(MATCHERS["RabinKarp"].find_matches(text + "\0" * 4, "\0" * 4), [4])

    def test_seeded_randomized(self):
        rng = random.Random(2201)
        alphabet = "aab$#\0\u00e9\U0001f600"
        for case in range(400):
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            if case % 3 == 0:
                start = rng.randint(0, len(text))
                pattern = text[start:rng.randint(start, len(text))]
            else:
                pattern = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 15)))
            expected = [i for i in range(len(text) + 1) if text.startswith(pattern, i)]
            for name, module in MATCHERS.items():
                with self.subTest(algorithm=name, text=text, pattern=pattern):
                    self.assertEqual(module.find_matches(text, pattern), expected)


class LinkedListTests(unittest.TestCase):
    @staticmethod
    def build_nodes(module, values):
        nodes = [module.Node(value) for value in values]
        for first, second in zip(nodes, nodes[1:]):
            first.next = second
        return nodes

    def collect_nodes(self, head, limit):
        """Bound traversal so a regression creating a cycle fails rather than hangs."""
        result, seen = [], set()
        while head is not None:
            self.assertNotIn(id(head), seen, "unexpected cycle in result")
            self.assertLess(len(result), limit, "unexpected extra result node")
            seen.add(id(head))
            result.append(head)
            head = head.next
        return result

    def test_node_constructors(self):
        for module in (REVERSE, CYCLE, MERGE):
            with self.subTest(module=module.__name__):
                tail = module.Node(-10**100)
                head = module.Node(10**100, tail)
                self.assertEqual(head.value, 10**100)
                self.assertIs(head.next, tail)
                self.assertEqual(tail.value, -10**100)
                self.assertIsNone(tail.next)
                for value in (True, 1.5, "1", None):
                    with self.assertRaises(TypeError):
                        module.Node(value)
                for next_node in (0, [], object()):
                    with self.assertRaises(TypeError):
                        module.Node(1, next_node)

    def test_reverse_boundaries_and_identity(self):
        for values in ([], [1], [1, 2], [1, 1, 1], [-10**100, 0, 10**100]):
            nodes = self.build_nodes(REVERSE, values)
            head = nodes[0] if nodes else None
            with self.subTest(values=values):
                result = REVERSE.reverse_list(head)
                reversed_nodes = self.collect_nodes(result, len(nodes))
                self.assertEqual(reversed_nodes, nodes[::-1])
                self.assertEqual([node.value for node in reversed_nodes], values[::-1])
                restored = REVERSE.reverse_list(result)
                self.assertIs(restored, head)
                self.assertEqual(self.collect_nodes(restored, len(nodes)), nodes)

    def test_reverse_rejects_cycles_before_mutation(self):
        for length in (1, 2, 5):
            for entry in range(length):
                nodes = self.build_nodes(REVERSE, range(length))
                nodes[-1].next = nodes[entry]
                links = [node.next for node in nodes]
                with self.subTest(length=length, entry=entry), self.assertRaises(ValueError):
                    REVERSE.reverse_list(nodes[0])
                self.assertEqual([node.next for node in nodes], links)
                nodes[-1].next = None

    def test_reverse_randomized(self):
        rng = random.Random(3301)
        for _ in range(120):
            values = [rng.randint(-10, 10) for _ in range(rng.randint(0, 50))]
            nodes = self.build_nodes(REVERSE, values)
            result = REVERSE.reverse_list(nodes[0] if nodes else None)
            actual = self.collect_nodes(result, len(nodes))
            self.assertEqual(actual, nodes[::-1])
            self.assertEqual([node.value for node in actual], values[::-1])

    def test_cycle_boundaries_and_no_mutation(self):
        self.assertFalse(CYCLE.has_cycle(None))
        for length in (1, 2, 3, 6):
            for entry in range(-1, length):
                # Equal values make an identity-based check important.
                nodes = self.build_nodes(CYCLE, [7] * length)
                if entry >= 0:
                    nodes[-1].next = nodes[entry]
                links = [node.next for node in nodes]
                with self.subTest(length=length, entry=entry):
                    self.assertEqual(CYCLE.has_cycle(nodes[0]), entry >= 0)
                    self.assertEqual([node.next for node in nodes], links)
                nodes[-1].next = None

    def test_cycle_randomized(self):
        rng = random.Random(3302)
        for _ in range(150):
            nodes = self.build_nodes(CYCLE, [1] * rng.randint(0, 40))
            entry = rng.randrange(-1, len(nodes))
            if entry >= 0:
                nodes[-1].next = nodes[entry]
            links = [node.next for node in nodes]
            self.assertEqual(CYCLE.has_cycle(nodes[0] if nodes else None), entry >= 0)
            self.assertEqual([node.next for node in nodes], links)
            if nodes:
                nodes[-1].next = None

    def test_merge_boundaries_identity_and_stability(self):
        cases = [([], []), ([], [1, 2]), ([1, 2], []), ([1], [2]), ([2], [1]),
                 ([1, 1, 3], [1, 2, 3]), ([-10**100, 0], [-1, 10**100])]
        for left, right in cases:
            first = self.build_nodes(MERGE, left)
            second = self.build_nodes(MERGE, right)
            expected = sorted(first + second, key=lambda node: node.value)
            with self.subTest(left=left, right=right):
                head = MERGE.merge_sorted_lists(first[0] if first else None,
                                               second[0] if second else None)
                actual = self.collect_nodes(head, len(expected))
                self.assertEqual(actual, expected)
                self.assertEqual([node.value for node in actual], sorted(left + right))

    def test_merge_rejects_unsorted_before_mutation(self):
        for bad_on_left in (True, False):
            for other_empty in (True, False):
                bad = self.build_nodes(MERGE, [1, 4, 2])
                good = self.build_nodes(MERGE, [] if other_empty else [0, 3])
                first = bad[0]
                second = good[0] if good else None
                if not bad_on_left:
                    first, second = second, first
                links = [node.next for node in bad + good]
                with self.subTest(bad_on_left=bad_on_left, other_empty=other_empty):
                    with self.assertRaises(ValueError):
                        MERGE.merge_sorted_lists(first, second)
                    self.assertEqual([node.next for node in bad + good], links)

    def test_merge_rejects_cycles_before_mutation(self):
        for bad_on_left in (True, False):
            for entry in range(3):
                cyclic = self.build_nodes(MERGE, [1, 2, 3])
                cyclic[-1].next = cyclic[entry]
                good = MERGE.Node(4)
                first, second = (cyclic[0], good) if bad_on_left else (good, cyclic[0])
                links = [node.next for node in cyclic] + [good.next]
                with self.subTest(bad_on_left=bad_on_left, entry=entry):
                    with self.assertRaises(ValueError):
                        MERGE.merge_sorted_lists(first, second)
                    self.assertEqual([node.next for node in cyclic] + [good.next], links)
                cyclic[-1].next = None

    def test_merge_rejects_shared_nodes_before_mutation(self):
        shared = MERGE.Node(3, MERGE.Node(5))
        first = MERGE.Node(1, shared)
        second = MERGE.Node(2, shared)
        nodes = [first, second, shared, shared.next]
        links = [node.next for node in nodes]
        for left, right in ((first, second), (first, first), (first, shared), (shared, first)):
            with self.subTest(left=left.value, right=right.value):
                with self.assertRaises(ValueError):
                    MERGE.merge_sorted_lists(left, right)
                self.assertEqual([node.next for node in nodes], links)

    def test_merge_randomized(self):
        rng = random.Random(3303)
        for _ in range(200):
            left = sorted(rng.randint(-8, 8) for _ in range(rng.randint(0, 20)))
            right = sorted(rng.randint(-8, 8) for _ in range(rng.randint(0, 20)))
            first = self.build_nodes(MERGE, left)
            second = self.build_nodes(MERGE, right)
            # Stable reference: all first-list ties precede second-list ties.
            expected = sorted(first + second, key=lambda node: node.value)
            head = MERGE.merge_sorted_lists(first[0] if first else None,
                                           second[0] if second else None)
            actual = self.collect_nodes(head, len(expected))
            self.assertEqual(actual, expected)
            self.assertEqual([node.value for node in actual], sorted(left + right))

    def test_invalid_heads(self):
        for invalid in (0, [], object()):
            with self.subTest(invalid=invalid):
                with self.assertRaises(TypeError):
                    REVERSE.reverse_list(invalid)
                with self.assertRaises(TypeError):
                    CYCLE.has_cycle(invalid)
                with self.assertRaises(TypeError):
                    MERGE.merge_sorted_lists(invalid, None)
                with self.assertRaises(TypeError):
                    MERGE.merge_sorted_lists(None, invalid)
        with self.assertRaises(TypeError):
            REVERSE.reverse_list(CYCLE.Node(1))


if __name__ == "__main__":
    unittest.main()
