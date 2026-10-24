"""Behavioral tests for the standalone structures; stdlib only.

Run from the repository root: python -m unittest discover -s tests -p test_structures.py
The shared _loader.load(relative_path) supports the independent source folders.
"""
from collections import deque
import heapq
import random
import unittest

from _loader import load


infix = load("Stack/InfixToPostfix/InfixToPostfix.py")
evaluation = load("Stack/ExpressionEvaluation/ExpressionEvaluation.py")
brackets = load("Stack/BalancedParentheses/BalancedParentheses.py")
queues = load("Queue/CircularQueue/CircularQueue.py")
traversals = load("Trees/TreeTraversals/TreeTraversals.py")
levels = load("Trees/LevelOrderTraversal/LevelOrderTraversal.py")
metrics = load("Trees/HeightAndDiameter/HeightAndDiameter.py")
bst = load("Trees/BinarySearchTree/BinarySearchTree.py")
heaps = load("Heaps/MinHeap/MinHeap.py")


class InfixToPostfixTests(unittest.TestCase):
    def test_precedence_associativity_and_whitespace(self):
        cases = {
            "12 + 3 * (4 - 2)": "12 3 4 2 - * +",
            "8 / 2 / 2": "8 2 / 2 /",
            "8 - 3 - 1": "8 3 - 1 -",
            "2 * (3 + 4) / 7": "2 3 4 + * 7 /",
            "\t(12\n+\v3) * 2\r\f": "12 3 + 2 *",
            "00012 + 0": "00012 0 +",
        }
        for expression, expected in cases.items():
            with self.subTest(expression=expression):
                self.assertEqual(infix.infix_to_postfix(expression), expected)

    def test_empty_and_invalid_syntax(self):
        invalid = ("", " \t\n", "()", "( )", "1+", "+1", "-2", "1 2",
                   "(1", "1)", "1+(2))", "2(3)", "(2)3", "(2)(3)",
                   "2**3", "2//3", "1 + -2", "1.5", "a+1", "1e2", "\u0661",
                   "1\u00a0+2")
        for expression in invalid:
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                infix.infix_to_postfix(expression)

    def test_literal_boundaries_and_deep_parentheses(self):
        self.assertEqual(infix.infix_to_postfix("1000000000"), "1000000000")
        self.assertEqual(infix.infix_to_postfix("(" * 256 + "0" + ")" * 256), "0")
        leading_zeros = "0" * 5000 + "1"
        self.assertEqual(infix.infix_to_postfix(leading_zeros), leading_zeros)
        for expression in ("1000000001", "9" * 100, "1+1000000001"):
            with self.subTest(expression=expression), self.assertRaises(OverflowError):
                infix.infix_to_postfix(expression)

    def test_wrong_argument_types(self):
        for value in (None, 12, [], True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                infix.infix_to_postfix(value)


class ExpressionEvaluationTests(unittest.TestCase):
    def test_arithmetic_and_truncation(self):
        cases = {
            "12 3 4 2 - * +": 18,
            "9 2 /": 4,
            "0 7 - 3 /": -2,
            "7 0 3 - /": -2,
            "0 7 - 0 3 - /": 2,
            "0 1 - 2 /": 0,
            "\t0012\n3\v+\r\f": 15,
            "0": 0,
        }
        for expression, expected in cases.items():
            with self.subTest(expression=expression):
                self.assertEqual(evaluation.evaluate_postfix(expression), expected)

    def test_converter_integration(self):
        cases = {"12 + 3 * (4 - 2)": 18, "(0-7)/3": -2,
                 "8-3-1": 4, "8/2/2": 2, "(4+6)*(8-3)/2": 25}
        for expression, expected in cases.items():
            with self.subTest(expression=expression):
                postfix = infix.infix_to_postfix(expression)
                self.assertEqual(evaluation.evaluate_postfix(postfix), expected)

    def test_empty_and_invalid_tokens_or_arity(self):
        invalid = ("", " \t", "1 2", "+", "1 +", "1 2 + +", "1 2 + 3",
                   "-1", "+1", "1.5", "1 2 ^", "(1)", "12+", "1 2+",
                   "1 a +", "\u0661", "1\u00a02 +")
        for expression in invalid:
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                evaluation.evaluate_postfix(expression)

    def test_division_by_zero(self):
        for expression in ("1 0 /", "0 0 /", "5 2 2 - /"):
            with self.subTest(expression=expression), self.assertRaises(ZeroDivisionError):
                evaluation.evaluate_postfix(expression)

    def test_numeric_boundaries_and_intermediate_overflow(self):
        for expression, expected in (("1000000000", 10**9),
                                     ("0 1000000000 -", -10**9),
                                     ("1000000000 1 *", 10**9),
                                     ("0" * 5000 + "1", 1)):
            with self.subTest(expression=expression):
                self.assertEqual(evaluation.evaluate_postfix(expression), expected)
        invalid = ("1000000001", "9" * 100, "1000000000 1 +",
                   "0 1000000000 - 1 -", "1000000000 1000000000 *",
                   "1000000000 1 + 1 -")
        for expression in invalid:
            with self.subTest(expression=expression), self.assertRaises(OverflowError):
                evaluation.evaluate_postfix(expression)

    def test_wrong_argument_types(self):
        for value in (None, 12, [], True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                evaluation.evaluate_postfix(value)


class BalancedParenthesesTests(unittest.TestCase):
    def test_balanced_empty_and_ignored_text(self):
        for text in ("", "plain text", "{[()]}", "()[]{}", "a*(b+[c-{d}])",
                     "\u200e\u0661", "'()'"):
            with self.subTest(text=text):
                self.assertTrue(brackets.is_balanced(text))

    def test_unbalanced(self):
        for text in ("(", ")", "([)]", "{]", "(()", "())", "'('"):
            with self.subTest(text=text):
                self.assertFalse(brackets.is_balanced(text))

    def test_depth_boundary_is_dynamic_in_python(self):
        self.assertTrue(brackets.is_balanced("(" * 2048 + ")" * 2048))
        self.assertFalse(brackets.is_balanced("(" * 2048 + ")" * 2047))

    def test_wrong_argument_types(self):
        for value in (None, 12, [], True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                brackets.is_balanced(value)


class CircularQueueTests(unittest.TestCase):
    def test_fifo_peek_and_wraparound(self):
        queue = queues.CircularQueue(3)
        for value in (10, 20, 30):
            queue.enqueue(value)
        self.assertEqual(queue.peek(), 10)
        self.assertEqual(len(queue), 3)
        with self.assertRaises(OverflowError):
            queue.enqueue(40)
        self.assertEqual(queue.dequeue(), 10)
        queue.enqueue(40)
        self.assertEqual([queue.dequeue() for _ in range(3)], [20, 30, 40])
        self.assertTrue(queue.is_empty())

    def test_empty_errors_and_reuse(self):
        queue = queues.CircularQueue(1)
        for _ in range(3):
            self.assertTrue(queue.is_empty())
            for operation in (queue.peek, queue.dequeue):
                with self.assertRaises(IndexError):
                    operation()
            queue.enqueue(-10**100)
            with self.assertRaises(OverflowError):
                queue.enqueue(2)
            self.assertEqual(queue.peek(), -10**100)
            self.assertEqual(queue.dequeue(), -10**100)
            self.assertEqual(len(queue), 0)

    def test_invalid_capacity_and_values_preserve_state(self):
        for capacity in (0, -1):
            with self.subTest(capacity=capacity), self.assertRaises(ValueError):
                queues.CircularQueue(capacity)
        for capacity in (None, 1.5, "2", True):
            with self.subTest(capacity=capacity), self.assertRaises(TypeError):
                queues.CircularQueue(capacity)
        queue = queues.CircularQueue(2)
        queue.enqueue(7)
        for value in (None, 1.5, "2", True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                queue.enqueue(value)
            self.assertEqual(len(queue), 1)
            self.assertEqual(queue.peek(), 7)

    def test_repeated_wraparound_against_deque(self):
        queue, reference = queues.CircularQueue(7), deque()
        rng = random.Random(42)
        for _ in range(300):
            if rng.randrange(2) == 0:
                value = rng.randint(-100, 100)
                if len(reference) == 7:
                    with self.assertRaises(OverflowError):
                        queue.enqueue(value)
                else:
                    queue.enqueue(value)
                    reference.append(value)
            elif reference:
                self.assertEqual(queue.dequeue(), reference.popleft())
            else:
                with self.assertRaises(IndexError):
                    queue.dequeue()
            self.assertEqual(len(queue), len(reference))
            self.assertEqual(queue.is_empty(), not reference)
            if reference:
                self.assertEqual(queue.peek(), reference[0])
        self.assertEqual([queue.dequeue() for _ in range(len(queue))], list(reference))


def sample_tree(module):
    """Build with each independent algorithm's own Node class."""
    return module.Node(1, module.Node(2, module.Node(4), module.Node(5)), module.Node(3))


class TreeTraversalsTests(unittest.TestCase):
    def test_all_three_orders_and_fresh_results(self):
        root = sample_tree(traversals)
        self.assertEqual(traversals.preorder(root), [1, 2, 4, 5, 3])
        self.assertEqual(traversals.inorder(root), [4, 2, 5, 1, 3])
        self.assertEqual(traversals.postorder(root), [4, 5, 2, 3, 1])
        result = traversals.inorder(root)
        result.clear()
        self.assertEqual(traversals.inorder(root), [4, 2, 5, 1, 3])

    def test_empty_singleton_and_duplicate_values(self):
        for operation in (traversals.preorder, traversals.inorder, traversals.postorder):
            with self.subTest(operation=operation.__name__):
                self.assertEqual(operation(None), [])
                self.assertEqual(operation(traversals.Node(-10**100)), [-10**100])
                self.assertEqual(operation(traversals.Node(1, traversals.Node(1))), [1, 1])

    def test_skewed_tree(self):
        root = None
        for value in reversed(range(100)):
            root = traversals.Node(value, None, root)
        self.assertEqual(traversals.preorder(root), list(range(100)))
        self.assertEqual(traversals.inorder(root), list(range(100)))
        self.assertEqual(traversals.postorder(root), list(reversed(range(100))))

    def test_invalid_nodes(self):
        for operation in (traversals.preorder, traversals.inorder, traversals.postorder):
            with self.subTest(operation=operation.__name__), self.assertRaises(TypeError):
                operation(42)
        for value in (None, "1", True, 1.5):
            with self.subTest(value=value), self.assertRaises(TypeError):
                traversals.Node(value)
        with self.assertRaises(TypeError):
            traversals.Node(1, left=2)
        with self.assertRaises(TypeError):
            traversals.Node(1, right=levels.Node(2))


class LevelOrderTraversalTests(unittest.TestCase):
    def test_flat_breadth_first_order(self):
        root = sample_tree(levels)
        self.assertEqual(levels.level_order(root), [1, 2, 3, 4, 5])
        root = levels.Node(1, levels.Node(2, None, levels.Node(4)),
                           levels.Node(3, levels.Node(5)))
        self.assertEqual(levels.level_order(root), [1, 2, 3, 4, 5])

    def test_empty_singleton_and_duplicates(self):
        self.assertEqual(levels.level_order(None), [])
        self.assertEqual(levels.level_order(levels.Node(-1)), [-1])
        root = levels.Node(2, levels.Node(2), levels.Node(2))
        self.assertEqual(levels.level_order(root), [2, 2, 2])

    def test_wide_and_deep_trees(self):
        nodes = [levels.Node(value) for value in range(2049)]
        for index, node in enumerate(nodes):
            if 2 * index + 1 < len(nodes):
                node.left = nodes[2 * index + 1]
            if 2 * index + 2 < len(nodes):
                node.right = nodes[2 * index + 2]
        self.assertEqual(levels.level_order(nodes[0]), list(range(2049)))
        root = None
        for value in reversed(range(1500)):
            root = levels.Node(value, None, root)
        self.assertEqual(levels.level_order(root), list(range(1500)))

    def test_invalid_nodes(self):
        for root in (42, [], ""):
            with self.subTest(root=root), self.assertRaises(TypeError):
                levels.level_order(root)
        with self.assertRaises(TypeError):
            levels.Node(True)
        with self.assertRaises(TypeError):
            levels.Node(1, right=2)
        root = levels.Node(1)
        root.left = "invalid child"
        with self.assertRaises(TypeError):
            levels.level_order(root)


class HeightAndDiameterTests(unittest.TestCase):
    def test_normal_tree_and_edge_units(self):
        self.assertEqual(metrics.height_and_diameter(sample_tree(metrics)), (2, 3))
        self.assertEqual(metrics.height_and_diameter(None), (-1, 0))
        self.assertEqual(metrics.height_and_diameter(metrics.Node(1)), (0, 0))
        self.assertEqual(metrics.height_and_diameter(metrics.Node(1, metrics.Node(1))), (1, 1))

    def test_diameter_not_through_root(self):
        branch = metrics.Node(2, metrics.Node(3, metrics.Node(4)),
                              metrics.Node(5, None, metrics.Node(6)))
        self.assertEqual(metrics.height_and_diameter(metrics.Node(1, branch)), (3, 4))

    def test_skewed_tree(self):
        root = None
        for value in range(100):
            root = metrics.Node(value, root)
        self.assertEqual(metrics.height_and_diameter(root), (99, 99))

    def test_invalid_nodes(self):
        for root in (42, [], ""):
            with self.subTest(root=root), self.assertRaises(TypeError):
                metrics.height_and_diameter(root)
        with self.assertRaises(TypeError):
            metrics.Node("1")
        with self.assertRaises(TypeError):
            metrics.Node(1, left=2)
        root = metrics.Node(1)
        root.right = False
        with self.assertRaises(TypeError):
            metrics.height_and_diameter(root)


class BinarySearchTreeTests(unittest.TestCase):
    def test_insert_search_duplicates_and_empty(self):
        tree = bst.BinarySearchTree()
        self.assertEqual(tree.inorder(), [])
        self.assertFalse(tree.search(1))
        self.assertFalse(tree.delete(1))
        for value in (5, 3, 7, 2, 4, 6, 8):
            self.assertTrue(tree.insert(value))
            self.assertTrue(tree.search(value))
        self.assertFalse(tree.insert(5))
        self.assertFalse(tree.search(9))
        self.assertEqual(tree.inorder(), [2, 3, 4, 5, 6, 7, 8])
        result = tree.inorder()
        result.clear()
        self.assertEqual(tree.inorder(), [2, 3, 4, 5, 6, 7, 8])

    def test_delete_leaf_one_child_two_children_and_root(self):
        tree = bst.BinarySearchTree()
        remaining = {5, 3, 7, 2, 4, 6, 8}
        for value in (5, 3, 7, 2, 4, 6, 8):
            tree.insert(value)
        for value in (2, 7, 3, 5, 4, 6, 8):
            self.assertTrue(tree.delete(value))
            remaining.remove(value)
            self.assertFalse(tree.search(value))
            self.assertEqual(tree.inorder(), sorted(remaining))
            self.assertFalse(tree.delete(value))
        self.assertTrue(tree.insert(1))
        self.assertTrue(tree.delete(1))
        self.assertEqual(tree.inorder(), [])

    def test_successor_with_right_child_and_single_child_root(self):
        tree = bst.BinarySearchTree()
        for value in (50, 20, 80, 60, 90, 55, 57):
            tree.insert(value)
        self.assertTrue(tree.delete(50))
        self.assertEqual(tree.inorder(), [20, 55, 57, 60, 80, 90])
        for child in (-1, 1):
            tree = bst.BinarySearchTree()
            tree.insert(0)
            tree.insert(child)
            self.assertTrue(tree.delete(0))
            self.assertEqual(tree.inorder(), [child])

    def test_extreme_keys_and_skewed_tree(self):
        tree = bst.BinarySearchTree()
        values = [-10**100] + list(range(256)) + [10**100]
        for value in values:
            self.assertTrue(tree.insert(value))
        self.assertEqual(tree.inorder(), values)
        for value in reversed(values):
            self.assertTrue(tree.search(value))
            self.assertTrue(tree.delete(value))
        self.assertEqual(tree.inorder(), [])

    def test_invalid_keys_do_not_mutate(self):
        tree = bst.BinarySearchTree()
        tree.insert(5)
        for operation in (tree.insert, tree.search, tree.delete):
            for value in (None, True, "5", 5.0):
                with self.subTest(operation=operation.__name__, value=value), self.assertRaises(TypeError):
                    operation(value)
                self.assertEqual(tree.inorder(), [5])

    def test_mixed_operations_against_set(self):
        tree, reference = bst.BinarySearchTree(), set()
        rng = random.Random(7)
        for _ in range(300):
            key, operation = rng.randint(-30, 30), rng.randrange(3)
            if operation == 0:
                self.assertEqual(tree.insert(key), key not in reference)
                reference.add(key)
            elif operation == 1:
                self.assertEqual(tree.delete(key), key in reference)
                reference.discard(key)
            else:
                self.assertEqual(tree.search(key), key in reference)
            self.assertEqual(tree.inorder(), sorted(reference))


class MinHeapTests(unittest.TestCase):
    def test_sorted_removal_for_varied_orders_and_duplicates(self):
        cases = ([5, -2, 8, -2, 1], list(range(32)), list(reversed(range(32))),
                 [7] * 16, [-10**100, 10**100, 0, -1, 1])
        for values in cases:
            with self.subTest(values=values):
                heap = heaps.MinHeap(len(values))
                for index, value in enumerate(values):
                    heap.push(value)
                    self.assertEqual(heap.peek(), min(values[:index + 1]))
                self.assertEqual(len(heap), len(values))
                with self.assertRaises(OverflowError):
                    heap.push(0)
                self.assertEqual([heap.pop() for _ in values], sorted(values))
                self.assertTrue(heap.is_empty())

    def test_empty_single_capacity_and_reuse(self):
        heap = heaps.MinHeap(1)
        for value in (0, -1, 10**100):
            self.assertEqual(len(heap), 0)
            for operation in (heap.peek, heap.pop):
                with self.assertRaises(IndexError):
                    operation()
            heap.push(value)
            self.assertEqual(heap.peek(), value)
            with self.assertRaises(OverflowError):
                heap.push(value - 1)
            self.assertEqual(heap.pop(), value)
            self.assertTrue(heap.is_empty())

    def test_invalid_capacity_and_values_preserve_state(self):
        for capacity in (0, -1):
            with self.subTest(capacity=capacity), self.assertRaises(ValueError):
                heaps.MinHeap(capacity)
        for capacity in (None, 1.5, "2", True):
            with self.subTest(capacity=capacity), self.assertRaises(TypeError):
                heaps.MinHeap(capacity)
        heap = heaps.MinHeap(3)
        heap.push(5)
        for value in (None, "1", 1.5, True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                heap.push(value)
            self.assertEqual(len(heap), 1)
            self.assertEqual(heap.peek(), 5)

    def test_mixed_operations_against_heapq(self):
        heap, reference = heaps.MinHeap(17), []
        rng = random.Random(19)
        for _ in range(400):
            if rng.randrange(3) < 2:
                value = rng.randint(-50, 50)
                if len(reference) == 17:
                    with self.assertRaises(OverflowError):
                        heap.push(value)
                else:
                    heap.push(value)
                    heapq.heappush(reference, value)
            elif reference:
                self.assertEqual(heap.pop(), heapq.heappop(reference))
            else:
                with self.assertRaises(IndexError):
                    heap.pop()
            self.assertEqual(len(heap), len(reference))
            self.assertEqual(heap.is_empty(), not reference)
            if reference:
                self.assertEqual(heap.peek(), reference[0])
        self.assertEqual([heap.pop() for _ in range(len(heap))], sorted(reference))


if __name__ == "__main__":
    unittest.main()
