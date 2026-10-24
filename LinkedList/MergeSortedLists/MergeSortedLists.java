/** Stable in-place merge: O(n+m) time including validation, O(1) extra space.
 * Require acyclic, nondecreasing, disjoint lists; validate before mutation.
 * Null is empty. Values are int and are compared without subtraction.
 * Equal values take first-list nodes first; successful merge reuses all nodes.
 */
public class MergeSortedLists {
    public static final class Node {
        public final int value;
        public Node next;

        public Node(int value) {
            this(value, null);
        }

        public Node(int value, Node next) {
            this.value = value;
            this.next = next;
        }
    }

    private static Node validateList(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) throw new IllegalArgumentException("cyclic input");
        }
        Node tail = null;
        for (Node current = head; current != null; current = current.next) {
            if (current.next != null && current.value > current.next.value) {
                throw new IllegalArgumentException("lists must be nondecreasing");
            }
            tail = current;
        }
        return tail;
    }

    public static Node mergeSortedLists(Node first, Node second) {
        Node firstTail = validateList(first), secondTail = validateList(second);
        if (firstTail != null && firstTail == secondTail) {
            throw new IllegalArgumentException("lists must not share nodes");
        }
        Node dummy = new Node(0), tail = dummy;
        while (first != null && second != null) {
            if (first.value <= second.value) {
                tail.next = first;
                first = first.next;
            } else {
                tail.next = second;
                second = second.next;
            }
            tail = tail.next;
        }
        tail.next = first != null ? first : second;
        return dummy.next;
    }

    public static void main(String[] args) {
        Node first = new Node(1, new Node(3));
        Node second = new Node(1, new Node(2));
        Node firstTail = first.next;
        Node result = mergeSortedLists(first, second);
        assert result == first && result.next == second;
        assert result.next.next.value == 2 && result.next.next.next == firstTail;
        assert firstTail.next == null;
        assert mergeSortedLists(null, null) == null;
        Node single = new Node(7);
        assert mergeSortedLists(null, single) == single;
        boolean rejected = false;
        try {
            mergeSortedLists(single, single);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected && single.next == null;
        Node unsorted = new Node(2, new Node(1));
        rejected = false;
        try {
            mergeSortedLists(unsorted, null);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected && unsorted.next.value == 1;
        single.next = single;
        rejected = false;
        try {
            mergeSortedLists(null, single);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected && single.next == single;
        single.next = null;
        System.out.println("Merged: " + result.value + " " + result.next.value
                + " " + result.next.next.value + " " + result.next.next.next.value);
    }
}
