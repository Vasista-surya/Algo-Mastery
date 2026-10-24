/* C99 fixed-capacity int FIFO: O(1) operations/initialization; O(1024) storage.
 * Active capacity is 1..1024. No allocations. Error calls preserve state/output.
 * Initialize before use; do not modify struct fields directly. Full/empty and
 * invalid arguments have distinct statuses. queue_is_empty(NULL) is false.
 */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>

#define QUEUE_MAX_CAPACITY 1024
typedef struct {
    int data[QUEUE_MAX_CAPACITY];
    size_t head, size, capacity;
} CircularQueue;
typedef enum { QUEUE_OK, QUEUE_INVALID, QUEUE_FULL, QUEUE_EMPTY } QueueStatus;

static bool valid_queue(const CircularQueue *queue) {
    return queue && queue->capacity > 0 && queue->capacity <= QUEUE_MAX_CAPACITY
        && queue->head < queue->capacity && queue->size <= queue->capacity;
}

QueueStatus queue_init(CircularQueue *queue, size_t capacity) {
    if (!queue || capacity == 0 || capacity > QUEUE_MAX_CAPACITY) return QUEUE_INVALID;
    queue->head = queue->size = 0;
    queue->capacity = capacity;
    return QUEUE_OK;
}

bool queue_is_empty(const CircularQueue *queue) {
    return valid_queue(queue) && queue->size == 0;
}

QueueStatus queue_enqueue(CircularQueue *queue, int value) {
    size_t tail;
    if (!valid_queue(queue)) return QUEUE_INVALID;
    if (queue->size == queue->capacity) return QUEUE_FULL;
    tail = (queue->head + queue->size) % queue->capacity;
    queue->data[tail] = value;
    ++queue->size;
    return QUEUE_OK;
}

QueueStatus queue_peek(const CircularQueue *queue, int *value) {
    if (!valid_queue(queue) || !value) return QUEUE_INVALID;
    if (queue->size == 0) return QUEUE_EMPTY;
    *value = queue->data[queue->head];
    return QUEUE_OK;
}

QueueStatus queue_dequeue(CircularQueue *queue, int *value) {
    QueueStatus status = queue_peek(queue, value);
    if (status != QUEUE_OK) return status;
    queue->head = (queue->head + 1) % queue->capacity;
    --queue->size;
    return QUEUE_OK;
}

int main(void) {
    CircularQueue queue = {0};
    int value = -1;
    QueueStatus status = queue_init(&queue, 3);
    assert(status == QUEUE_OK && queue_is_empty(&queue));
    for (int i = 1; i <= 3; ++i) {
        status = queue_enqueue(&queue, i * 10);
        assert(status == QUEUE_OK);
    }
    status = queue_enqueue(&queue, 40);
    assert(status == QUEUE_FULL && queue.size == 3);
    status = queue_dequeue(&queue, &value);
    assert(status == QUEUE_OK && value == 10);
    status = queue_enqueue(&queue, 40);
    assert(status == QUEUE_OK);
    for (int expected = 20; expected <= 40; expected += 10) {
        status = queue_dequeue(&queue, &value);
        assert(status == QUEUE_OK && value == expected);
        printf("%d%s", value, expected == 40 ? "\n" : " ");
    }
    assert(queue_is_empty(&queue));
    status = queue_dequeue(&queue, &value);
    assert(status == QUEUE_EMPTY && value == 40);
    status = queue_init(&queue, 0);
    assert(status == QUEUE_INVALID);
    status = queue_init(&queue, QUEUE_MAX_CAPACITY + 1);
    assert(status == QUEUE_INVALID);
    status = queue_init(&queue, 1);
    assert(status == QUEUE_OK);
    status = queue_enqueue(&queue, -1);
    assert(status == QUEUE_OK);
    status = queue_dequeue(&queue, &value);
    assert(status == QUEUE_OK && value == -1 && queue_is_empty(&queue));
    return 0;
}
