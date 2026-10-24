import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;

/** Breadth-first traversal: O(n) time, O(w) queue plus O(n) output.
 * Input must be an acyclic tree without shared children. null is empty;
 * duplicate int values are allowed. w denotes maximum tree width.
 */
public class LevelOrderTraversal {
    public static final class Node {
        public final int value;
        public Node left, right;
        public Node(int value) { this(value, null, null); }
        public Node(int value, Node left, Node right) {
            this.value = value; this.left = left; this.right = right;
        }
    }

    /** Return a flat list, each level left to right; null returns an empty list. */
    public static List<Integer> levelOrder(Node root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        Deque<Node> queue = new ArrayDeque<>();
        queue.addLast(root);
        while (!queue.isEmpty()) {
            Node node = queue.removeFirst();
            result.add(node.value);
            if (node.left != null) queue.addLast(node.left);
            if (node.right != null) queue.addLast(node.right);
        }
        return result;
    }

    public static void main(String[] args) {
        Node root = new Node(1, new Node(2, new Node(4), new Node(5)), new Node(3));
        List<Integer> result = levelOrder(root);
        assert result.equals(Arrays.asList(1, 2, 3, 4, 5));
        assert levelOrder(null).isEmpty();
        assert levelOrder(new Node(-1)).equals(Arrays.asList(-1));
        assert levelOrder(new Node(1, null, new Node(2, new Node(3), null)))
            .equals(Arrays.asList(1, 2, 3));
        System.out.println(result);
    }
}
