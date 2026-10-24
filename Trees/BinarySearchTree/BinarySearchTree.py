"""Unbalanced integer BST with set semantics (duplicate insertions are ignored).

insert/search/delete: O(h) time, O(1) auxiliary space; worst-case h=O(n).
inorder: O(n) time, O(h) stack plus O(n) output. Storage: O(n).
Empty search/delete return False; empty inorder returns []. All keys must be
int, excluding bool. Nodes are private implementation details.
"""


class _Node:
    def __init__(self, value):
        self.value = value
        self.left = self.right = None


class BinarySearchTree:
    def __init__(self):
        self._root = None

    @staticmethod
    def _check_key(value):
        if type(value) is not int:
            raise TypeError("key must be an integer")

    def insert(self, value):
        """Insert a new key and return True; duplicates return False."""
        self._check_key(value)
        if self._root is None:
            self._root = _Node(value)
            return True
        node = self._root
        while True:
            if value == node.value:
                return False
            if value < node.value:
                if node.left is None:
                    node.left = _Node(value)
                    return True
                node = node.left
            else:
                if node.right is None:
                    node.right = _Node(value)
                    return True
                node = node.right

    def search(self, value):
        """Return membership without modifying the tree."""
        self._check_key(value)
        node = self._root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def delete(self, value):
        """Delete a key if present; return whether it existed."""
        self._check_key(value)
        parent, node = None, self._root
        while node is not None and node.value != value:
            parent = node
            node = node.left if value < node.value else node.right
        if node is None:
            return False
        if node.left is not None and node.right is not None:
            successor_parent, successor = node, node.right
            while successor.left is not None:
                successor_parent, successor = successor, successor.left
            node.value = successor.value
            parent, node = successor_parent, successor
        child = node.left if node.left is not None else node.right
        if parent is None:
            self._root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child
        return True

    def inorder(self):
        """Return a new sorted list of all keys."""
        result, stack, node = [], [], self._root
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.value)
            node = node.right
        return result


def main():
    tree = BinarySearchTree()
    assert not tree.search(5) and not tree.delete(5) and tree.inorder() == []
    for value in (5, 3, 7, 2, 4, 6, 8):
        inserted = tree.insert(value)
        assert inserted
    duplicate = tree.insert(5)
    assert not duplicate and tree.search(6)
    for value in (2, 7, 3, 5):  # Leaf, two children, one child, then root.
        deleted = tree.delete(value)
        assert deleted and not tree.search(value)
    result = tree.inorder()
    assert result == [4, 6, 8]
    print(result)


if __name__ == "__main__":
    main()
