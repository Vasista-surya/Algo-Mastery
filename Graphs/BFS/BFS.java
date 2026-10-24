import java.util.*;

/** Directed edge-list BFS; vertices [0,n), both arcs for undirected edges.
 * Only source-reachable vertices, input-neighbor order. O(V+E) time/space.
 * Empty graphs have no source; malformed input throws IllegalArgumentException.
 */
public class BFS {
    public static final class Edge {
        public final int u, v;
        public Edge(int u, int v) { this.u = u; this.v = v; }
    }

    public static List<Integer> bfs(int n, Edge[] edges, int source) {
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
        Queue<Integer> queue = new ArrayDeque<>();
        boolean[] seen = new boolean[n];
        seen[source] = true;
        queue.add(source);
        while (!queue.isEmpty()) {
            int u = queue.remove();
            order.add(u);
            for (int v : adjacency.get(u)) {
                if (!seen[v]) {
                    seen[v] = true;
                    queue.add(v);
                }
            }
        }
        return order;
    }

    public static void main(String[] args) {
        List<Integer> result = bfs(5, new Edge[] {
            new Edge(0, 1), new Edge(0, 2), new Edge(1, 3), new Edge(2, 3)}, 0);
        assert result.equals(Arrays.asList(0, 1, 2, 3));
        assert bfs(2, new Edge[0], 1).equals(Arrays.asList(1));
        boolean rejected = false;
        try { bfs(0, new Edge[0], 0); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("BFS: " + result);
    }
}
