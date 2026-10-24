#include <stdio.h>
#include <math.h>

int jump_search(int arr[], int n, int key) {
    if (n <= 0) return -1;
    int step = sqrt(n);
    int prev = 0;

    while (arr[(step < n ? step : n) - 1] < key) {
        prev = step;
        step += sqrt(n);

        if (prev >= n)
            return -1;
    }

    for (int i = prev; i < (step < n ? step : n); i++) {
        if (arr[i] == key)
            return i;
    }

    return -1;
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

    int res = jump_search(arr, n, key);

    if (res != -1)
        printf("Found at index: %d\n", res);
    else
        printf("Not found\n");

    return 0;
}
