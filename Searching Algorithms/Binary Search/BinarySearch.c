/* Binary search: O(log n) time, O(1) space; input must be sorted.
 * The demo sorts at most 100 integers and reports an index in that sorted array.
 */
#include <stdio.h>
#include <stdlib.h>

int binary_search(int arr[], int n, int key) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == key) return mid;
        if (arr[mid] < key) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

static int compare(const void *a, const void *b) {
    int first = *(const int *)a, second = *(const int *)b;
    return (first > second) - (first < second);
}

int main(void) {
    int arr[100], n, key;
    printf("Enter n, n integers, then the search key:\n");
    if (scanf("%d", &n) != 1 || n < 0 || n > 100) {
        fprintf(stderr, "Size must be between 0 and 100.\n");
        return 1;
    }
    for (int i = 0; i < n; ++i)
        if (scanf("%d", &arr[i]) != 1) return 1;
    if (scanf("%d", &key) != 1) return 1;
    qsort(arr, (size_t)n, sizeof(arr[0]), compare);
    int result = binary_search(arr, n, key);
    if (result < 0) printf("Not found\n");
    else printf("Found at index: %d\n", result);
    return 0;
}
