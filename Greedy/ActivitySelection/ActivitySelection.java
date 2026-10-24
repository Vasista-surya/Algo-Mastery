import java.util.*;

/** Maximum-cardinality compatible activities, O(N log N) time/O(N) space.
 * Long start < finish; negative times allowed. Touching endpoints compatible.
 * Return original indices; ties (finish,start,index). Empty -> empty.
 * Invalid intervals throw IllegalArgumentException; input is not modified.
 */
public class ActivitySelection {
    public static final class Activity {
        public final long start, finish;
        public Activity(long start, long finish) { this.start = start; this.finish = finish; }
    }

    public static List<Integer> activitySelection(Activity[] activities) {
        if (activities == null) throw new IllegalArgumentException("null activities");
        Integer[] order = new Integer[activities.length];
        for (int i = 0; i < activities.length; i++) {
            if (activities[i] == null || activities[i].start >= activities[i].finish)
                throw new IllegalArgumentException("start < finish required");
            order[i] = i;
        }
        Arrays.sort(order, Comparator.comparingLong((Integer i) -> activities[i].finish)
            .thenComparingLong(i -> activities[i].start).thenComparingInt(i -> i));
        List<Integer> selected = new ArrayList<>();
        long lastFinish = 0;
        for (int i : order)
            if (selected.isEmpty() || activities[i].start >= lastFinish) {
                selected.add(i);
                lastFinish = activities[i].finish;
            }
        return selected;
    }

    public static void main(String[] args) {
        List<Integer> result = activitySelection(new Activity[] {new Activity(5, 9),
            new Activity(1, 2), new Activity(3, 4), new Activity(0, 6),
            new Activity(5, 7), new Activity(8, 9)});
        assert result.equals(Arrays.asList(1, 2, 4, 5));
        assert activitySelection(new Activity[0]).isEmpty();
        assert activitySelection(new Activity[] {new Activity(-4, -2), new Activity(-2, 0)})
            .equals(Arrays.asList(0, 1));
        boolean rejected = false;
        try { activitySelection(new Activity[] {new Activity(2, 2)}); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        System.out.println("Selected indices: " + result);
    }
}
