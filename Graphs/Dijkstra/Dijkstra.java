import java.util.*;

/** Directed dense-selection Dijkstra, O(V^2+E) time, O(V+E) space.
 * Vertices [0,n), n<=10000; weights 0..10^9, including unreachable edges.
 * Supply both arcs for undirected graphs. INF means unreachable. Empty has
 * no source. Invalid input throws IllegalArgumentException; sums are checked.
 */
public class Dijkstra {
    public static final long INF = Long.MAX_VALUE;
    public static final int MAX_VERTICES = 10000;
    public static final class Edge {
        public final int u, v;
        public final long weight;
        public Edge(int u, int v, long weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    public static long[] dijkstra(int n, Edge[] edges, int source) {
        if (n < 0 || n > MAX_VERTICES || edges == null || source < 0 || source >= n)
            throw new IllegalArgumentException("invalid graph/source");
        List<List<Edge>> adjacency = new ArrayList<>();
        for (int v = 0; v < n; v++) adjacency.add(new ArrayList<>());
        for (Edge e : edges) {
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
                e.weight < 0 || e.weight > 1_000_000_000L)
                throw new IllegalArgumentException("invalid vertex/weight");
            adjacency.get(e.u).add(e);
        }
        long[] distance = new long[n];
        Arrays.fill(distance, INF);
        distance[source] = 0;
        boolean[] used = new boolean[n];
        for (int step = 0; step < n; step++) {
            int u = -1;
            for (int v = 0; v < n; v++)
                if (!used[v] && (u == -1 || distance[v] < distance[u])) u = v;
            if (u == -1 || distance[u] == INF) break;
            used[u] = true;
            for (Edge e : adjacency.get(u))
                distance[e.v] = Math.min(distance[e.v], Math.addExact(distance[u], e.weight));
        }
        return distance;
    }

    public static void main(String[] args) {
        long[] result = dijkstra(4, new Edge[] {
            new Edge(0, 1, 4), new Edge(0, 2, 1), new Edge(2, 1, 2)}, 0);
        assert Arrays.equals(result, new long[] {0, 3, 1, INF});
        assert Arrays.equals(dijkstra(1, new Edge[0], 0), new long[] {0});
        boolean rejected = false;
        try { dijkstra(2, new Edge[] {new Edge(1, 1, -1)}, 0); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("Distances (INF=" + INF + "): " + Arrays.toString(result));
    }
}
