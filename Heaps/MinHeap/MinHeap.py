"""Fixed-capacity binary min-heap, storing integer values (duplicates allowed).

push/pop: O(log n) time, O(1) auxiliary space; peek/is_empty/len: O(1).
Construction/storage: O(capacity). Positive integer capacity is required.
Empty pop/peek raises IndexError; full push raises OverflowError. Non-int
values/capacities (including bool) raise TypeError. Failed calls preserve state.
"""


class MinHeap:
    def __init__(self, capacity):
        if type(capacity) is not int:
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._data = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def push(self, value):
        """Insert value, restoring the heap by sifting upward."""
        if type(value) is not int:
            raise TypeError("value must be an integer")
        if self._size == len(self._data):
            raise OverflowError("heap is full")
        index = self._size
        self._size += 1
        while index > 0:
            parent = (index - 1) // 2
            if self._data[parent] <= value:
                break
            self._data[index] = self._data[parent]
            index = parent
        self._data[index] = value

    def peek(self):
        if self.is_empty():
            raise IndexError("heap is empty")
        return self._data[0]

    def pop(self):
        """Remove the minimum, restoring the heap by sifting downward."""
        minimum = self.peek()
        self._size -= 1
        value = self._data[self._size]
        self._data[self._size] = None
        if self._size:
            index = 0
            while 2 * index + 1 < self._size:
                child = 2 * index + 1
                if child + 1 < self._size and self._data[child + 1] < self._data[child]:
                    child += 1
                if value <= self._data[child]:
                    break
                self._data[index] = self._data[child]
                index = child
            self._data[index] = value
        return minimum


def main():
    heap = MinHeap(5)
    for value in (5, -2, 8, -2, 1):
        heap.push(value)
    assert heap.peek() == -2
    try:
        heap.push(9)
    except OverflowError:
        pass
    else:
        raise AssertionError("full heap accepted an element")
    result = [heap.pop() for _ in range(5)]
    assert result == [-2, -2, 1, 5, 8] and heap.is_empty()
    try:
        heap.pop()
    except IndexError:
        pass
    else:
        raise AssertionError("empty heap returned an element")
    print(result)


if __name__ == "__main__":
    main()
