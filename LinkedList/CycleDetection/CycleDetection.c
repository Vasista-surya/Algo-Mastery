/* Floyd cycle detection: O(n) time/O(1) space; n distinct reachable nodes.
 * Return 1 for a cycle, 0 otherwise. NULL is empty. Require valid live nodes
 * and Node/NULL links. int32_t values are not compared or added; no size
 * counter can overflow. No allocations or mutations; caller owns all nodes.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>

typedef struct Node {
    int32_t value;
    struct Node *next;
} Node;

int has_cycle(const Node *head) {
    const Node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return 1;
    }
    return 0;
}

int main(void) {
    /* Stack-owned nodes need no free; cycle links are restored before return. */
    Node third = {3, NULL}, second = {2, &third}, first = {1, &second};
    assert(!has_cycle(&first));
    assert(!has_cycle(NULL));
    third.next = &second;
    assert(has_cycle(&first));
    printf("Cycle detected: %d\n", has_cycle(&first));
    third.next = NULL;
    Node single = {1, NULL};
    assert(!has_cycle(&single));
    single.next = &single;
    assert(has_cycle(&single));
    single.next = NULL;
    return 0;
}
