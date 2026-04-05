import java.util.*;

class Sorting {
    public static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];   // last element as pivot
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                // swap
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        // place pivot in correct position
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        return i + 1;
    }

    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);

            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
}

public class QuickSort {
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

                Sorting.quickSort(arr, 0, n - 1);

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

                    Sorting.quickSort(arr, 0, arr.length - 1);

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