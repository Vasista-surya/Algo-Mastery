import java.util.*;

class Searching {
    static int interpolationSearch(int[] arr, int key) {
        int low = 0, high = arr.length - 1;

        while (low <= high && key >= arr[low] && key <= arr[high]) {

            if (arr[low] == arr[high]) {
                if (arr[low] == key)
                    return low;
                return -1;
            }

            int pos = low + (int)(((long)key - arr[low]) * (high - low)
                    / ((long)arr[high] - arr[low]));

            if (arr[pos] == key)
                return pos;
            else if (arr[pos] < key)
                low = pos + 1;
            else
                high = pos - 1;
        }

        return -1;
    }
}

public class InterpolationSearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] arr = new int[n];

        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt();

        Arrays.sort(arr);

        int key = sc.nextInt();

        int res = Searching.interpolationSearch(arr, key);

        if (res != -1)
            System.out.println("Found at index: " + res);
        else
            System.out.println("Not found");

        sc.close();
    }
}
