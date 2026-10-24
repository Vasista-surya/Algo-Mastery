import java.util.Arrays;
import java.util.NoSuchElementException;

/** Fixed-capacity int FIFO: O(1) operations, O(capacity) initialization/storage.
 * Invalid capacity: IllegalArgumentException. Full: IllegalStateException.
 * Empty peek/dequeue: NoSuchElementException. Failed calls preserve the queue.
 */
public class CircularQueue {
    private final int[] data;
    private int head;
    private int size;

    public CircularQueue(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be positive");
        data = new int[capacity];
    }

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }

    public void enqueue(int value) {
        if (size == data.length) throw new IllegalStateException("queue is full");
        int tail = (int) (((long) head + size) % data.length);
        data[tail] = value;
        size++;
    }

    public int peek() {
        if (isEmpty()) throw new NoSuchElementException("queue is empty");
        return data[head];
    }

    public int dequeue() {
        int value = peek();
        head = head == data.length - 1 ? 0 : head + 1;
        size--;
        return value;
    }

    public static void main(String[] args) {
        CircularQueue queue = new CircularQueue(3);
        assert queue.isEmpty();
        queue.enqueue(10); queue.enqueue(20); queue.enqueue(30);
        boolean rejected = false;
        try { queue.enqueue(40); }
        catch (IllegalStateException ex) { rejected = true; }
        assert rejected && queue.size() == 3;
        int first = queue.dequeue();
        assert first == 10;
        queue.enqueue(40);
        int[] result = {queue.dequeue(), queue.dequeue(), queue.dequeue()};
        assert Arrays.equals(result, new int[]{20, 30, 40}) && queue.isEmpty();
        rejected = false;
        try { queue.dequeue(); }
        catch (NoSuchElementException ex) { rejected = true; }
        assert rejected;
        CircularQueue single = new CircularQueue(1);
        single.enqueue(-1);
        int only = single.dequeue();
        assert only == -1 && single.isEmpty();
        System.out.println(Arrays.toString(result));
    }
}
