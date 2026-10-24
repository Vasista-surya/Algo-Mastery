"""Reverse an acyclic singly linked list in place: O(n) time, O(1) space.

Nodes store built-in integers (unbounded, excluding bools). Links must remain
Node or None. Cycles are rejected before any links are changed; None is empty.
"""


class Node:
    """An integer node; use this module's Node class for this standalone API."""

    def __init__(self, value, next_node=None):
        if type(value) is not int:
            raise TypeError("node value must be an integer")
        if next_node is not None and not isinstance(next_node, Node):
            raise TypeError("next_node must be a Node or None")
        self.value = value
        self.next = next_node


def reverse_list(head):
    """Return the new head, preserving node identity; reject cyclic input."""
    if head is not None and not isinstance(head, Node):
        raise TypeError("head must be a Node or None")
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            raise ValueError("cannot reverse a cyclic list")
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous, current = current, following
    return previous


if __name__ == "__main__":
    first = Node(1, Node(2, Node(3)))
    last = first.next.next
    result = reverse_list(first)
    assert result is last
    assert result.value == 3 and result.next.value == 2
    assert result.next.next is first and first.next is None
    assert reverse_list(None) is None
    single = Node(7)
    assert reverse_list(single) is single and single.next is None
    cycle = Node(9)
    cycle.next = cycle
    try:
        reverse_list(cycle)
    except ValueError:
        assert cycle.next is cycle
    else:
        raise AssertionError("cycles must be rejected")
    cycle.next = None
    print("Reversed:", result.value, result.next.value, result.next.next.value)
