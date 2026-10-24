import java.util.*;

class Searching {

    static int binarySearch(int[] arr, int left, int right, int key) {
        while (left <= right) {
            int mid = (left + right) / 2;

            if (arr[mid] == key)
                return mid;
            else if (arr[mid] < key)
                left = mid + 1;
            else
                right = mid - 1;
        }
        return -1;
    }

    static int exponentialSearch(int[] arr, int key) {
        int n = arr.length;
        if (n == 0) return -1;

        if (arr[0] == key)
            return 0;

        int i = 1;
        while (i < n && arr[i] <= key) {
            if (i > n / 2) return binarySearch(arr, i / 2, n - 1, key);
            i *= 2;
        }

        return binarySearch(arr, i / 2, Math.min(i, n - 1), key);
    }
}

public class ExponentialSearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] arr = new int[n];

        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt();

        Arrays.sort(arr);

        int key = sc.nextInt();

        int res = Searching.exponentialSearch(arr, key);

        if (res != -1)
            System.out.println("Found at index: " + res);
        else
            System.out.println("Not found");

        sc.close();
    }
}
