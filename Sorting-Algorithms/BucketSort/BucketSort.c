#include <stdio.h>
#include <stdlib.h>

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
    int max = arr[0];

    for (int i = 1; i < n; i++)
        if (arr[i] > max) max = arr[i];

    int bucket[n][n], count[n];

    for (int i = 0; i < n; i++)
        count[i] = 0;

    // distribute elements
    for (int i = 0; i < n; i++) {
        int index = arr[i] * n / (max + 1);
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
    scanf("%d", &n);

    for (int i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Original: ");
    print(arr, n);

    bucket_sort(arr, n);

    printf("Sorted: ");
    print(arr, n);

    return 0;
}