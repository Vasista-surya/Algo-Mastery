/* C99 DFS traversals: O(n) time, O(h) call stack plus caller's O(n) output.
 * Input is an acyclic, unshared tree whose depth fits the call stack; int values
 * may repeat. NULL root is empty. No allocations: caller owns all nodes.
 * Output capacity is in ints. On capacity failure, length counts the valid
 * partial prefix. NULL output is allowed only with capacity zero.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

typedef struct Node { int value; struct Node *left, *right; } Node;
typedef enum { TRAVERSAL_OK, TRAVERSAL_INVALID, TRAVERSAL_CAPACITY } TraversalStatus;

static TraversalStatus emit(int value, int *out, size_t capacity, size_t *length) {
    if (*length == capacity) return TRAVERSAL_CAPACITY;
    out[(*length)++] = value;
    return TRAVERSAL_OK;
}

static TraversalStatus visit(const Node *root, int order, int *out,
                             size_t capacity, size_t *length) {
    TraversalStatus status;
    if (!root) return TRAVERSAL_OK;
    if (order == 0) {
        status = emit(root->value, out, capacity, length);
        if (status != TRAVERSAL_OK) return status;
    }
    status = visit(root->left, order, out, capacity, length);
    if (status != TRAVERSAL_OK) return status;
    if (order == 1) {
        status = emit(root->value, out, capacity, length);
        if (status != TRAVERSAL_OK) return status;
    }
    status = visit(root->right, order, out, capacity, length);
    if (status != TRAVERSAL_OK) return status;
    return order == 2 ? emit(root->value, out, capacity, length) : TRAVERSAL_OK;
}

static TraversalStatus traverse(const Node *root, int order, int *out,
                                size_t capacity, size_t *length) {
    if (!length || (!out && capacity != 0)) return TRAVERSAL_INVALID;
    *length = 0;
    return visit(root, order, out, capacity, length);
}

TraversalStatus preorder(const Node *root, int *out, size_t capacity, size_t *length) {
    return traverse(root, 0, out, capacity, length);
}
TraversalStatus inorder(const Node *root, int *out, size_t capacity, size_t *length) {
    return traverse(root, 1, out, capacity, length);
}
TraversalStatus postorder(const Node *root, int *out, size_t capacity, size_t *length) {
    return traverse(root, 2, out, capacity, length);
}

int main(void) {
    Node four = {4, NULL, NULL}, five = {5, NULL, NULL}, three = {3, NULL, NULL};
    Node two = {2, &four, &five}, root = {1, &two, &three};
    int out[5];
    const int expected[3][5] = {{1, 2, 4, 5, 3}, {4, 2, 5, 1, 3}, {4, 5, 2, 3, 1}};
    TraversalStatus (*functions[])(const Node *, int *, size_t, size_t *) =
        {preorder, inorder, postorder};
    size_t length = 0;
    for (size_t order = 0; order < 3; ++order) {
        TraversalStatus status = functions[order](&root, out, 5, &length);
        assert(status == TRAVERSAL_OK && length == 5);
        for (size_t i = 0; i < length; ++i) {
            assert(out[i] == expected[order][i]);
            printf("%d%s", out[i], i + 1 == length ? "\n" : " ");
        }
        status = functions[order](NULL, NULL, 0, &length);
        assert(status == TRAVERSAL_OK && length == 0);
        status = functions[order](&root, out, 4, &length);
        assert(status == TRAVERSAL_CAPACITY && length == 4);
    }
    return 0;
}
