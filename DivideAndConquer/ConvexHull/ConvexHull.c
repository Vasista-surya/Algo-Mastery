/* Andrew's monotone chain, NOT a divide-and-conquer hull. O(n log n) time
 * (heapsort), O(n) space. n<=100000; coordinates integers in [-10^9,10^9].
 * CCW extreme vertices from lexicographic minimum, no repeated endpoint.
 * Return 1 success, 0 invalid, -1 allocation failure, -2 insufficient capacity.
 * out_count is set on success/capacity failure; other failures change nothing.
 * output changes only on success; may alias input. NULL output/capacity=0
 * queries required capacity. Empty input permits NULL points and output.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { long long x, y; } Point;

static int compare_points(Point a, Point b) {
    if (a.x != b.x) return a.x < b.x ? -1 : 1;
    if (a.y != b.y) return a.y < b.y ? -1 : 1;
    return 0;
}

static void sift_down(Point *points, int root, int count) {
    while (root < count / 2) {
        int child = root * 2 + 1;
        if (child + 1 < count && compare_points(points[child], points[child + 1]) < 0) ++child;
        if (compare_points(points[root], points[child]) >= 0) return;
        Point swap = points[root]; points[root] = points[child]; points[child] = swap;
        root = child;
    }
}

static void sort_points(Point *points, int n) {
    for (int root = n / 2 - 1; root >= 0; --root) sift_down(points, root, n);
    for (int end = n - 1; end > 0; --end) {
        Point swap = points[0]; points[0] = points[end]; points[end] = swap;
        sift_down(points, 0, end);
    }
}

static long long cross(Point origin, Point a, Point b) {
    /* Differences <=2*10^9; products <=4*10^18; subtraction <=8*10^18.
     * All fit C99's at-least-64-bit signed long long after validation. */
    return (a.x - origin.x) * (b.y - origin.y) - (a.y - origin.y) * (b.x - origin.x);
}

int convex_hull(const Point *points, int n, Point *output, int capacity, int *out_count) {
    if (!out_count || n < 0 || n > 100000 || capacity < 0
            || (n > 0 && !points) || (capacity > 0 && !output)) return 0;
    for (int i = 0; i < n; ++i) {
        if (points[i].x < -1000000000LL || points[i].x > 1000000000LL
                || points[i].y < -1000000000LL || points[i].y > 1000000000LL) return 0;
    }
    if (n == 0) { *out_count = 0; return 1; }
    if ((size_t)n > SIZE_MAX / sizeof(Point) / 2) return -1;
    Point *ordered = malloc((size_t)n * sizeof(*ordered));
    Point *hull = malloc(2 * (size_t)n * sizeof(*hull));
    if (!ordered || !hull) { free(ordered); free(hull); return -1; }
    memcpy(ordered, points, (size_t)n * sizeof(*ordered));
    sort_points(ordered, n);
    int unique = 0;
    for (int i = 0; i < n; ++i) {
        if (unique == 0 || compare_points(ordered[i], ordered[unique - 1]) != 0) {
            ordered[unique++] = ordered[i];
        }
    }
    int size = 0;
    for (int i = 0; i < unique; ++i) {
        while (size >= 2 && cross(hull[size - 2], hull[size - 1], ordered[i]) <= 0) --size;
        hull[size++] = ordered[i];
    }
    int upper_start = size + 1;
    for (int i = unique - 2; i >= 0; --i) {
        while (size >= upper_start && cross(hull[size - 2], hull[size - 1], ordered[i]) <= 0) --size;
        hull[size++] = ordered[i];
    }
    if (unique > 1) --size;
    *out_count = size;
    if (capacity < size) { free(ordered); free(hull); return -2; }
    memcpy(output, hull, (size_t)size * sizeof(*output));
    free(ordered);
    free(hull);
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const Point points[] = {{0,0},{2,0},{2,2},{0,2},{1,1},{0,0},{1,0}};
    const Point expected[] = {{0,0},{2,0},{2,2},{0,2}};
    const Point line[] = {{2,2},{0,0},{1,1}}, duplicate[] = {{1,1},{1,1}};
    const Point large[] = {{-1000000000LL,-1000000000LL},{1000000000LL,-1000000000LL},
                          {1000000000LL,1000000000LL},{-1000000000LL,1000000000LL}};
    Point hull[7];
    int count = 0;
    int status = convex_hull(NULL, 0, NULL, 0, &count);
    assert(status == 1 && count == 0);
    status = convex_hull(points, 7, NULL, 0, &count);
    assert(status == -2 && count == 4);
    status = convex_hull(line, 3, hull, 7, &count);
    assert(status == 1 && count == 2 && hull[0].x == 0 && hull[1].x == 2);
    status = convex_hull(duplicate, 2, hull, 7, &count);
    assert(status == 1 && count == 1 && hull[0].x == 1 && hull[0].y == 1);
    status = convex_hull(large, 4, hull, 7, &count);
    assert(status == 1 && count == 4);
    for (int i = 0; i < count; ++i) assert(compare_points(hull[i], large[i]) == 0);
    status = convex_hull(points, 7, hull, 7, &count);
    assert(status == 1 && count == 4);
    if (status != 1) return 1;
    for (int i = 0; i < count; ++i) {
        assert(compare_points(hull[i], expected[i]) == 0);
        printf("(%lld, %lld)%s", hull[i].x, hull[i].y, i + 1 == count ? "\n" : " ");
    }
    return 0;
}
#endif
