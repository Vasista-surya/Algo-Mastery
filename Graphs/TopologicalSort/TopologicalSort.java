import java.util.*;

/** Kahn's directed topological sort, O(V+E) time/space; vertices [0,n).
 * Includes isolated vertices; empty -> empty. FIFO ties: ascending initial
 * vertices, then input neighbors. Cycles/invalid input throw IllegalArgumentException.
 */
public class TopologicalSort {
    public static final class Edge {
        public final int u, v;
        public Edge(int u, int v) { this.u = u; this.v = v; }
    }

    public static List<Integer> topologicalSort(int n, Edge[] edges) {
        if (n < 0 || edges == null) throw new IllegalArgumentException("invalid graph");
        List<List<Integer>> adjacency = new ArrayList<>();
        for (int v = 0; v < n; v++) adjacency.add(new ArrayList<>());
        int[] indegree = new int[n];
        for (Edge e : edges) {
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n)
                throw new IllegalArgumentException("vertex outside [0,n)");
            adjacency.get(e.u).add(e.v);
            indegree[e.v]++;
        }
        Queue<Integer> queue = new ArrayDeque<>();
        for (int v = 0; v < n; v++) if (indegree[v] == 0) queue.add(v);
        List<Integer> order = new ArrayList<>();
        while (!queue.isEmpty()) {
            int u = queue.remove();
            order.add(u);
            for (int v : adjacency.get(u)) if (--indegree[v] == 0) queue.add(v);
        }
        if (order.size() != n) throw new IllegalArgumentException("directed cycle");
        return order;
    }

    public static void main(String[] args) {
        List<Integer> result = topologicalSort(4, new Edge[] {
            new Edge(0, 2), new Edge(1, 2), new Edge(2, 3)});
        assert result.equals(Arrays.asList(0, 1, 2, 3));
        assert topologicalSort(0, new Edge[0]).isEmpty();
        boolean rejected = false;
        try { topologicalSort(1, new Edge[] {new Edge(0, 0)}); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("Topological order: " + result);
    }
}
