import java.util.*;

class Sorting {
    public static void bucketSort(int[] arr) {
        int n = arr.length;
        int max = Arrays.stream(arr).max().getAsInt();

        ArrayList<ArrayList<Integer>> buckets = new ArrayList<>();

        for (int i = 0; i < n; i++)
            buckets.add(new ArrayList<>());

        // distribute elements
        for (int num : arr) {
            int index = num * n / (max + 1);
            buckets.get(index).add(num);
        }

        // sort buckets
        for (ArrayList<Integer> bucket : buckets)
            Collections.sort(bucket);

        // merge buckets
        int k = 0;
        for (ArrayList<Integer> bucket : buckets) {
            for (int num : bucket)
                arr[k++] = num;
        }
    }
}

public class BucketSort {
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
                Sorting.bucketSort(arr);
                System.out.println("Sorted: " + Arrays.toString(arr));
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
                    System.out.println("Original: " + Arrays.toString(arr));
                    Sorting.bucketSort(arr);
                    System.out.println("Sorted: " + Arrays.toString(arr));
                }
            }

            else break;
        }
        sc.close();
    }
}