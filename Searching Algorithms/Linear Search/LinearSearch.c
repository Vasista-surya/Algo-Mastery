#include <stdio.h>

int linear_search(int arr[], int n, int key) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == key)
            return i;
    }
    return -1;
}

int main() {
    int arr[100], n, key;

    if (scanf("%d", &n) != 1 || n < 0 || n > 100) return 1;

    for (int i = 0; i < n; i++)
        if (scanf("%d", &arr[i]) != 1) return 1;

    if (scanf("%d", &key) != 1) return 1;

    int res = linear_search(arr, n, key);

    if (res != -1)
        printf("Found at index: %d\n", res);
    else
        printf("Not found\n");

    return 0;
}
