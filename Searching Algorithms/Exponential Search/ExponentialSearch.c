#include <stdio.h>

int binary_search(int arr[], int left, int right, int key) {
    while (left <= right) {
        int mid = (left + right) / 2;

        if (arr[mid] == key)
            return mid;
        else if (arr[mid] < key)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}

int exponential_search(int arr[], int n, int key) {
    if (n <= 0) return -1;
    if (arr[0] == key)
        return 0;

    int i = 1;
    while (i < n && arr[i] <= key) {
        if (i > n / 2) return binary_search(arr, i / 2, n - 1, key);
        i *= 2;
    }

    return binary_search(arr, i/2, (i < n ? i : n-1), key);
}

void sort(int arr[], int n) {
    for (int i = 0; i < n-1; i++)
        for (int j = 0; j < n-i-1; j++)
            if (arr[j] > arr[j+1]) {
                int t = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = t;
            }
}

int main() {
    int arr[100], n, key;

    if (scanf("%d", &n) != 1 || n < 0 || n > 100) return 1;

    for (int i = 0; i < n; i++)
        if (scanf("%d", &arr[i]) != 1) return 1;

    sort(arr, n);

    if (scanf("%d", &key) != 1) return 1;

    int res = exponential_search(arr, n, key);

    if (res != -1)
        printf("Found at index: %d\n", res);
    else
        printf("Not found\n");

    return 0;
}
