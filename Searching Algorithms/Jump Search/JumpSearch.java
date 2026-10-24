import java.util.*;

class Searching {
    static int jumpSearch(int[] arr, int key) {
        int n = arr.length;
        if (n == 0) return -1;
        int step = (int)Math.sqrt(n);
        int prev = 0;

        while (arr[Math.min(step, n) - 1] < key) {
            prev = step;
            step += (int)Math.sqrt(n);

            if (prev >= n)
                return -1;
        }

        for (int i = prev; i < Math.min(step, n); i++) {
            if (arr[i] == key)
                return i;
        }

        return -1;
    }
}

public class JumpSearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] arr = new int[n];

        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt();

        Arrays.sort(arr);

        int key = sc.nextInt();

        int res = Searching.jumpSearch(arr, key);

        if (res != -1)
            System.out.println("Found at index: " + res);
        else
            System.out.println("Not found");

        sc.close();
    }
}
