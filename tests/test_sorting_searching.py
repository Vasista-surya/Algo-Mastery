"""Regression tests for the original sorting/searching folder layout and APIs."""

import random
import unittest

from _loader import load


SORT_NAMES = ("BubbleSort", "SelectionSort", "InsertionSort", "MergeSort",
              "QuickSort", "HeapSort", "CountingSort", "RadixSort", "BucketSort")
SORTS = {}
for name in SORT_NAMES:
    filename = "Bubble-Sort" if name == "BubbleSort" else name
    module = load(f"Sorting-Algorithms/{name}/{filename}.py")
    if name == "BubbleSort":
        SORTS[name] = module.Sorting.bubble_sort
    else:
        function_name = name.removesuffix("Sort").lower() + "_sort"
        SORTS[name] = getattr(module, function_name)

SEARCHES = {}
for name in ("Linear", "Binary", "Jump", "Interpolation", "Exponential"):
    module = load(f"Searching Algorithms/{name} Search/{name}Search.py")
    SEARCHES[name] = getattr(module, name.lower() + "_search")


def sort(name, values):
    if name in ("MergeSort", "QuickSort"):
        SORTS[name](values, 0, len(values) - 1)
    else:
        SORTS[name](values)


class SortingTests(unittest.TestCase):
    def test_boundaries(self):
        cases = [[], [0], [7], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5],
                 [3, 1, 3, 0, 1], [0, 0, 0], [2147483647, 2147483646]]
        for name in SORTS:
            for original in cases:
                with self.subTest(name=name, values=original):
                    values = original.copy()
                    sort(name, values)
                    self.assertEqual(values, sorted(original))

    def test_signed_inputs(self):
        for name in SORTS:
            if name == "RadixSort":
                continue  # Its documented input domain is nonnegative integers.
            for original in ([-8, -1, -4], [4, -7, 0, -7, 2], [-2147483648, -2147483647]):
                with self.subTest(name=name, values=original):
                    values = original.copy()
                    sort(name, values)
                    self.assertEqual(values, sorted(original))

    def test_seeded_randomized(self):
        rng = random.Random(2026)
        for name in SORTS:
            for _ in range(100):
                original = [rng.randint(0 if name == "RadixSort" else -100, 100)
                            for _ in range(rng.randrange(50))]
                with self.subTest(name=name, values=original):
                    values = original.copy()
                    sort(name, values)
                    self.assertEqual(values, sorted(original))

    def test_bucket_uses_exact_integer_arithmetic(self):
        values = [10**100, -(10**100), 0, -1, 10**100 - 1]
        expected = sorted(values)
        sort("BucketSort", values)
        self.assertEqual(values, expected)

    def test_unsupported_domains_leave_input_unchanged(self):
        for name, original in (("RadixSort", [2, -1, 0]),
                               ("CountingSort", [0, 1_000_000])):
            values = original.copy()
            with self.subTest(name=name), self.assertRaises(ValueError):
                sort(name, values)
            self.assertEqual(values, original)


class SearchingTests(unittest.TestCase):
    def test_empty_singleton_duplicates_and_missing(self):
        for name, search in SEARCHES.items():
            for values in ([], [0], [7, 7, 7], [-5, -1, 0, 0, 10],
                           [-2147483648, 0, 2147483647]):
                for key in (*values, -99, 99):
                    with self.subTest(name=name, values=values, key=key):
                        before = values.copy()
                        result = search(values, key)
                        if key in values:
                            self.assertTrue(0 <= result < len(values))
                            self.assertEqual(values[result], key)
                        else:
                            self.assertEqual(result, -1)
                        self.assertEqual(values, before)

    def test_linear_preserves_original_indices(self):
        self.assertEqual(SEARCHES["Linear"]([8, 3, 7, 3], 3), 1)

    def test_seeded_randomized(self):
        rng = random.Random(2027)
        for _ in range(150):
            values = sorted(rng.randint(-30, 30) for _ in range(rng.randrange(70)))
            key = rng.randint(-35, 35)
            for name, search in SEARCHES.items():
                with self.subTest(name=name, values=values, key=key):
                    result = search(values, key)
                    if key in values:
                        self.assertTrue(0 <= result < len(values))
                        self.assertEqual(values[result], key)
                    else:
                        self.assertEqual(result, -1)


if __name__ == "__main__":
    unittest.main()
