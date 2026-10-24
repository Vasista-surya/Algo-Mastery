/* C99 maximum-cardinality activities; long long start < finish, negative
 * times valid, touching endpoints compatible. Return original indices in
 * scheduled order; ties (finish,start,index). Empty succeeds. N<=4096.
 * O(N log N) with O(N log N) qsort; fixed workspace, no allocation.
 * 0 success, -1 invalid, -2 output capacity < n. Caller owns nonoverlapping
 * buffers; NULL input/output only for n=0. No time arithmetic/overflow.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

enum { MAX_ACTIVITIES = 4096 };
typedef struct { long long start, finish; } Activity;
typedef struct { Activity activity; size_t index; } IndexedActivity;

static int compare_activities(const void *left, const void *right) {
    const IndexedActivity *a = left, *b = right;
    if (a->activity.finish != b->activity.finish)
        return a->activity.finish > b->activity.finish ? 1 : -1;
    if (a->activity.start != b->activity.start)
        return a->activity.start > b->activity.start ? 1 : -1;
    return (a->index > b->index) - (a->index < b->index);
}

int activity_selection(const Activity *activities, size_t n,
                       size_t *selected, size_t capacity, size_t *count) {
    IndexedActivity ordered[MAX_ACTIVITIES];
    long long last_finish = 0;
    if (!count) return -1;
    *count = 0;
    if (n > MAX_ACTIVITIES || (n && !activities)) return -1;
    if (capacity < n || (n && !selected)) return -2;
    for (size_t i = 0; i < n; ++i) {
        if (activities[i].start >= activities[i].finish) return -1;
        ordered[i].activity = activities[i]; ordered[i].index = i;
    }
    qsort(ordered, n, sizeof(ordered[0]), compare_activities);
    for (size_t i = 0; i < n; ++i)
        if (*count == 0 || ordered[i].activity.start >= last_finish) {
            selected[(*count)++] = ordered[i].index;
            last_finish = ordered[i].activity.finish;
        }
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    const Activity activities[] = {{5, 9}, {1, 2}, {3, 4}, {0, 6}, {5, 7}, {8, 9}};
    const Activity invalid[] = {{2, 2}}, negative[] = {{-4, -2}, {-2, 0}};
    size_t selected[6], count;
    int status = activity_selection(activities, 6, selected, 6, &count);
    assert(status == 0 && count == 4);
    if (status != 0) return 1;
    assert(selected[0] == 1 && selected[1] == 2 && selected[2] == 4 && selected[3] == 5);
    printf("Selected indices:");
    for (size_t i = 0; i < count; ++i) printf(" %zu", selected[i]);
    puts("");
    assert(activity_selection(NULL, 0, NULL, 0, &count) == 0 && count == 0);
    assert(activity_selection(invalid, 1, selected, 6, &count) == -1);
    assert(activity_selection(activities, 6, selected, 1, &count) == -2);
    assert(activity_selection(negative, 2, selected, 6, &count) == 0 && count == 2);
    return 0;
}
#endif
