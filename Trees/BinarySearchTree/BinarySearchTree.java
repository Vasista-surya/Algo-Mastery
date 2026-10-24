import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;

/** Unbalanced int BST with set semantics; duplicates are ignored.
 * insert/search/delete: O(h) time, O(1) auxiliary space; h can be n.
 * inorder: O(n) time, O(h) stack plus O(n) output. Tree storage O(n).
 * Empty search/delete return false; empty inorder returns an empty list.
 */
public class BinarySearchTree {
    private static final class Node {
        int value;
        Node left, right;
        Node(int value) { this.value = value; }
    }
    private Node root;

    public boolean insert(int value) {
        if (root == null) { root = new Node(value); return true; }
        Node node = root;
        while (true) {
            if (value == node.value) return false;
            if (value < node.value) {
                if (node.left == null) { node.left = new Node(value); return true; }
                node = node.left;
            } else {
                if (node.right == null) { node.right = new Node(value); return true; }
                node = node.right;
            }
        }
    }

    public boolean search(int value) {
        Node node = root;
        while (node != null) {
            if (value == node.value) return true;
            node = value < node.value ? node.left : node.right;
        }
        return false;
    }

    public boolean delete(int value) {
        Node parent = null, node = root;
        while (node != null && node.value != value) {
            parent = node;
            node = value < node.value ? node.left : node.right;
        }
        if (node == null) return false;
        if (node.left != null && node.right != null) {
            Node successorParent = node, successor = node.right;
            while (successor.left != null) {
                successorParent = successor;
                successor = successor.left;
            }
            node.value = successor.value;
            parent = successorParent;
            node = successor;
        }
        Node child = node.left != null ? node.left : node.right;
        if (parent == null) root = child;
        else if (parent.left == node) parent.left = child;
        else parent.right = child;
        return true;
    }

    public List<Integer> inorder() {
        List<Integer> result = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.left; }
            node = stack.pop();
            result.add(node.value);
            node = node.right;
        }
        return result;
    }

    public static void main(String[] args) {
        BinarySearchTree tree = new BinarySearchTree();
        assert !tree.search(5) && !tree.delete(5) && tree.inorder().isEmpty();
        for (int value : new int[]{5, 3, 7, 2, 4, 6, 8}) {
            boolean inserted = tree.insert(value);
            assert inserted;
        }
        boolean duplicate = tree.insert(5);
        assert !duplicate && tree.search(6);
        for (int value : new int[]{2, 7, 3, 5}) {
            boolean deleted = tree.delete(value);
            assert deleted && !tree.search(value);
        }
        List<Integer> result = tree.inorder();
        assert result.equals(Arrays.asList(4, 6, 8));
        System.out.println(result);
    }
}
