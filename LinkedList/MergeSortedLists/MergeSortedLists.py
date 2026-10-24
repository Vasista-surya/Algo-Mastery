"""Stable, in-place merge of two disjoint nondecreasing singly linked lists.

O(n+m) time including validation, O(1) extra space. Nodes contain built-in ints
(unbounded, excluding bools); links must remain Node or None. Reject cycles,
unsorted inputs, and shared nodes before mutation. None is an empty list.
"""


class Node:
    """An integer node; merge reuses these nodes instead of copying values."""

    def __init__(self, value, next_node=None):
        if type(value) is not int:
            raise TypeError("node value must be an integer")
        if next_node is not None and not isinstance(next_node, Node):
            raise TypeError("next_node must be a Node or None")
        self.value = value
        self.next = next_node


def merge_sorted_lists(first, second):
    """Return the merged head; equal values take nodes from first before second.

    Successful merging consumes the original list structure. Invalid inputs
    raise ValueError (bad heads raise TypeError), with both lists unchanged.
    """
    tails = []  # Exactly two entries: constant space, not a visited-node set.
    for head in (first, second):
        if head is not None and not isinstance(head, Node):
            raise TypeError("heads must be Nodes or None")
        slow = fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                raise ValueError("cannot merge a cyclic list")
        tail = None
        current = head
        while current is not None:
            if current.next is not None and current.value > current.next.value:
                raise ValueError("lists must be nondecreasing")
            tail = current
            current = current.next
        tails.append(tail)
    # Acyclic singly linked lists intersect exactly when their nonempty tails match.
    if tails[0] is not None and tails[0] is tails[1]:
        raise ValueError("lists must not share nodes")
    dummy = Node(0)
    tail = dummy
    while first is not None and second is not None:
        if first.value <= second.value:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next
    tail.next = first if first is not None else second
    return dummy.next


if __name__ == "__main__":
    first = Node(1, Node(3))
    second = Node(1, Node(2))
    first_tail = first.next
    result = merge_sorted_lists(first, second)
    assert result is first and result.next is second
    assert result.next.next.value == 2 and result.next.next.next is first_tail
    assert first_tail.next is None
    assert merge_sorted_lists(None, None) is None
    single = Node(7)
    assert merge_sorted_lists(None, single) is single
    try:
        merge_sorted_lists(single, single)
    except ValueError:
        assert single.next is None
    else:
        raise AssertionError("shared nodes must be rejected")
    print("Merged:", result.value, result.next.value,
          result.next.next.value, result.next.next.next.value)
