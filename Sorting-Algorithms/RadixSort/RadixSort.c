#include <stdio.h>
#include <stdlib.h>

int getMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > max) max = arr[i];
    return max;
}

void counting_sort(int arr[], int n, int exp) {
    int output[100], count[10] = {0};

    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;

    for (int i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        int idx = (arr[i] / exp) % 10;
        output[count[idx] - 1] = arr[i];
        count[idx]--;
    }

    for (int i = 0; i < n; i++)
        arr[i] = output[i];
}

void radix_sort(int arr[], int n) {
    if (n <= 0) return;
    if (n > 100) {
        fprintf(stderr, "Radix sort supports at most 100 elements.\n");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < n; ++i) {
        if (arr[i] < 0) {
            fprintf(stderr, "Radix sort requires nonnegative integers.\n");
            exit(EXIT_FAILURE);
        }
    }
    int max = getMax(arr, n);

    for (int exp = 1; max / exp > 0;) {
        counting_sort(arr, n, exp);
        if (exp > max / 10) break;
        exp *= 10;
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

    radix_sort(arr, n);

    printf("Sorted: ");
    print(arr, n);

    return 0;
}
