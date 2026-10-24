import java.util.*;

/** Directed synchronous Bellman-Ford: O(VE+V^2) time, O(V) auxiliary space.
 * Vertices [0,n), n<=10000; weights [-10^9,10^9]. Both arcs for undirected.
 * INF = unreachable. Only source-reachable negative cycles are rejected.
 * Empty has no source. Invalid input/cycles throw IllegalArgumentException.
 * Synchronous rounds bound path length; long addition is also checked.
 */
public class BellmanFord {
    public static final long INF = Long.MAX_VALUE;
    public static final int MAX_VERTICES = 10000;
    public static final class Edge {
        public final int u, v;
        public final long weight;
        public Edge(int u, int v, long weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    public static long[] bellmanFord(int n, Edge[] edges, int source) {
        if (n < 0 || n > MAX_VERTICES || edges == null || source < 0 || source >= n)
            throw new IllegalArgumentException("invalid graph/source");
        for (Edge e : edges)
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
                e.weight < -1_000_000_000L || e.weight > 1_000_000_000L)
                throw new IllegalArgumentException("invalid vertex/weight");
        long[] distance = new long[n];
        Arrays.fill(distance, INF);
        distance[source] = 0;
        for (int step = 1; step < n; step++) {
            long[] updated = distance.clone();
            for (Edge e : edges)
                if (distance[e.u] != INF)
                    updated[e.v] = Math.min(updated[e.v], Math.addExact(distance[e.u], e.weight));
            if (Arrays.equals(updated, distance)) break;
            distance = updated;
        }
        for (Edge e : edges)
            if (distance[e.u] != INF && Math.addExact(distance[e.u], e.weight) < distance[e.v])
                throw new IllegalArgumentException("source-reachable negative cycle");
        return distance;
    }

    public static void main(String[] args) {
        long[] result = bellmanFord(4, new Edge[] {new Edge(0, 1, 4), new Edge(1, 2, -6)}, 0);
        assert Arrays.equals(result, new long[] {0, 4, -2, INF});
        assert Arrays.equals(bellmanFord(2, new Edge[] {new Edge(1, 1, -1)}, 0),
                             new long[] {0, INF});
        boolean rejected = false;
        try { bellmanFord(1, new Edge[] {new Edge(0, 0, -1)}, 0); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("Distances (INF=" + INF + "): " + Arrays.toString(result));
    }
}
