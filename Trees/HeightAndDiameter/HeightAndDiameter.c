/* C99 one-pass height/diameter: O(n) time, O(h) call stack, no allocations.
 * Both count EDGES: empty height -1, leaf height 0, empty/leaf diameter 0.
 * Caller owns an acyclic, unshared tree whose depth fits the call stack.
 * Duplicate int values are allowed. Output is unchanged on failure.
 */
#include <assert.h>
#include <limits.h>
#include <stdio.h>

typedef struct Node { int value; struct Node *left, *right; } Node;
typedef struct { int height, diameter; } Metrics;
typedef enum { METRICS_OK, METRICS_INVALID, METRICS_RANGE } MetricsStatus;

static int max_int(int a, int b) { return a > b ? a : b; }

MetricsStatus height_and_diameter(const Node *root, Metrics *result) {
    Metrics left, right;
    MetricsStatus status;
    int left_path, right_path;
    if (!result) return METRICS_INVALID;
    if (!root) {
        result->height = -1;
        result->diameter = 0;
        return METRICS_OK;
    }
    status = height_and_diameter(root->left, &left);
    if (status != METRICS_OK) return status;
    status = height_and_diameter(root->right, &right);
    if (status != METRICS_OK) return status;
    /* Check before addition; do not assume long long is wider than int. */
    if (left.height == INT_MAX || right.height == INT_MAX) return METRICS_RANGE;
    left_path = left.height + 1;
    right_path = right.height + 1;
    if (left_path > INT_MAX - right_path) return METRICS_RANGE;
    result->height = max_int(left_path, right_path);
    result->diameter = max_int(max_int(left.diameter, right.diameter), left_path + right_path);
    return METRICS_OK;
}

int main(void) {
    Node four = {4, NULL, NULL}, five = {5, NULL, NULL}, three = {3, NULL, NULL};
    Node two = {2, &four, &five}, root = {1, &two, &three};
    Metrics result;
    MetricsStatus status = height_and_diameter(&root, &result);
    assert(status == METRICS_OK && result.height == 2 && result.diameter == 3);
    printf("height=%d, diameter=%d\n", result.height, result.diameter);
    status = height_and_diameter(NULL, &result);
    assert(status == METRICS_OK && result.height == -1 && result.diameter == 0);
    status = height_and_diameter(&four, &result);
    assert(status == METRICS_OK && result.height == 0 && result.diameter == 0);
    {
        Node a = {3, &four, NULL}, b = {5, NULL, &three};
        Node branch = {2, &a, &b}, outer = {1, &branch, NULL};
        status = height_and_diameter(&outer, &result);
        assert(status == METRICS_OK && result.height == 3 && result.diameter == 4);
    }
    status = height_and_diameter(&root, NULL);
    assert(status == METRICS_INVALID);
    return 0;
}
