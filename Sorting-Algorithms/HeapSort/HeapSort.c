#include <stdio.h>

void heapify(int arr[], int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    int temp;

    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }

    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest != i) {
        temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;

        heapify(arr, n, largest);
    }
}

void heap_sort(int arr[], int n) {
    // build max heap
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }

    // extract elements
    for (int i = n - 1; i > 0; i--) {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;

        heapify(arr, i, 0);
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

            heap_sort(arr, n);

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

                heap_sort(arr, sizes[t - 1]);

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