import java.util.Arrays;

/** Andrew's monotone chain (not a divide-and-conquer hull).
 * O(n log n) time, O(n) space; n<=100000, integer coordinates in [-10^9,10^9].
 * CCW extreme vertices from lexicographic minimum, no closing repetition;
 * duplicate/interior collinear points removed. Empty -> []; no input mutation.
 */
public class ConvexHull {
    public static final class Point {
        public final long x, y;

        public Point(long x, long y) {
            if (x < -1000000000L || x > 1000000000L || y < -1000000000L || y > 1000000000L) {
                throw new IllegalArgumentException("coordinates must be in [-10^9,10^9]");
            }
            this.x = x; this.y = y;
        }

        @Override public boolean equals(Object other) {
            if (!(other instanceof Point)) return false;
            Point point = (Point) other;
            return x == point.x && y == point.y;
        }

        @Override public int hashCode() {
            return 31 * Long.hashCode(x) + Long.hashCode(y);
        }

        @Override public String toString() { return "(" + x + ", " + y + ")"; }
    }

    private static long cross(Point origin, Point a, Point b) {
        // Differences <=2*10^9, each product <=4*10^18, difference <=8*10^18.
        return (a.x - origin.x) * (b.y - origin.y) - (a.y - origin.y) * (b.x - origin.x);
    }

    public static Point[] convexHull(Point[] points) {
        if (points == null || points.length > 100000) {
            throw new IllegalArgumentException("at most 100000 points required");
        }
        for (Point point : points) {
            if (point == null) throw new IllegalArgumentException("points must not be null");
        }
        Point[] ordered = points.clone();
        Arrays.sort(ordered, (a, b) -> {
            int byX = Long.compare(a.x, b.x);
            return byX != 0 ? byX : Long.compare(a.y, b.y);
        });
        int unique = 0;
        for (int i = 0; i < ordered.length; i++) {
            Point point = ordered[i];
            if (unique == 0 || !point.equals(ordered[unique - 1])) ordered[unique++] = point;
        }
        if (unique <= 1) return Arrays.copyOf(ordered, unique);
        Point[] hull = new Point[2 * unique];
        int size = 0;
        for (int i = 0; i < unique; i++) {
            while (size >= 2 && cross(hull[size - 2], hull[size - 1], ordered[i]) <= 0) size--;
            hull[size++] = ordered[i];
        }
        int upperStart = size + 1;
        for (int i = unique - 2; i >= 0; i--) {
            while (size >= upperStart && cross(hull[size - 2], hull[size - 1], ordered[i]) <= 0) size--;
            hull[size++] = ordered[i];
        }
        return Arrays.copyOf(hull, size - 1);
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Convex-hull self-check failed");
    }

    public static void main(String[] args) {
        Point[] points = {new Point(0,0), new Point(2,0), new Point(2,2),
                new Point(0,2), new Point(1,1), new Point(0,0), new Point(1,0)};
        Point[] expected = {new Point(0,0), new Point(2,0), new Point(2,2), new Point(0,2)};
        check(Arrays.equals(convexHull(points), expected));
        check(convexHull(new Point[0]).length == 0);
        check(convexHull(new Point[]{new Point(1,1), new Point(1,1)}).length == 1);
        check(Arrays.equals(convexHull(new Point[]{new Point(2,2), new Point(0,0), new Point(1,1)}),
                new Point[]{new Point(0,0), new Point(2,2)}));
        Point[] large = {new Point(-1000000000L,-1000000000L), new Point(1000000000L,-1000000000L),
                new Point(1000000000L,1000000000L), new Point(-1000000000L,1000000000L)};
        check(Arrays.equals(convexHull(large), large));
        System.out.println("Convex hull: " + Arrays.toString(convexHull(points)));
    }
}
