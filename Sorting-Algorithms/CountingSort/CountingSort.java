import java.util.*;

class Sorting {
    public static void countingSort(int[] arr) {
        int max = arr[0];

        // find max
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }

        int[] count = new int[max + 1];

        // count frequency
        for (int i = 0; i < arr.length; i++) {
            count[arr[i]]++;
        }

        // rebuild array
        int index = 0;
        for (int i = 0; i < count.length; i++) {
            while (count[i] > 0) {
                arr[index++] = i;
                count[i]--;
            }
        }
    }
}

public class CountingSort {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("\n===== MENU =====");
            System.out.println("1. User Input");
            System.out.println("2. Test Cases");
            System.out.println("3. Exit");

            System.out.print("Enter choice: ");
            int choice = sc.nextInt();

            if (choice == 1) {
                // User Input
                System.out.print("Enter number of elements: ");
                int n = sc.nextInt();

                int[] arr = new int[n];
                for (int i = 0; i < n; i++) {
                    System.out.print("Enter element " + (i + 1) + ": ");
                    arr[i] = sc.nextInt();
                }

                System.out.println("Original Array: " + Arrays.toString(arr));

                Sorting.countingSort(arr);

                System.out.println("Sorted Array: " + Arrays.toString(arr));
            }

            else if (choice == 2) {
                // Test Cases
                int[][] testCases = {
                    {1, 2, 3, 4, 5},
                    {10, 20, 30, 40},
                    {3, 1, 4, 2, 5},
                    {8, 3, 7, 2, 6},
                    {5, 4, 3, 2, 1},
                    {9, 7, 5, 3, 1}
                };

                String[] names = {
                    "Best Case 1",
                    "Best Case 2",
                    "Average Case 1",
                    "Average Case 2",
                    "Worst Case 1",
                    "Worst Case 2"
                };

                System.out.println("\nSelect Test Case (1-6):");
                for (int i = 0; i < 6; i++) {
                    System.out.println((i + 1) + ". " + names[i]);
                }

                int t = sc.nextInt();

                if (t >= 1 && t <= 6) {
                    int[] arr = Arrays.copyOf(testCases[t - 1], testCases[t - 1].length);

                    System.out.println("\n" + names[t - 1]);
                    System.out.println("Original Array: " + Arrays.toString(arr));

                    Sorting.countingSort(arr);

                    System.out.println("Sorted Array: " + Arrays.toString(arr));
                } else {
                    System.out.println("Invalid choice!");
                }
            }

            else if (choice == 3) {
                System.out.println("Exiting...");
                break;
            }

            else {
                System.out.println("Invalid choice!");
            }
        }

        sc.close();
    }
}