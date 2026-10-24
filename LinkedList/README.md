# Singly linked lists

`ReverseLinkedList`, `CycleDetection`, and `MergeSortedLists` each contain an
independently runnable `.py`, `.java`, and `.c` file with the directory's
PascalCase name. Each has its own integer `Node` type with `value` and `next`
fields. Java helpers are nested inside the public filename-matching class.
Python nodes from different standalone modules are deliberately separate types.

## APIs and examples

| Directory | Python API | Java static API | Time | Extra space |
| --- | --- | --- | --- | --- |
| `ReverseLinkedList` | `reverse_list(head)` | `reverseList(head)` | O(n), including cycle validation | O(1) |
| `CycleDetection` | `has_cycle(head)` | `hasCycle(head)` | O(n) distinct reachable nodes | O(1) |
| `MergeSortedLists` | `merge_sorted_lists(first, second)` | `mergeSortedLists(first, second)` | O(n+m), including validation | O(1) |

Python construction: `Node(value, next_node=None)`. Java construction:
`new ClassName.Node(value)` or `new ClassName.Node(value, next)`.

```python
# In the reversal module:
head = Node(1, Node(2, Node(3)))
head = reverse_list(head)  # 3 -> 2 -> 1 -> None; reuses the same nodes
assert reverse_list(None) is None

# In the cycle-detection module:
node = Node(7)
assert not has_cycle(node)
node.next = node
assert has_cycle(node)
node.next = None

# In the merge module:
first = Node(1, Node(3))
second = Node(1, Node(2))
head = merge_sorted_lists(first, second)  # 1 -> 1 -> 2 -> 3
assert head is first and head.next is second  # stable across equal values
```

## Contracts

- `None` / `null` / `NULL` denotes an empty list. Reversing it returns empty;
  cycle detection returns false; merging two empty lists returns empty. Merging
  one empty list returns the other list after validation.
- Reversal and merge **rewire the original nodes**. Save their returned head;
  previous head references no longer describe independent original lists.
  Neither operation changes values or copies result nodes. Merge uses one
  temporary dummy node that is not part of the result.
- Reversal rejects cyclic input **before mutation**. Cycle detection accepts
  cycles, compares node identity rather than values, and changes no links.
- Merge requires acyclic, nondecreasing, **disjoint** inputs. It rejects cycles,
  unsorted input, and shared nodes (including identical nonempty heads), before
  modifying either list. Two acyclic singly linked lists share nodes exactly
  when their nonempty tails are the same object. Validation stays O(1) space.
- Merge is stable: ties choose the first list, and order within each input is
  preserved. Duplicate and negative values are valid.
- Python values must be built-in integers, excluding bools (`TypeError`
  otherwise); they are unbounded. Constructors check the next-node type and
  algorithms reject invalid head types. Callers must keep every subsequently
  assigned link a `Node` from that module or `None`, and values integers.
  Invalid cycles/order/sharing raise `ValueError`. Java uses `int` values and
  throws `IllegalArgumentException` for these structural errors.
- No value arithmetic is needed, so extreme integer values are safe. Loops
  follow links without a numeric length counter; there is no fixed capacity or
  recursive call stack. All nodes/links must be valid and stable during calls.

## C99 API and ownership

```c
typedef struct Node {
    int32_t value;
    struct Node *next;
} Node;

int reverse_list(Node **head);
int has_cycle(const Node *head);
int merge_sorted_lists(Node *first, Node *second, Node **out);
```

Compile these files separately: each intentionally defines its own `Node` and
`main`. C requires `int32_t` support; no signed addition/subtraction on values
is used. Input pointers must reference live nodes with valid next pointers.
The algorithm cannot validate dangling pointers or the lifetime of caller data.

- `reverse_list` returns `1` and updates `*head` on success; `0` for a null
  head-output pointer or cyclic input. `head != NULL` with `*head == NULL` is valid.
- `has_cycle` returns `1` for a reachable cycle, otherwise `0`.
- `merge_sorted_lists` returns `1` and sets `*out` on success, `0` for invalid
  inputs or a null output pointer. On failure, output and all node links stay
  unchanged. Use a separate head variable for `out` / `head`, not a node's
  `next` field, to avoid aliasing output writes into the list being processed.
- The caller owns every node. Algorithms allocate/free nothing; demo nodes are
  stack-owned, so no heap cleanup is necessary. For caller-allocated lists, free
  each node exactly once from the new head after reversal/merge; do not free
  the original input heads as separate lists. Break cycles before linear cleanup.

## Run

For example, from `LinkedList/ReverseLinkedList`:

```text
python ReverseLinkedList.py
javac ReverseLinkedList.java
java -ea ReverseLinkedList
cc -std=c99 -Wall -Wextra -pedantic ReverseLinkedList.c -o reverse_list
./reverse_list
```

Each demo prints deterministic results and uses real self-check assertions.
Keep Python assertions enabled, run Java with `-ea`, and compile C without
`-DNDEBUG`. Python edge, identity, invalid-input and seeded randomized tests are
in `tests/test_foundations.py`, using the shared `tests/_loader.py` helper.
From the root: `python -m unittest discover -s tests -p "test_foundations.py"`.
