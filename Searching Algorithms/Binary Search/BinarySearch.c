import java.util.*;

class Searching {
    public static int binarySearch(int[] arr, int key) {
        int low = 0, high = arr.length - 1;

        while (low <= high) {
            int mid = (low + high) / 2;

            if (arr[mid] == key)
                return mid;
            else if (arr[mid] < key)
                low = mid + 1;
            else
                high = mid - 1;
        }

        return -1;
    }
}

public class BinarySearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("\n1.User Input\n2.Test Cases\n3.Exit");
            int choice = sc.nextInt();

            if (choice == 1) {
                int n = sc.nextInt();
                int[] arr = new int[n];

                for (int i = 0; i < n; i++)
                    arr[i] = sc.nextInt();

                Arrays.sort(arr);
                System.out.println("Sorted: " + Arrays.toString(arr));

                int key = sc.nextInt();

                int res = Searching.binarySearch(arr, key);

                if (res != -1)
                    System.out.println("Found at index: " + res);
                else
                    System.out.println("Not found");
            }

            else if (choice == 2) {
                int[][] test = {
                    {1,2,3,4,5},
                    {10,20,30,40},
                    {3,1,4,2,5},
                    {8,3,7,2,6},
                    {5,4,3,2,1},
                    {9,7,5,3,1}
                };

                int t = sc.nextInt();

                if (t >= 1 && t <= 6) {
                    int[] arr = Arrays.copyOf(test[t-1], test[t-1].length);
                    Arrays.sort(arr);

                    System.out.println("Sorted: " + Arrays.toString(arr));

                    int key = sc.nextInt();

                    int res = Searching.binarySearch(arr, key);

                    if (res != -1)
                        System.out.println("Found at index: " + res);
                    else
                        System.out.println("Not found");
                }
            }

            else break;
        }
        sc.close();
    }
}