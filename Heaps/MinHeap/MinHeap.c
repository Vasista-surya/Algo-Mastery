/* C99 fixed-capacity int min-heap; duplicates allowed. push/pop O(log n),
 * peek/is_empty/init O(1). Struct reserves 1024 ints; scratch O(1).
 * Initialize before use; do not alter fields. No allocations. Failed calls
 * preserve heap/output; output pointers must not alias fields in the heap.
 */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <limits.h>
#include <stdio.h>

#define HEAP_MAX_CAPACITY 1024
typedef struct { int data[HEAP_MAX_CAPACITY]; size_t size, capacity; } MinHeap;
typedef enum { HEAP_OK, HEAP_INVALID, HEAP_FULL, HEAP_EMPTY } HeapStatus;

static bool valid_heap(const MinHeap *heap) {
    return heap && heap->capacity > 0 && heap->capacity <= HEAP_MAX_CAPACITY
        && heap->size <= heap->capacity;
}

HeapStatus heap_init(MinHeap *heap, size_t capacity) {
    if (!heap || capacity == 0 || capacity > HEAP_MAX_CAPACITY) return HEAP_INVALID;
    heap->capacity = capacity;
    heap->size = 0;
    return HEAP_OK;
}

bool heap_is_empty(const MinHeap *heap) {
    return valid_heap(heap) && heap->size == 0;
}

HeapStatus heap_push(MinHeap *heap, int value) {
    size_t index;
    if (!valid_heap(heap)) return HEAP_INVALID;
    if (heap->size == heap->capacity) return HEAP_FULL;
    index = heap->size++;
    while (index > 0) {
        size_t parent = (index - 1) / 2;
        if (heap->data[parent] <= value) break;
        heap->data[index] = heap->data[parent];
        index = parent;
    }
    heap->data[index] = value;
    return HEAP_OK;
}

HeapStatus heap_peek(const MinHeap *heap, int *value) {
    if (!valid_heap(heap) || !value) return HEAP_INVALID;
    if (heap->size == 0) return HEAP_EMPTY;
    *value = heap->data[0];
    return HEAP_OK;
}

HeapStatus heap_pop(MinHeap *heap, int *value) {
    int last;
    HeapStatus status = heap_peek(heap, value);
    if (status != HEAP_OK) return status;
    last = heap->data[--heap->size];
    if (heap->size > 0) {
        size_t index = 0;
        while (index < heap->size / 2) {
            size_t child = 2 * index + 1;
            if (child + 1 < heap->size && heap->data[child + 1] < heap->data[child]) ++child;
            if (last <= heap->data[child]) break;
            heap->data[index] = heap->data[child];
            index = child;
        }
        heap->data[index] = last;
    }
    return HEAP_OK;
}

int main(void) {
    MinHeap heap = {0};
    const int input[] = {5, -2, 8, -2, 1}, expected[] = {-2, -2, 1, 5, 8};
    int value = 0;
    HeapStatus status = heap_init(&heap, 5);
    assert(status == HEAP_OK && heap_is_empty(&heap));
    for (size_t i = 0; i < 5; ++i) {
        status = heap_push(&heap, input[i]);
        assert(status == HEAP_OK);
    }
    status = heap_push(&heap, 9);
    assert(status == HEAP_FULL && heap.size == 5);
    status = heap_peek(&heap, &value);
    assert(status == HEAP_OK && value == -2);
    for (size_t i = 0; i < 5; ++i) {
        status = heap_pop(&heap, &value);
        assert(status == HEAP_OK && value == expected[i]);
        printf("%d%s", value, i == 4 ? "\n" : " ");
    }
    assert(heap_is_empty(&heap));
    status = heap_pop(&heap, &value);
    assert(status == HEAP_EMPTY && value == 8);
    status = heap_init(&heap, 0);
    assert(status == HEAP_INVALID);
    status = heap_init(&heap, HEAP_MAX_CAPACITY + 1);
    assert(status == HEAP_INVALID);
    status = heap_init(&heap, 1);
    assert(status == HEAP_OK);
    status = heap_push(&heap, INT_MIN);
    assert(status == HEAP_OK);
    status = heap_pop(&heap, &value);
    assert(status == HEAP_OK && value == INT_MIN && heap_is_empty(&heap));
    return 0;
}
