#include <stdio.h>
#include <stdint.h>

int interpolation_search(int arr[], int n, int key) {
    int low = 0, high = n - 1;

    while (low <= high && key >= arr[low] && key <= arr[high]) {

        if (arr[low] == arr[high]) {
            if (arr[low] == key)
                return low;
            return -1;
        }

        int pos = low + (int)(((int64_t)key - arr[low]) * (high - low)
                             / ((int64_t)arr[high] - arr[low]));

        if (arr[pos] == key)
            return pos;
        else if (arr[pos] < key)
            low = pos + 1;
        else
            high = pos - 1;
    }

    return -1;
}

void sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1]) {
                int t = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = t;
            }
}

int main() {
    int arr[100], n, key;

    if (scanf("%d", &n) != 1 || n < 0 || n > 100) return 1;

    for (int i = 0; i < n; i++)
        if (scanf("%d", &arr[i]) != 1) return 1;

    sort(arr, n);

    if (scanf("%d", &key) != 1) return 1;

    int res = interpolation_search(arr, n, key);

    if (res != -1)
        printf("Found at index: %d\n", res);
    else
        printf("Not found\n");

    return 0;
}
