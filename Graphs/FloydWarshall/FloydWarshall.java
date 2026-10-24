import java.util.*;

/** Directed all-pairs shortest paths: O(V^3+E) time, O(V^2) space.
 * Vertices [0,n), n<=10000; weights [-10^9,10^9]. Both arcs for undirected.
 * INF = unreachable; zero diagonal, minimum parallel arc. Empty -> empty.
 * Any negative cycle/invalid input throws IllegalArgumentException.
 * Checked long sums throw ArithmeticException rather than overflowing.
 */
public class FloydWarshall {
    public static final long INF = Long.MAX_VALUE;
    public static final int MAX_VERTICES = 10000;
    public static final class Edge {
        public final int u, v;
        public final long weight;
        public Edge(int u, int v, long weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    private static void rejectNegativeCycle(long[][] distance) {
        for (int v = 0; v < distance.length; v++)
            if (distance[v][v] < 0) throw new IllegalArgumentException("negative cycle");
    }

    public static long[][] floydWarshall(int n, Edge[] edges) {
        if (n < 0 || n > MAX_VERTICES || edges == null)
            throw new IllegalArgumentException("invalid graph");
        for (Edge e : edges)
            if (e == null || e.u < 0 || e.u >= n || e.v < 0 || e.v >= n ||
                e.weight < -1_000_000_000L || e.weight > 1_000_000_000L)
                throw new IllegalArgumentException("invalid vertex/weight");
        long[][] distance = new long[n][n];
        for (int v = 0; v < n; v++) {
            Arrays.fill(distance[v], INF);
            distance[v][v] = 0;
        }
        for (Edge e : edges) distance[e.u][e.v] = Math.min(distance[e.u][e.v], e.weight);
        for (int k = 0; k < n; k++) {
            rejectNegativeCycle(distance);
            for (int u = 0; u < n; u++) {
                if (distance[u][k] == INF) continue;
                for (int v = 0; v < n; v++) {
                    if (distance[k][v] == INF) continue;
                    long candidate = Math.addExact(distance[u][k], distance[k][v]);
                    if (candidate == INF) throw new ArithmeticException("reserved infinity");
                    distance[u][v] = Math.min(distance[u][v], candidate);
                }
            }
        }
        rejectNegativeCycle(distance);
        return distance;
    }

    public static void main(String[] args) {
        long[][] result = floydWarshall(3, new Edge[] {new Edge(0, 1, 4), new Edge(1, 2, -6)});
        assert Arrays.equals(result[0], new long[] {0, 4, -2});
        assert result[2][0] == INF && floydWarshall(0, new Edge[0]).length == 0;
        boolean rejected = false;
        try { floydWarshall(2, new Edge[] {new Edge(1, 1, -1)}); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("Distances (INF=" + INF + "): " + Arrays.deepToString(result));
    }
}
