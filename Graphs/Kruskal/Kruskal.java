import java.util.*;

/** Undirected minimum spanning FOREST, O(V+E log E) time, O(V+E) space.
 * Vertices [0,n), n<=10000; weights [-10^9,10^9]. One entry per undirected
 * edge; loops ignored, parallel edges allowed. Empty/disconnected valid.
 * Endpoints normalized; ties by (weight,u,v). Input not modified.
 * Invalid input throws IllegalArgumentException; totals use checked long sums.
 */
public class Kruskal {
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
    private static int root(int[] parent, int v) {
        while (parent[v] != v) {
            parent[v] = parent[parent[v]];
            v = parent[v];
        }
        return v;
    }

    public static Result kruskal(int n, Edge[] edges) {
        if (n < 0 || n > MAX_VERTICES || edges == null)
            throw new IllegalArgumentException("invalid graph");
        List<Edge> ordered = new ArrayList<>();
        for (Edge e : edges) {
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
                e.weight < -1_000_000_000L || e.weight > 1_000_000_000L)
                throw new IllegalArgumentException("invalid vertex/weight");
            ordered.add(new Edge(Math.min(e.u, e.v), Math.max(e.u, e.v), e.weight));
        }
        ordered.sort(Comparator.comparingLong((Edge e) -> e.weight)
                               .thenComparingInt(e -> e.u).thenComparingInt(e -> e.v));
        int[] parent = new int[n], size = new int[n];
        for (int v = 0; v < n; v++) { parent[v] = v; size[v] = 1; }
        List<Edge> forest = new ArrayList<>();
        long total = 0;
        for (Edge e : ordered) {
            int a = root(parent, e.u), b = root(parent, e.v);
            if (a == b) continue;
            if (size[a] < size[b]) { int swap = a; a = b; b = swap; }
            parent[b] = a;
            size[a] += size[b];
            forest.add(e);
            total = Math.addExact(total, e.weight);
        }
        return new Result(forest, total);
    }

    public static void main(String[] args) {
        Result result = kruskal(5, new Edge[] {new Edge(0, 1, 4), new Edge(0, 2, 1),
            new Edge(1, 2, 2), new Edge(3, 4, -1)});
        assert result.total == 2 && result.edges.size() == 3;
        assert kruskal(0, new Edge[0]).edges.isEmpty();
        assert kruskal(1, new Edge[] {new Edge(0, 0, -9)}).total == 0;
        System.out.println("Forest: " + result.edges + "; total: " + result.total);
    }
}
