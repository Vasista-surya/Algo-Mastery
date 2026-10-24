"""Fixed-capacity integer FIFO backed by a circular array.

enqueue/dequeue/peek/is_empty/len: O(1); construction/storage O(capacity).
Capacity must be a positive int; values must be ints (bool is rejected).
OverflowError signals full, IndexError signals empty. Failed calls preserve state.
"""


class CircularQueue:
    def __init__(self, capacity):
        if type(capacity) is not int:
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._data = [None] * capacity
        self._head = 0
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def enqueue(self, value):
        """Append value; raise OverflowError rather than overwrite a full queue."""
        if type(value) is not int:
            raise TypeError("value must be an integer")
        if self._size == len(self._data):
            raise OverflowError("queue is full")
        tail = (self._head + self._size) % len(self._data)
        self._data[tail] = value
        self._size += 1

    def peek(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self._data[self._head]

    def dequeue(self):
        value = self.peek()
        self._data[self._head] = None
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return value


def main():
    queue = CircularQueue(3)
    assert queue.is_empty()
    for value in (10, 20, 30):
        queue.enqueue(value)
    try:
        queue.enqueue(40)
    except OverflowError:
        pass
    else:
        raise AssertionError("full queue accepted an element")
    first = queue.dequeue()
    assert first == 10
    queue.enqueue(40)
    result = [queue.dequeue() for _ in range(3)]
    assert result == [20, 30, 40] and queue.is_empty()
    try:
        queue.peek()
    except IndexError:
        pass
    else:
        raise AssertionError("empty queue returned an element")
    print(result)


if __name__ == "__main__":
    main()
