"""Breadth-first traversal: O(n) time, O(w) queue plus O(n) output space.

w is maximum tree width. Input is a finite acyclic tree without shared children,
using this module's Node class. None is empty; duplicate integer values are fine.
"""
from collections import deque


class Node:
    def __init__(self, value, left=None, right=None):
        if type(value) is not int:
            raise TypeError("value must be an integer")
        for child in (left, right):
            if child is not None and not isinstance(child, Node):
                raise TypeError("children must be Node or None")
        self.value, self.left, self.right = value, left, right


def level_order(root):
    """Return a flat list, top to bottom and left to right; None returns []."""
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if not isinstance(node, Node):
            raise TypeError("root and children must be Node or None")
        result.append(node.value)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return result


def main():
    root = Node(1, Node(2, Node(4), Node(5)), Node(3))
    result = level_order(root)
    assert result == [1, 2, 3, 4, 5]
    assert level_order(None) == []
    assert level_order(Node(-1)) == [-1]
    assert level_order(Node(1, None, Node(2, Node(3)))) == [1, 2, 3]
    print(result)


if __name__ == "__main__":
    main()
