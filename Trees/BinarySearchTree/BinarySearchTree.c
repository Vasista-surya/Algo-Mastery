/* C99 unbalanced int BST with set semantics: duplicates are ignored.
 * insert/search/delete: O(h) time, O(1) auxiliary space; worst h=O(n).
 * inorder/free: O(n) time, O(h) recursion stack (depth must fit call stack).
 * Storage O(n). Initialize root to NULL; use these functions to preserve order
 * and ownership. Delete frees its node; bst_free frees all remaining nodes.
 * Insertion allocation failure preserves the tree. Output arrays are bounded.
 */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int value; struct Node *left, *right; } Node;
typedef enum {
    BST_OK, BST_INVALID, BST_DUPLICATE, BST_NOT_FOUND, BST_NOMEM, BST_CAPACITY
} BSTStatus;

BSTStatus bst_insert(Node **root, int value) {
    Node *node;
    if (!root) return BST_INVALID;
    while (*root) {
        if (value == (*root)->value) return BST_DUPLICATE;
        root = value < (*root)->value ? &(*root)->left : &(*root)->right;
    }
    node = malloc(sizeof *node);
    if (!node) return BST_NOMEM;
    node->value = value;
    node->left = node->right = NULL;
    *root = node;
    return BST_OK;
}

bool bst_search(const Node *root, int value) {
    while (root) {
        if (value == root->value) return true;
        root = value < root->value ? root->left : root->right;
    }
    return false;
}

BSTStatus bst_delete(Node **root, int value) {
    Node *victim;
    if (!root) return BST_INVALID;
    while (*root && (*root)->value != value)
        root = value < (*root)->value ? &(*root)->left : &(*root)->right;
    if (!*root) return BST_NOT_FOUND;
    victim = *root;
    if (victim->left && victim->right) {
        Node **successor = &victim->right;
        while ((*successor)->left) successor = &(*successor)->left;
        victim->value = (*successor)->value;
        root = successor;
        victim = *root;
    }
    *root = victim->left ? victim->left : victim->right;
    free(victim);
    return BST_OK;
}

static BSTStatus visit(const Node *root, int *out, size_t capacity, size_t *length) {
    BSTStatus status;
    if (!root) return BST_OK;
    status = visit(root->left, out, capacity, length);
    if (status != BST_OK) return status;
    if (*length == capacity) return BST_CAPACITY;
    out[(*length)++] = root->value;
    return visit(root->right, out, capacity, length);
}

/* On capacity failure, length counts the valid sorted prefix. */
BSTStatus bst_inorder(const Node *root, int *out, size_t capacity, size_t *length) {
    if (!length || (!out && capacity != 0)) return BST_INVALID;
    *length = 0;
    return visit(root, out, capacity, length);
}

void bst_free(Node **root) {
    if (!root || !*root) return;
    bst_free(&(*root)->left);
    bst_free(&(*root)->right);
    free(*root);
    *root = NULL;
}

int main(void) {
    Node *root = NULL;
    const int values[] = {5, 3, 7, 2, 4, 6, 8};
    const int removed[] = {2, 7, 3, 5}, expected[] = {4, 6, 8};
    int out[7];
    size_t length;
    BSTStatus status = bst_delete(&root, 5);
    assert(status == BST_NOT_FOUND && !bst_search(root, 5));
    status = bst_inorder(root, NULL, 0, &length);
    assert(status == BST_OK && length == 0);
    for (size_t i = 0; i < sizeof values / sizeof values[0]; ++i) {
        status = bst_insert(&root, values[i]);
        if (status != BST_OK) {
            bst_free(&root);
            fputs("BST allocation failed\n", stderr);
            return EXIT_FAILURE;
        }
        assert(bst_search(root, values[i]));
    }
    status = bst_insert(&root, 5);
    assert(status == BST_DUPLICATE);
    for (size_t i = 0; i < sizeof removed / sizeof removed[0]; ++i) {
        status = bst_delete(&root, removed[i]);
        assert(status == BST_OK && !bst_search(root, removed[i]));
    }
    status = bst_inorder(root, out, 7, &length);
    assert(status == BST_OK && length == 3);
    for (size_t i = 0; i < length; ++i) {
        assert(out[i] == expected[i]);
        printf("%d%s", out[i], i + 1 == length ? "\n" : " ");
    }
    status = bst_inorder(root, out, 2, &length);
    assert(status == BST_CAPACITY && length == 2);
    bst_free(&root);
    assert(root == NULL);
    bst_free(&root); /* Repeated release is safe. */
    return 0;
}
