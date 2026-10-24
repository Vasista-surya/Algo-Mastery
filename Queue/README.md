# Circular queue

`CircularQueue/` contains independent `CircularQueue.py`, `CircularQueue.java`,
and C99 `CircularQueue.c`. Each demonstrates FIFO wraparound without input.

| Operation | Python | Java | C |
| --- | --- | --- | --- |
| Construct/reset | `CircularQueue(capacity)` | `new CircularQueue(capacity)` | `queue_init(&queue, capacity)` |
| Enqueue | `enqueue(value)` | `enqueue(int)` | `queue_enqueue(&queue, value)` |
| Dequeue | `dequeue() -> int` | `dequeue() -> int` | `queue_dequeue(&queue, &value)` |
| Peek | `peek() -> int` | `peek() -> int` | `queue_peek(&queue, &value)` |
| Empty | `is_empty()` | `isEmpty()` | `queue_is_empty(&queue)` |
| Size | `len(queue)` | `size()` | `queue.size` (read-only) |

All operations are **O(1)**. Python/Java construction and storage are
O(capacity). C initialization is O(1) and the struct reserves 1024 integer
slots, regardless of active capacity. There are no C allocations to release.
The circular array reuses dequeued slots; full queues never overwrite values.
Duplicates and negative integers are allowed. Python accepts arbitrary-size
`int` values, excluding `bool`; Java/C values fit their native `int` range.

Capacity must be positive. Python raises `TypeError` for non-integer capacity
or value, `ValueError` for nonpositive capacity, `OverflowError` when full,
and `IndexError` for empty dequeue/peek. Java uses `IllegalArgumentException`,
`IllegalStateException`, and `NoSuchElementException`, respectively.

C accepts active capacities 1..`QUEUE_MAX_CAPACITY` (1024), and returns
`QUEUE_OK`, `QUEUE_INVALID`, `QUEUE_FULL`, or `QUEUE_EMPTY`. Initialize the struct
before use; do not change its fields directly. NULL queue/output pointers are
invalid, and `queue_is_empty(NULL)` returns false. Failed calls leave the queue
and output unchanged. Output pointers must refer to caller-owned variables,
not fields inside the queue. An initialized empty queue reports true; empty
peek/dequeue never return an ambiguous sentinel value.

## Demos and tests

From `Queue/CircularQueue`:

```text
python CircularQueue.py
javac CircularQueue.java
java -ea CircularQueue
cc -std=c99 -Wall -Wextra -pedantic CircularQueue.c -o CircularQueue
./CircularQueue
```

Use the executable's `.exe` name on Windows; keep C assertions enabled. Demos
enqueue 10, 20, 30, remove 10, and enqueue 40 into the recycled slot. Output is
`[20, 30, 40]` in Python/Java and `20 30 40` in C. Assertions cover full/empty
behavior and wraparound. Python imports are silent and reusable.

From the repository root, Python tests use
`python -m unittest discover -s tests -p test_structures.py`, with the
shared `tests/_loader.py` available in the repository.
