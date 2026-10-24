#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void counting_sort(int arr[], int n) {
    if (n <= 0) return;
    int max = arr[0];
    int min = arr[0];

    // find max
    for (int i = 1; i < n; i++) {
        if (arr[i] < min) min = arr[i];
        if (arr[i] > max) {
            max = arr[i];
        }
    }

    int64_t width = (int64_t)max - min + 1;
    if (width > 1000000) {
        fprintf(stderr, "Counting sort supports a value range of at most 1,000,000.\n");
        exit(EXIT_FAILURE);
    }
    int *count = calloc((size_t)width, sizeof(*count));
    if (count == NULL) {
        fprintf(stderr, "Cannot allocate counts.\n");
        exit(EXIT_FAILURE);
    }

    // count frequency
    for (int i = 0; i < n; i++) {
        count[arr[i] - min]++;
    }

    // rebuild sorted array
    int index = 0;
    for (int i = 0; i < (int)width; i++) {
        while (count[i] > 0) {
            arr[index++] = i + min;
            count[i]--;
        }
    }
    free(count);
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
        if (scanf("%d", &choice) != 1) break;

        if (choice == 1) {
            // User Input
            int n;
            printf("Enter number of elements: ");
            if (scanf("%d", &n) != 1 || n < 0 || n > 100) return 1;

            int arr[100];
            for (int i = 0; i < n; i++) {
                printf("Enter element %d: ", i + 1);
                if (scanf("%d", &arr[i]) != 1) return 1;
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
            if (scanf("%d", &t) != 1) return 1;

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
