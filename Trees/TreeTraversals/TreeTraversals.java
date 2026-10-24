import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** DFS traversals: O(n) time, O(h) call stack plus O(n) result space.
 * Input must be an acyclic tree with no shared children and depth fitting the
 * call stack. null is empty. Values are int; duplicates are allowed.
 */
public class TreeTraversals {
    public static final class Node {
        public final int value;
        public Node left, right;
        public Node(int value) { this(value, null, null); }
        public Node(int value, Node left, Node right) {
            this.value = value; this.left = left; this.right = right;
        }
    }

    private static void visit(Node node, int order, List<Integer> result) {
        if (node == null) return;
        if (order == 0) result.add(node.value);
        visit(node.left, order, result);
        if (order == 1) result.add(node.value);
        visit(node.right, order, result);
        if (order == 2) result.add(node.value);
    }

    private static List<Integer> traverse(Node root, int order) {
        List<Integer> result = new ArrayList<>();
        visit(root, order, result);
        return result;
    }

    public static List<Integer> preorder(Node root) { return traverse(root, 0); }
    public static List<Integer> inorder(Node root) { return traverse(root, 1); }
    public static List<Integer> postorder(Node root) { return traverse(root, 2); }

    public static void main(String[] args) {
        Node root = new Node(1, new Node(2, new Node(4), new Node(5)), new Node(3));
        List<Integer> pre = preorder(root), in = inorder(root), post = postorder(root);
        assert pre.equals(Arrays.asList(1, 2, 4, 5, 3));
        assert in.equals(Arrays.asList(4, 2, 5, 1, 3));
        assert post.equals(Arrays.asList(4, 5, 2, 3, 1));
        assert preorder(null).isEmpty() && inorder(null).isEmpty() && postorder(null).isEmpty();
        assert postorder(new Node(-1)).equals(Arrays.asList(-1));
        System.out.println(pre); System.out.println(in); System.out.println(post);
    }
}
