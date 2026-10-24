# Binary min-heap

`MinHeap/MinHeap.py`, `MinHeap.java`, and C99 `MinHeap.c` independently implement
a fixed-capacity binary min-heap. Every parent is <= its children; pushing sifts
up and popping the minimum sifts the last value down. Duplicates are retained.

| Operation | Python | Java | C |
| --- | --- | --- | --- |
| Construct/reset | `MinHeap(capacity)` | `new MinHeap(capacity)` | `heap_init(&heap, capacity)` |
| Insert | `push(value)` | `push(int)` | `heap_push(&heap, value)` |
| Remove minimum | `pop() -> int` | `pop() -> int` | `heap_pop(&heap, &value)` |
| Minimum | `peek() -> int` | `peek() -> int` | `heap_peek(&heap, &value)` |
| Empty | `is_empty()` | `isEmpty()` | `heap_is_empty(&heap)` |
| Size | `len(heap)` | `size()` | `heap.size` (read-only) |

`push`/`pop` are **O(log n)** time (O(1) for n <= 1) and O(1) auxiliary space;
peek, empty, and size queries are O(1). Python/Java construction and storage are
O(capacity). C initialization is O(1); its struct reserves 1024 integer slots.
These time bounds assume constant-time key comparisons; very large Python
integers add comparison cost dependent on their bit length. The implementation
teaches insertion/removal rather than bulk heapify.

## Constraints and errors

- Capacity must be positive. Python requires `int` capacity and values,
  excluding `bool`; values may be arbitrary-size and negative. Java/C store
  native `int` values. Comparisons do not subtract keys, so extreme values work.
- Python: bad types raise `TypeError`, nonpositive capacity raises `ValueError`,
  full push raises `OverflowError`, empty peek/pop raises `IndexError`.
- Java: invalid capacity raises `IllegalArgumentException`, full push raises
  `IllegalStateException`, empty peek/pop raises `NoSuchElementException`.
- C active capacity must be 1..`HEAP_MAX_CAPACITY` (1024). Functions return
  `HEAP_OK`, `HEAP_INVALID`, `HEAP_FULL`, or `HEAP_EMPTY`; NULL heap/output
  arguments are invalid. `heap_is_empty(NULL)` returns false. Initialize before
  use, and do not edit struct fields. Output pointers must refer to caller-owned
  variables, not heap fields. No dynamic allocations need releasing.
- Failed operations preserve heap and output. Empty results are errors rather
  than sentinel values, so every integer remains a valid element.

## Demos and tests

From `Heaps/MinHeap`:

```text
python MinHeap.py
javac MinHeap.java
java -ea MinHeap
cc -std=c99 -Wall -Wextra -pedantic MinHeap.c -o MinHeap
./MinHeap
```

Use the `.exe` filename on Windows and keep C assertions enabled. All demos
insert `5, -2, 8, -2, 1`, verify full/empty handling, and print sorted removals:
`[-2, -2, 1, 5, 8]` (space-separated without brackets in C). Python imports are
silent; Java helpers stay within the matching public class.

Python tests use `python -m unittest discover -s tests -p test_structures.py`
from the root, using the included `tests/_loader.py`.
