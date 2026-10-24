/* Stable in-place merge: O(n+m) time including validation, O(1) extra space.
 * Inputs must be acyclic, nondecreasing and disjoint, with live Node/NULL links.
 * Validate before mutation. Return 1 success (NULL output for two empty lists),
 * 0 invalid input/output pointer; on failure links and *out stay unchanged.
 * Reuses caller-owned nodes, allocates nothing; compares int32_t without sums.
 */
#include <assert.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

typedef struct Node {
    int32_t value;
    struct Node *next;
} Node;

static int validate_list(Node *head, Node **tail) {
    const Node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return 0;
    }
    *tail = NULL;
    for (Node *current = head; current != NULL; current = current->next) {
        if (current->next != NULL && current->value > current->next->value) return 0;
        *tail = current;
    }
    return 1;
}

int merge_sorted_lists(Node *first, Node *second, Node **out) {
    if (out == NULL) return 0;
    Node *first_tail = NULL, *second_tail = NULL;
    if (!validate_list(first, &first_tail) || !validate_list(second, &second_tail)) return 0;
    if (first_tail != NULL && first_tail == second_tail) return 0;
    Node dummy = {0, NULL};
    Node *tail = &dummy;
    while (first != NULL && second != NULL) {
        if (first->value <= second->value) {
            tail->next = first;
            first = first->next;
        } else {
            tail->next = second;
            second = second->next;
        }
        tail = tail->next;
    }
    tail->next = first != NULL ? first : second;
    *out = dummy.next;
    return 1;
}

int main(void) {
    /* Stack-owned nodes, so no heap allocation or free is needed. */
    Node a_tail = {3, NULL}, a = {1, &a_tail};
    Node b_tail = {2, NULL}, b = {1, &b_tail};
    Node *result = NULL;
    int ok = merge_sorted_lists(&a, &b, &result);
    assert(ok && result == &a && a.next == &b && b.next == &b_tail);
    assert(b_tail.next == &a_tail && a_tail.next == NULL);
    if (!ok) return 1;
    printf("Merged:");
    for (Node *node = result; node != NULL; node = node->next) {
        printf(" %" PRId32, node->value);
    }
    putchar('\n');
    assert(merge_sorted_lists(NULL, NULL, &result) && result == NULL);
    Node single = {7, NULL};
    assert(merge_sorted_lists(NULL, &single, &result) && result == &single);
    assert(!merge_sorted_lists(&single, &single, &result) && single.next == NULL);
    Node low = {1, NULL}, unsorted = {2, &low};
    assert(!merge_sorted_lists(&unsorted, NULL, &result) && unsorted.next == &low);
    single.next = &single;
    assert(!merge_sorted_lists(NULL, &single, &result) && single.next == &single);
    single.next = NULL;
    assert(!merge_sorted_lists(NULL, NULL, NULL));
    return 0;
}
