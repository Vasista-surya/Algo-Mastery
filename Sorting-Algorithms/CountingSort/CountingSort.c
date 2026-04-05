#include <stdio.h>

void counting_sort(int arr[], int n) {
    int max = arr[0];

    // find max
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }

    int count[max + 1];

    // initialize count array
    for (int i = 0; i <= max; i++) {
        count[i] = 0;
    }

    // count frequency
    for (int i = 0; i < n; i++) {
        count[arr[i]]++;
    }

    // rebuild sorted array
    int index = 0;
    for (int i = 0; i <= max; i++) {
        while (count[i] > 0) {
            arr[index++] = i;
            count[i]--;
        }
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

            int arr[100];
            for (int i = 0; i < n; i++) {
                printf("Enter element %d: ", i + 1);
                scanf("%d", &arr[i]);
            }

            printf("Original Array: ");
            print_array(arr, n);

            counting_sort(arr, n);

            printf("Sorted Array: ");
            print_array(arr, n);
        }

        else if (choice == 2) {
            // Test Cases
            int test_cases[6][5] = {
                {1, 2, 3, 4, 5},
                {10, 20, 30, 40, 0},
                {3, 1, 4, 2, 5},
                {8, 3, 7, 2, 6},
                {5, 4, 3, 2, 1},
                {9, 7, 5, 3, 1}
            };

            int sizes[6] = {5, 4, 5, 5, 5, 5};

            printf("\nSelect Test Case (1-6): ");
            int t;
            scanf("%d", &t);

            if (t >= 1 && t <= 6) {
                int arr[100];

                for (int i = 0; i < sizes[t - 1]; i++) {
                    arr[i] = test_cases[t - 1][i];
                }

                printf("Original Array: ");
                print_array(arr, sizes[t - 1]);

                counting_sort(arr, sizes[t - 1]);

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