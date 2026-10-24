/** Compute height and diameter in one postorder pass: O(n) time, O(h) stack.
 * Both count EDGES: null height -1, leaf height 0, null/leaf diameter 0.
 * Input must be an acyclic unshared tree with depth fitting the call stack.
 * Duplicate values are allowed. Metrics exceeding Integer.MAX_VALUE are errors.
 */
public class HeightAndDiameter {
    public static final class Node {
        public final int value;
        public Node left, right;
        public Node(int value) { this(value, null, null); }
        public Node(int value, Node left, Node right) {
            this.value = value; this.left = left; this.right = right;
        }
    }

    public static final class Metrics {
        public final int height, diameter;
        private Metrics(int height, int diameter) {
            this.height = height; this.diameter = diameter;
        }
    }

    public static Metrics heightAndDiameter(Node root) {
        if (root == null) return new Metrics(-1, 0);
        Metrics left = heightAndDiameter(root.left), right = heightAndDiameter(root.right);
        long height = 1L + Math.max(left.height, right.height);
        long diameter = Math.max(Math.max(left.diameter, right.diameter),
                                 (long) left.height + right.height + 2);
        if (height > Integer.MAX_VALUE || diameter > Integer.MAX_VALUE)
            throw new ArithmeticException("tree metrics exceed int range");
        return new Metrics((int) height, (int) diameter);
    }

    public static void main(String[] args) {
        Node root = new Node(1, new Node(2, new Node(4), new Node(5)), new Node(3));
        Metrics result = heightAndDiameter(root);
        assert result.height == 2 && result.diameter == 3;
        Metrics empty = heightAndDiameter(null), leaf = heightAndDiameter(new Node(1));
        assert empty.height == -1 && empty.diameter == 0;
        assert leaf.height == 0 && leaf.diameter == 0;
        Node branch = new Node(2, new Node(3, new Node(4), null),
                               new Node(5, null, new Node(6)));
        Metrics offRoot = heightAndDiameter(new Node(1, branch, null));
        assert offRoot.height == 3 && offRoot.diameter == 4;
        System.out.println("height=" + result.height + ", diameter=" + result.diameter);
    }
}
