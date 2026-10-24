/** Floyd cycle detection: O(n) time/O(1) space, no link mutations.
 * n counts distinct reachable nodes. Null is empty. Node values are int and
 * are never used for arithmetic or equality tests between nodes.
 */
public class CycleDetection {
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

    public static boolean hasCycle(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        Node first = new Node(1, new Node(2, new Node(3)));
        assert !hasCycle(first);
        assert !hasCycle(null);
        first.next.next.next = first.next;
        assert hasCycle(first);
        System.out.println("Cycle detected: " + hasCycle(first));
        first.next.next.next = null;
        Node single = new Node(1);
        assert !hasCycle(single);
        single.next = single;
        assert hasCycle(single);
        single.next = null;
    }
}
