/* Stream permutations/combinations of positions, n in [0,8]. Duplicates remain.
 * Permutations O(n*n!), combinations O((k+1)*C(n,k)), assuming O(n)/O(k) visitor.
 * O(n) search space, no heap storage. Empty permutation/k=0 emits one empty
 * tuple; k>n emits none; k<0 invalid. Return 1 success, 0 invalid.
 * NULL visitor counts only; count required. NULL items valid only when n=0.
 * Visitor's tuple is borrowed for that call only. Input must remain unchanged
 * during enumeration. Counts <=8!=40320 fit size_t (at least 16 bits).
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

typedef void (*TupleVisitor)(const int *tuple, int length, void *context);

typedef struct {
    const int *items;
    int n, k, path[8], used[8];
    size_t count;
    TupleVisitor visit;
    void *context;
} Enumeration;

static void emit(Enumeration *state, int length) {
    ++state->count;
    if (state->visit) state->visit(state->path, length, state->context);
}

static void permute(Enumeration *state, int depth) {
    if (depth == state->n) { emit(state, depth); return; }
    for (int index = 0; index < state->n; ++index) {
        if (state->used[index]) continue;
        state->used[index] = 1;
        state->path[depth] = state->items[index];
        permute(state, depth + 1);
        state->used[index] = 0;
    }
}

static void combine(Enumeration *state, int start, int depth) {
    if (depth == state->k) { emit(state, depth); return; }
    for (int index = start; index <= state->n - (state->k - depth); ++index) {
        state->path[depth] = state->items[index];
        combine(state, index + 1, depth + 1);
    }
}

int permutations(const int *items, int n, TupleVisitor visit, void *context, size_t *count) {
    if (!count || n < 0 || n > 8 || (n > 0 && !items)) return 0;
    Enumeration state = {0};
    state.items = items; state.n = n; state.visit = visit; state.context = context;
    permute(&state, 0);
    *count = state.count;
    return 1;
}

int combinations(const int *items, int n, int k, TupleVisitor visit, void *context,
                 size_t *count) {
    if (!count || n < 0 || n > 8 || k < 0 || (n > 0 && !items)) return 0;
    Enumeration state = {0};
    state.items = items; state.n = n; state.k = k;
    state.visit = visit; state.context = context;
    if (k <= n) combine(&state, 0, 0);
    *count = state.count;
    return 1;
}

#ifndef ALGO_NO_MAIN
static void print_tuple(const int *tuple, int length, void *context) {
    (void)context;
    for (int i = 0; i < length; ++i) printf("%s%d", i ? " " : "", tuple[i]);
    printf("\n");
}

int main(void) {
    const int items[] = {1, 2, 3}, duplicate[] = {1, 1};
    size_t count = 0;
    int status = permutations(NULL, 0, NULL, NULL, &count);
    assert(status == 1 && count == 1);
    status = permutations(duplicate, 2, NULL, NULL, &count);
    assert(status == 1 && count == 2);
    status = permutations(items, 3, NULL, NULL, &count);
    assert(status == 1 && count == 6);
    status = combinations(NULL, 0, 0, NULL, NULL, &count);
    assert(status == 1 && count == 1);
    status = combinations(items, 3, 4, NULL, NULL, &count);
    assert(status == 1 && count == 0);
    status = combinations(items, 3, -1, NULL, NULL, &count);
    assert(status == 0);
    status = combinations(items, 3, 2, print_tuple, NULL, &count);
    assert(status == 1 && count == 3);
    return status == 1 ? 0 : 1;
}
#endif
