"""Depth-first binary-tree traversals: O(n) time, O(h) stack plus O(n) output.

Inputs must be finite, acyclic trees of this module's Node objects; no shared
children. Values are integers; duplicates are allowed. None denotes an empty
tree. Recursion depth must fit Python's recursion limit.
"""


class Node:
    def __init__(self, value, left=None, right=None):
        if type(value) is not int:
            raise TypeError("value must be an integer")
        for child in (left, right):
            if child is not None and not isinstance(child, Node):
                raise TypeError("children must be Node or None")
        self.value, self.left, self.right = value, left, right


def _traverse(root, order):
    result = []

    def visit(node):
        if node is None:
            return
        if not isinstance(node, Node):
            raise TypeError("root and children must be Node or None")
        if order == "pre":
            result.append(node.value)
        visit(node.left)
        if order == "in":
            result.append(node.value)
        visit(node.right)
        if order == "post":
            result.append(node.value)

    visit(root)
    return result


def preorder(root):
    """Return root-left-right values; an empty tree returns []."""
    return _traverse(root, "pre")


def inorder(root):
    """Return left-root-right values; an empty tree returns []."""
    return _traverse(root, "in")


def postorder(root):
    """Return left-right-root values; an empty tree returns []."""
    return _traverse(root, "post")


def main():
    root = Node(1, Node(2, Node(4), Node(5)), Node(3))
    results = (preorder(root), inorder(root), postorder(root))
    assert results == ([1, 2, 4, 5, 3], [4, 2, 5, 1, 3], [4, 5, 2, 3, 1])
    for traversal in (preorder, inorder, postorder):
        assert traversal(None) == []
        assert traversal(Node(-1)) == [-1]
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
