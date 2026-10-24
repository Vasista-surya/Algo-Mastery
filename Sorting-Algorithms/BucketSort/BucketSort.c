#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void insertion_sort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i], j = i - 1;

        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void bucket_sort(int arr[], int n) {
    if (n <= 0) return;
    /* This teaching implementation uses O(n^2) bucket storage. */
    if (n > 100) {
        fprintf(stderr, "Bucket sort supports at most 100 elements.\n");
        exit(EXIT_FAILURE);
    }
    int max = arr[0];
    int min = arr[0];

    for (int i = 1; i < n; i++) {
        if (arr[i] > max) max = arr[i];
        if (arr[i] < min) min = arr[i];
    }

    int bucket[n][n], count[n];

    for (int i = 0; i < n; i++)
        count[i] = 0;

    // distribute elements
    for (int i = 0; i < n; i++) {
        int index = (int)(((int64_t)arr[i] - min) * n / ((int64_t)max - min + 1));
        bucket[index][count[index]++] = arr[i];
    }

    // sort buckets
    for (int i = 0; i < n; i++)
        insertion_sort(bucket[i], count[i]);

    // merge
    int k = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < count[i]; j++)
            arr[k++] = bucket[i][j];
    }
}

void print(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int arr[100], n;

    printf("Enter n: ");
    if (scanf("%d", &n) != 1 || n < 0 || n > 100) return 1;

    for (int i = 0; i < n; i++)
        if (scanf("%d", &arr[i]) != 1) return 1;

    printf("Original: ");
    print(arr, n);

    bucket_sort(arr, n);

    printf("Sorted: ");
    print(arr, n);

    return 0;
}
