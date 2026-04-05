import java.util.*;

class Sorting {
    public static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }

        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }

        if (largest != i) {
            // swap
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;

            heapify(arr, n, largest);
        }
    }

    public static void heapSort(int[] arr) {
        int n = arr.length;

        // build max heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        // extract elements
        for (int i = n - 1; i > 0; i--) {
            // swap
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;

            heapify(arr, i, 0);
        }
    }
}

public class HeapSort {
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

                Sorting.heapSort(arr);

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

                    Sorting.heapSort(arr);

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
} {
    
}
