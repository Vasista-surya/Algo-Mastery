import java.util.Arrays;
import java.util.NoSuchElementException;

/** Fixed-capacity int min-heap; duplicates allowed. push/pop: O(log n),
 * peek/isEmpty/size: O(1). Construction/storage O(capacity), scratch O(1).
 * Invalid capacity: IllegalArgumentException; full: IllegalStateException;
 * empty: NoSuchElementException. Failed operations preserve the heap.
 */
public class MinHeap {
    private final int[] data;
    private int size;

    public MinHeap(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be positive");
        data = new int[capacity];
    }

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }

    public void push(int value) {
        if (size == data.length) throw new IllegalStateException("heap is full");
        int index = size++;
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (data[parent] <= value) break;
            data[index] = data[parent];
            index = parent;
        }
        data[index] = value;
    }

    public int peek() {
        if (isEmpty()) throw new NoSuchElementException("heap is empty");
        return data[0];
    }

    public int pop() {
        int minimum = peek();
        int value = data[--size];
        if (size > 0) {
            int index = 0;
            // index < size/2 guarantees 2*index+1 exists without int overflow.
            while (index < size / 2) {
                int child = 2 * index + 1;
                if (child + 1 < size && data[child + 1] < data[child]) child++;
                if (value <= data[child]) break;
                data[index] = data[child];
                index = child;
            }
            data[index] = value;
        }
        return minimum;
    }

    public static void main(String[] args) {
        MinHeap heap = new MinHeap(5);
        for (int value : new int[]{5, -2, 8, -2, 1}) heap.push(value);
        assert heap.peek() == -2;
        boolean rejected = false;
        try { heap.push(9); }
        catch (IllegalStateException ex) { rejected = true; }
        assert rejected && heap.size() == 5;
        int[] result = new int[5];
        for (int i = 0; i < result.length; i++) result[i] = heap.pop();
        assert Arrays.equals(result, new int[]{-2, -2, 1, 5, 8}) && heap.isEmpty();
        rejected = false;
        try { heap.peek(); }
        catch (NoSuchElementException ex) { rejected = true; }
        assert rejected;
        heap.push(Integer.MIN_VALUE);
        int only = heap.pop();
        assert only == Integer.MIN_VALUE && heap.isEmpty();
        System.out.println(Arrays.toString(result));
    }
}
