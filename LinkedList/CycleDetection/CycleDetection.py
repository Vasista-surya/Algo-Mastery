"""Floyd's cycle detection: O(n) time, O(1) space, with no link mutations.

Nodes store built-in integers (unbounded, excluding bools). Every link must
remain Node or None. n counts distinct reachable nodes; None is an empty list.
"""


class Node:
    """An integer node, including nodes that will later be linked into a cycle."""

    def __init__(self, value, next_node=None):
        if type(value) is not int:
            raise TypeError("node value must be an integer")
        if next_node is not None and not isinstance(next_node, Node):
            raise TypeError("next_node must be a Node or None")
        self.value = value
        self.next = next_node


def has_cycle(head):
    """Return whether a next-link cycle is reachable; compare identity, not values."""
    if head is not None and not isinstance(head, Node):
        raise TypeError("head must be a Node or None")
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


if __name__ == "__main__":
    first = Node(1, Node(2, Node(3)))
    assert not has_cycle(first)
    assert not has_cycle(None)
    first.next.next.next = first.next
    assert has_cycle(first)
    print("Cycle detected:", has_cycle(first))
    first.next.next.next = None
    single = Node(1)
    assert not has_cycle(single)
    single.next = single
    assert has_cycle(single)
    single.next = None
