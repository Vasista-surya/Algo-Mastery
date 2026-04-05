import java.util.*;

class Sorting {
    static void countingSort(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10];

        for (int i = 0; i < n; i++)
            count[(arr[i] / exp) % 10]++;

        for (int i = 1; i < 10; i++)
            count[i] += count[i - 1];

        for (int i = n - 1; i >= 0; i--) {
            int idx = (arr[i] / exp) % 10;
            output[count[idx] - 1] = arr[i];
            count[idx]--;
        }

        for (int i = 0; i < n; i++)
            arr[i] = output[i];
    }

    static void radixSort(int[] arr) {
        int max = arr[0];
        for (int i : arr) if (i > max) max = i;

        for (int exp = 1; max / exp > 0; exp *= 10)
            countingSort(arr, exp);
    }
}

public class RadixSort {
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

                System.out.println("Original: " + Arrays.toString(arr));
                Sorting.radixSort(arr);
                System.out.println("Sorted: " + Arrays.toString(arr));
            }

            else if (choice == 2) {
                int[][] test = {
                    {1,2,3,4,5},
                    {10,20,30,40},
                    {170,45,75,90,802},
                    {8,3,7,2,6},
                    {5,4,3,2,1},
                    {9,7,5,3,1}
                };

                int t = sc.nextInt();

                if (t >= 1 && t <= 6) {
                    int[] arr = Arrays.copyOf(test[t-1], test[t-1].length);
                    System.out.println("Original: " + Arrays.toString(arr));
                    Sorting.radixSort(arr);
                    System.out.println("Sorted: " + Arrays.toString(arr));
                }
            }

            else break;
        }
        sc.close();
    }
}