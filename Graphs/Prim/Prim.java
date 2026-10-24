import java.util.*;

/** Dense-selection Prim minimum spanning FOREST, O(V^2+E) time, O(V+E) space.
 * Undirected edges, vertices [0,n), n<=10000, weights [-10^9,10^9].
 * Supply each edge once. Loops ignored, parallel/negative edges allowed.
 * Restart at smallest unvisited vertex; empty/disconnected valid.
 * Ties by vertex, then parent; endpoints normalized. Input not modified.
 * Invalid input throws IllegalArgumentException; totals use checked long sums.
 */
public class Prim {
    public static final int MAX_VERTICES = 10000;
    public static final class Edge {
        public final int u, v;
        public final long weight;
        public Edge(int u, int v, long weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
        public String toString() { return "(" + u + "," + v + "," + weight + ")"; }
    }
    public static final class Result {
        public final List<Edge> edges;
        public final long total;
        private Result(List<Edge> edges, long total) {
            this.edges = Collections.unmodifiableList(edges); this.total = total;
        }
    }

    public static Result prim(int n, Edge[] edges) {
        if (n < 0 || n > MAX_VERTICES || edges == null)
            throw new IllegalArgumentException("invalid graph");
        List<List<Edge>> adjacency = new ArrayList<>();
        for (int v = 0; v < n; v++) adjacency.add(new ArrayList<>());
        for (Edge e : edges) {
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
                e.weight < -1_000_000_000L || e.weight > 1_000_000_000L)
                throw new IllegalArgumentException("invalid vertex/weight");
            adjacency.get(e.u).add(e);
            adjacency.get(e.v).add(new Edge(e.v, e.u, e.weight));
        }
        long[] key = new long[n];
        Arrays.fill(key, Long.MAX_VALUE);
        int[] parent = new int[n];
        Arrays.fill(parent, -1);
        boolean[] used = new boolean[n];
        List<Edge> forest = new ArrayList<>();
        long total = 0;
        for (int step = 0; step < n; step++) {
            int u = -1;
            for (int v = 0; v < n; v++)
                if (!used[v] && (u == -1 || key[v] < key[u])) u = v;
            used[u] = true;
            if (parent[u] != -1) {
                forest.add(new Edge(Math.min(u, parent[u]), Math.max(u, parent[u]), key[u]));
                total = Math.addExact(total, key[u]);
            }
            for (Edge e : adjacency.get(u))
                if (!used[e.v] && (e.weight < key[e.v] ||
                    (e.weight == key[e.v] && u < parent[e.v]))) {
                    key[e.v] = e.weight;
                    parent[e.v] = u;
                }
        }
        return new Result(forest, total);
    }

    public static void main(String[] args) {
        Result result = prim(5, new Edge[] {new Edge(0, 1, 4), new Edge(0, 2, 1),
            new Edge(1, 2, 2), new Edge(3, 4, -1)});
        assert result.total == 2 && result.edges.size() == 3;
        assert prim(0, new Edge[0]).edges.isEmpty();
        assert prim(1, new Edge[] {new Edge(0, 0, -9)}).total == 0;
        System.out.println("Forest: " + result.edges + "; total: " + result.total);
    }
}
