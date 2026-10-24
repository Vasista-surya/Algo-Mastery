/* In-place reversal: O(n) time, O(1) space, no allocation/value arithmetic.
 * Nodes contain int32_t values and valid live Node/NULL links. NULL *head is
 * empty. Return 1 success, 0 for NULL head pointer or a cycle; on failure all
 * links and *head stay unchanged. Caller retains ownership of every node.
 */
#include <assert.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

typedef struct Node {
    int32_t value;
    struct Node *next;
} Node;

int reverse_list(Node **head) {
    if (head == NULL) return 0;
    const Node *slow = *head, *fast = *head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return 0;
    }
    Node *previous = NULL, *current = *head;
    while (current != NULL) {
        Node *following = current->next;
        current->next = previous;
        previous = current;
        current = following;
    }
    *head = previous;
    return 1;
}

int main(void) {
    /* Stack-owned demo nodes: there are no heap allocations to release. */
    Node third = {3, NULL}, second = {2, &third}, first = {1, &second};
    Node *head = &first;
    int ok = reverse_list(&head);
    assert(ok && head == &third && third.next == &second);
    assert(second.next == &first && first.next == NULL);
    if (!ok) return 1;
    printf("Reversed:");
    for (Node *node = head; node != NULL; node = node->next) {
        printf(" %" PRId32, node->value);
    }
    putchar('\n');
    head = NULL;
    assert(reverse_list(&head) && head == NULL);
    Node single = {7, NULL};
    head = &single;
    assert(reverse_list(&head) && head == &single && single.next == NULL);
    single.next = &single;
    assert(!reverse_list(&head) && head == &single && single.next == &single);
    single.next = NULL;
    assert(!reverse_list(NULL));
    return 0;
}
