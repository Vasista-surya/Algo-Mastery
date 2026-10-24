/* C99 breadth-first traversal: O(n) time, O(w) live queue + O(n) output.
 * The fixed queue holds at most 1024 pending nodes (possibly from two levels).
 * Input must be an acyclic, unshared tree. NULL root is empty; duplicates okay.
 * Caller owns nodes and output. No allocations. On capacity failure, length
 * counts the valid output prefix. NULL output is valid only at capacity zero.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

#define LEVEL_QUEUE_CAPACITY 1024
typedef struct Node { int value; struct Node *left, *right; } Node;
typedef enum { LEVEL_OK, LEVEL_INVALID, LEVEL_CAPACITY } LevelStatus;

LevelStatus level_order(const Node *root, int *out, size_t capacity, size_t *length) {
    const Node *queue[LEVEL_QUEUE_CAPACITY];
    size_t head = 0, count = 0;
    if (!length || (!out && capacity != 0)) return LEVEL_INVALID;
    *length = 0;
    if (!root) return LEVEL_OK;
    queue[count++] = root;
    while (count) {
        const Node *node = queue[head];
        const Node *children[2] = {node->left, node->right};
        head = (head + 1) % LEVEL_QUEUE_CAPACITY;
        --count;
        if (*length == capacity) return LEVEL_CAPACITY;
        out[(*length)++] = node->value;
        for (size_t i = 0; i < 2; ++i) {
            if (!children[i]) continue;
            if (count == LEVEL_QUEUE_CAPACITY) return LEVEL_CAPACITY;
            queue[(head + count) % LEVEL_QUEUE_CAPACITY] = children[i];
            ++count;
        }
    }
    return LEVEL_OK;
}

int main(void) {
    Node four = {4, NULL, NULL}, five = {5, NULL, NULL}, three = {3, NULL, NULL};
    Node two = {2, &four, &five}, root = {1, &two, &three};
    int out[5];
    size_t length;
    LevelStatus status = level_order(&root, out, 5, &length);
    assert(status == LEVEL_OK && length == 5);
    for (size_t i = 0; i < length; ++i) {
        assert(out[i] == (int)i + 1);
        printf("%d%s", out[i], i + 1 == length ? "\n" : " ");
    }
    status = level_order(NULL, NULL, 0, &length);
    assert(status == LEVEL_OK && length == 0);
    status = level_order(&root, out, 4, &length);
    assert(status == LEVEL_CAPACITY && length == 4);
    status = level_order(&root, NULL, 1, &length);
    assert(status == LEVEL_INVALID);
    /* A complete 2049-node tree requires a pending queue of 1025 nodes. */
    {
        Node wide[2 * LEVEL_QUEUE_CAPACITY + 1];
        int values[2 * LEVEL_QUEUE_CAPACITY + 1];
        size_t nodes = sizeof wide / sizeof wide[0];
        for (size_t i = 0; i < nodes; ++i) {
            wide[i].value = (int)i;
            wide[i].left = 2 * i + 1 < nodes ? &wide[2 * i + 1] : NULL;
            wide[i].right = 2 * i + 2 < nodes ? &wide[2 * i + 2] : NULL;
        }
        status = level_order(wide, values, nodes, &length);
        assert(status == LEVEL_CAPACITY);
        wide[LEVEL_QUEUE_CAPACITY - 1].left = NULL;
        wide[LEVEL_QUEUE_CAPACITY - 1].right = NULL;
        status = level_order(wide, values, nodes - 2, &length);
        assert(status == LEVEL_OK && length == nodes - 2);
        for (size_t i = 0; i < length; ++i) assert(values[i] == (int)i);
    }
    return 0;
}
