#include <stdio.h>

void merge(int arr[], int left, int mid, int right) {
    int i = left, j = mid + 1, k = 0;
    int temp[100];  // temporary array

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j])
            temp[k++] = arr[i++];
        else
            temp[k++] = arr[j++];
    }

    while (i <= mid)
        temp[k++] = arr[i++];

    while (j <= right)
        temp[k++] = arr[j++];

    for (i = left, k = 0; i <= right; i++, k++) {
        arr[i] = temp[k];
    }
}

void merge_sort(int arr[], int left, int right) {
    if (left < right) {
        int mid = (left + right) / 2;

        merge_sort(arr, left, mid);
        merge_sort(arr, mid + 1, right);

        merge(arr, left, mid, right);
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

            merge_sort(arr, 0, n - 1);

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

                merge_sort(arr, 0, sizes[t - 1] - 1);

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