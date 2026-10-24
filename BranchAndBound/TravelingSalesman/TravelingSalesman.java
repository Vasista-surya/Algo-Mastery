import java.util.Arrays;

/** Exact directed TSP by branch-and-bound, O(n^2*n!) time/O(n) search space.
 * n<=12, diagonal 0, other entries -1 (absent) or [0,10^9]. Zero is an edge.
 * Returns null for no tour; empty graph cost 0/path []; singleton [0,0] cost 0.
 * Invalid matrices throw. Inputs are not modified; exponential worst case.
 */
public class TravelingSalesman {
    public static final class Tour {
        public final long cost;
        public final int[] path;

        private Tour(long cost, int[] path) {
            this.cost = cost;
            this.path = path;
        }
    }

    private static final class Search {
        final long[][] weights;
        final boolean[] visited;
        final int[] path;
        Tour best;

        Search(long[][] weights) {
            this.weights = weights;
            visited = new boolean[weights.length];
            path = new int[weights.length + 1];
            visited[0] = true;
        }

        long lowerBound(int last, long cost) {
            // Every completion needs one outgoing edge from last and every
            // unvisited vertex to an unvisited vertex or 0. Independent minima
            // relax distinct destinations/cycle order and thus never overestimate.
            long bound = cost;
            for (int source = 0; source < weights.length; source++) {
                if (visited[source] && source != last) continue;
                long cheapest = Long.MAX_VALUE;
                for (int destination = 0; destination < weights.length; destination++) {
                    if (destination == source || (visited[destination] && destination != 0)) continue;
                    long edge = weights[source][destination];
                    if (edge >= 0) cheapest = Math.min(cheapest, edge);
                }
                if (cheapest == Long.MAX_VALUE) return Long.MAX_VALUE;
                bound += cheapest; // <=12*10^9, including the paid prefix.
            }
            return bound;
        }

        void visit(int depth, int last, long cost) {
            if (depth == weights.length) {
                long closing = weights[last][0];
                if (closing >= 0 && (best == null || cost + closing < best.cost)) {
                    path[depth] = 0;
                    best = new Tour(cost + closing, path.clone());
                }
                return;
            }
            long bound = lowerBound(last, cost);
            if (bound == Long.MAX_VALUE || (best != null && bound >= best.cost)) return;
            for (int vertex = 1; vertex < weights.length; vertex++) {
                long edge = weights[last][vertex];
                if (visited[vertex] || edge < 0 || (best != null && cost + edge >= best.cost)) continue;
                visited[vertex] = true;
                path[depth] = vertex;
                visit(depth + 1, vertex, cost + edge);
                visited[vertex] = false;
            }
        }
    }

    public static Tour travelingSalesman(long[][] matrix) {
        if (matrix == null || matrix.length > 12) {
            throw new IllegalArgumentException("at most 12 vertices required");
        }
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            if (matrix[i] == null || matrix[i].length != n) {
                throw new IllegalArgumentException("matrix must be square");
            }
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] < -1 || matrix[i][j] > 1000000000L
                        || (i == j && matrix[i][j] != 0)) {
                    throw new IllegalArgumentException("invalid edge or nonzero diagonal");
                }
            }
        }
        if (n == 0) return new Tour(0, new int[0]);
        if (n == 1) return new Tour(0, new int[]{0, 0});
        Search search = new Search(matrix);
        search.visit(1, 0, 0);
        return search.best;
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("TSP self-check failed");
    }

    public static void main(String[] args) {
        long[][] matrix = {{0,10,15,20}, {10,0,35,25}, {15,35,0,30}, {20,25,30,0}};
        Tour tour = travelingSalesman(matrix);
        check(tour != null && tour.cost == 80 && Arrays.equals(tour.path, new int[]{0,1,3,2,0}));
        check(travelingSalesman(new long[0][0]).path.length == 0);
        check(travelingSalesman(new long[][]{{0}}).cost == 0);
        check(travelingSalesman(new long[][]{{0,1}, {-1,0}}) == null);
        check(travelingSalesman(new long[][]{{0,0}, {0,0}}).cost == 0);
        Tour directed = travelingSalesman(new long[][]{{0,0,-1}, {-1,0,2}, {3,-1,0}});
        check(directed != null && directed.cost == 5);
        System.out.println("Minimum tour: " + tour.cost + " " + Arrays.toString(tour.path));
    }
}
