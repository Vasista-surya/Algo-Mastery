#include <stdio.h>

void insertion_sort(int arr[], int n) {
    int i, j, key;

    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;

        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;
    }
}

void print_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int choice;

    while (1) {
        printf("\n===== MENU =====\n");
        printf("1. User Input\n");
        printf("2. Test Cases\n");
        printf("3. Exit\n");

        printf("Enter choice: ");
        scanf("%d", &choice);

        if (choice == 1) {
            // User Input
            int n;
            printf("Enter number of elements: ");
            scanf("%d", &n);

            int arr[n];
            for (int i = 0; i < n; i++) {
                printf("Enter element %d: ", i + 1);
                scanf("%d", &arr[i]);
            }

            printf("Original Array: ");
            print_array(arr, n);

            insertion_sort(arr, n);

            printf("Sorted Array: ");
            print_array(arr, n);
        }

        else if (choice == 2) {
            // Test Cases
            int test_cases[6][5] = {
                {1, 2, 3, 4, 5},   // Best
                {10, 20, 30, 40, 0}, // Best (4 elements)
                {3, 1, 4, 2, 5},   // Average
                {8, 3, 7, 2, 6},   // Average
                {5, 4, 3, 2, 1},   // Worst
                {9, 7, 5, 3, 1}    // Worst
            };

            int sizes[6] = {5, 4, 5, 5, 5, 5};

            printf("\nSelect Test Case (1-6): ");
            int t;
            scanf("%d", &t);

            if (t >= 1 && t <= 6) {
                int arr[5];

                for (int i = 0; i < sizes[t - 1]; i++) {
                    arr[i] = test_cases[t - 1][i];
                }

                printf("Original Array: ");
                print_array(arr, sizes[t - 1]);

                insertion_sort(arr, sizes[t - 1]);

                printf("Sorted Array: ");
                print_array(arr, sizes[t - 1]);
            } else {
                printf("Invalid choice!\n");
            }
        }

        else if (choice == 3) {
            printf("Exiting...\n");
            break;
        }

        else {
            printf("Invalid choice!\n");
        }
    }

    return 0;
}