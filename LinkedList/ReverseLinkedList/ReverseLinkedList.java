/** Reverse an acyclic singly linked list in place, O(n) time/O(1) space.
 * Null is an empty list. Detect cycles before mutation and reject them with
 * IllegalArgumentException. Values are int; no value arithmetic is performed.
 */
public class ReverseLinkedList {
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

    public static Node reverseList(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) throw new IllegalArgumentException("cyclic input");
        }
        Node previous = null, current = head;
        while (current != null) {
            Node following = current.next;
            current.next = previous;
            previous = current;
            current = following;
        }
        return previous;
    }

    public static void main(String[] args) {
        Node first = new Node(1, new Node(2, new Node(3)));
        Node last = first.next.next;
        Node result = reverseList(first);
        assert result == last && result.value == 3 && result.next.value == 2;
        assert result.next.next == first && first.next == null;
        assert reverseList(null) == null;
        Node single = new Node(7);
        assert reverseList(single) == single && single.next == null;
        Node cycle = new Node(9);
        cycle.next = cycle;
        boolean rejected = false;
        try {
            reverseList(cycle);
        } catch (IllegalArgumentException expected) {
            rejected = true;
        }
        assert rejected && cycle.next == cycle;
        cycle.next = null;
        System.out.println("Reversed: " + result.value + " " + result.next.value
                + " " + result.next.next.value);
    }
}
