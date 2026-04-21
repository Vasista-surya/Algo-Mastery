import java.util.*;

class Searching {
    static int linearSearch(int[] arr, int key) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == key)
                return i;
        }
        return -1;
    }
}

public class LinearSearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] arr = new int[n];

        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt();

        int key = sc.nextInt();

        int res = Searching.linearSearch(arr, key);

        if (res != -1)
            System.out.println("Found at index: " + res);
        else
            System.out.println("Not found");

        sc.close();
    }
}