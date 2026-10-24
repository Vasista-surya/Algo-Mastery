import java.util.*;

/** Iterative directed DFS preorder; vertices [0,n), both arcs for undirected.
 * Source component only; input-neighbor order. O(V+E) time/space, no recursion.
 * Invalid vertices/source (including empty source) throw IllegalArgumentException.
 */
public class DFS {
    public static final class Edge {
        public final int u, v;
        public Edge(int u, int v) { this.u = u; this.v = v; }
    }

    public static List<Integer> dfs(int n, Edge[] edges, int source) {
        if (n < 0 || source < 0 || source >= n || edges == null)
            throw new IllegalArgumentException("invalid graph/source");
        List<List<Integer>> adjacency = new ArrayList<>();
        for (int v = 0; v < n; v++) adjacency.add(new ArrayList<>());
        for (Edge e : edges) {
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n)
                throw new IllegalArgumentException("vertex outside [0,n)");
            adjacency.get(e.u).add(e.v);
        }
        List<Integer> order = new ArrayList<>();
        Deque<Integer> stack = new ArrayDeque<>();
        boolean[] seen = new boolean[n];
        int[] next = new int[n];
        seen[source] = true;
        order.add(source);
        stack.push(source);
        while (!stack.isEmpty()) {
            int u = stack.peek();
            if (next[u] == adjacency.get(u).size()) {
                stack.pop();
            } else {
                int v = adjacency.get(u).get(next[u]++);
                if (!seen[v]) {
                    seen[v] = true;
                    order.add(v);
                    stack.push(v);
                }
            }
        }
        return order;
    }

    public static void main(String[] args) {
        List<Integer> result = dfs(5, new Edge[] {
            new Edge(0, 1), new Edge(0, 2), new Edge(1, 3), new Edge(3, 0)}, 0);
        assert result.equals(Arrays.asList(0, 1, 3, 2));
        assert dfs(2, new Edge[0], 1).equals(Arrays.asList(1));
        boolean rejected = false;
        try { dfs(2, new Edge[] {new Edge(1, 2)}, 0); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("DFS: " + result);
    }
}
