# Binary trees and binary search trees

Every directory contains matching standalone Python, Java, and C99 files, each
with a deterministic demo and meaningful assertions. Python imports are silent;
Java's public class matches the filename, with nested helper types. No file
depends on another topic.

## APIs

For the first three topics, each file defines its **own** `Node(value, left,
right)` type (Python/Java children default to empty with the one-value
constructor). Construct nodes from the same module/class as the algorithm.
C uses `Node { int value; Node *left, *right; }` with caller-owned nodes.

| Directory | Python | Java API | C functions |
| --- | --- | --- | --- |
| `TreeTraversals` | `preorder(root)`, `inorder(root)`, `postorder(root)` | `preorder(root)`, `inorder(root)`, `postorder(root)` | same names: `(root, out, capacity, &length)` |
| `LevelOrderTraversal` | `level_order(root)` | `levelOrder(root)` | `level_order(root, out, capacity, &length)` |
| `HeightAndDiameter` | `height_and_diameter(root)` | `heightAndDiameter(root)` | `height_and_diameter(root, &metrics)` |
| `BinarySearchTree` | `BinarySearchTree()`; `insert(key)`, `search(key)`, `delete(key)`, `inorder()` | `new BinarySearchTree()`; same method names | `bst_insert(&root, key)`, `bst_search(root, key)`, `bst_delete(&root, key)`, `bst_inorder(root, out, capacity, &length)`, `bst_free(&root)` |

DFS returns root-left-right, left-root-right, or left-right-root order. Level
order returns a **flat** list, top to bottom and left to right. Python/Java
return newly allocated lists; C writes into a caller-sized integer buffer.

Height/diameter return a Python pair or Java/C `Metrics` with `height` and
`diameter` fields. **Both count edges.** Empty height is -1; leaf height is 0;
empty/leaf diameter is 0. Diameter is the longest simple path anywhere in the
tree, including paths wholly inside a subtree. It is computed with height in
one postorder pass. Java/C reject metrics beyond their `int` range.

## Inputs, empty behavior, and ownership

- General trees must be finite, acyclic, and without shared children. Structural
  cycle detection is not performed. Recursive DFS/metrics (and C BST traversal
  and release) require depth that fits the language's call stack.
- `None` / `null` / `NULL` roots mean empty. Traversals return empty lists (C:
  success with length zero). Empty metrics are `(-1, 0)`. Empty BST searches and
  deletions report absence.
- General trees allow duplicate values. **BSTs have set semantics:** duplicate
  insertion leaves the tree unchanged. Python/Java insert/delete return a bool
  indicating whether a key was added/removed; search returns membership.
  BST operations preserve strict ordering, including successor replacement for
  deletion of nodes with two children. Trees are not self-balancing.
- Python values/keys must be integers, excluding `bool`; constructors and BST
  methods raise `TypeError` otherwise. General-tree algorithms also reject roots
  or encountered children of the wrong type. Python integers are arbitrary-size;
  Java/C values use native `int`. Do not manually corrupt node fields/invariants.
- C traversal APIs return `TRAVERSAL_OK` / `LEVEL_OK` / `BST_OK` on success,
  `*_INVALID` for NULL length pointers or NULL output with nonzero capacity, and
  `*_CAPACITY` if the output is too small. Capacity is measured in **ints**.
  On capacity failure, `length` describes the valid partial prefix; output
  entries beyond it are untouched. `(NULL, 0)` is a valid zero-capacity output.
  Invalid arguments leave output/length unchanged. Buffers must not alias nodes
  or the length variable.
- C level-order additionally checks a circular queue holding at most 1024
  **pending nodes**, possibly spanning two adjacent levels; excess pending work
  returns `LEVEL_CAPACITY`. This is not a total-node limit. No heap allocation
  is used in the three general-tree demos; their automatic nodes need no free.
- C metrics return `METRICS_OK`, `METRICS_INVALID` (NULL output), or
  `METRICS_RANGE`; on failure the output is unchanged.
- C BST: start with `Node *root = NULL`. `BST_DUPLICATE`, `BST_NOT_FOUND`,
  `BST_INVALID`, and `BST_NOMEM` distinguish insertion/deletion failures;
  failed insertion preserves the tree. Nodes are allocated by insertion, freed
  by deletion, and the rest released by `bst_free(&root)`, which sets the root
  to NULL. Repeated free and `bst_free(NULL)` are safe. Do not attach externally
  owned nodes or retain pointers to nodes across mutation. Demos clean up on
  allocation failure and normal exit.

## Complexity

Let n be node count, h tree height, and w maximum width.

| Algorithm | Time | Auxiliary space (excluding returned output/tree storage) |
| --- | --- | --- |
| Preorder/inorder/postorder | O(n) | O(h) recursion |
| Level order | O(n) | O(w) queue; C reserves 1024 pointer slots |
| Height and diameter | O(n) | O(h) recursion |
| BST insert/search/delete | O(h), worst O(n) | O(1), iterative |
| BST inorder | O(n) | O(h), explicit stack in Python/Java, recursion in C |
| C BST release | O(n) | O(h) recursion |

Traversals also require O(n) output. BST storage is O(n). For an empty/one-node
tree, constant overhead applies even where h is -1/0. BST time bounds assume
constant-time key comparisons; very large Python integers add comparison cost
dependent on their bit length.

## Demos and tests

From each algorithm directory (substitute the matching algorithm name):

```text
python TreeTraversals.py
javac TreeTraversals.java
java -ea TreeTraversals
cc -std=c99 -Wall -Wextra -pedantic TreeTraversals.c -o TreeTraversals
./TreeTraversals
```

Use the `.exe` filename on Windows; keep C assertions enabled. General-tree
demos use root 1, children 2/3, and children 4/5 under 2:

- DFS: `[1, 2, 4, 5, 3]`, `[4, 2, 5, 1, 3]`, `[4, 5, 2, 3, 1]`.
- Level order: `[1, 2, 3, 4, 5]`.
- Height/diameter: `(2, 3)` (Java/C label the fields).
- BST: insert `5,3,7,2,4,6,8`, then delete `2,7,3,5`; output `[4,6,8]`.

C traversal/BST demos print space-separated values rather than list brackets.
Python tests: `python -m unittest discover -s tests -p test_structures.py`
from the repository root, using the included `tests/_loader.py`.
