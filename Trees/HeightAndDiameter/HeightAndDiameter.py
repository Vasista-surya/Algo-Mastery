"""Compute binary-tree height and diameter together in O(n) time, O(h) space.

Both count EDGES: empty height -1, leaf height 0, empty/leaf diameter 0.
Diameter is the longest simple path anywhere, not necessarily through the root.
Input must be an acyclic, unshared tree of this module's Node objects; depth
must fit Python's recursion limit. Duplicate integer values are allowed.
"""


class Node:
    def __init__(self, value, left=None, right=None):
        if type(value) is not int:
            raise TypeError("value must be an integer")
        for child in (left, right):
            if child is not None and not isinstance(child, Node):
                raise TypeError("children must be Node or None")
        self.value, self.left, self.right = value, left, right


def height_and_diameter(root):
    """Return (height_edges, diameter_edges); None returns (-1, 0)."""
    if root is None:
        return -1, 0
    if not isinstance(root, Node):
        raise TypeError("root and children must be Node or None")
    left_height, left_diameter = height_and_diameter(root.left)
    right_height, right_diameter = height_and_diameter(root.right)
    return (1 + max(left_height, right_height),
            max(left_diameter, right_diameter, left_height + right_height + 2))


def main():
    root = Node(1, Node(2, Node(4), Node(5)), Node(3))
    result = height_and_diameter(root)
    assert result == (2, 3)
    assert height_and_diameter(None) == (-1, 0)
    assert height_and_diameter(Node(1)) == (0, 0)
    # Longest path is inside the left subtree, not through the outer root.
    branch = Node(2, Node(3, Node(4)), Node(5, None, Node(6)))
    assert height_and_diameter(Node(1, branch)) == (3, 4)
    print(result)


if __name__ == "__main__":
    main()
