/* Stream N-Queens column-per-row placements; n in [0,10].
 * O(n*n! + S*n) time including O(n) visitor work; O(n) auxiliary space
 * (fixed arrays sized to limit). No allocation. n=0 emits one empty solution.
 * Return 1 success, 0 invalid. NULL visitor counts only; count is required.
 * Visitor may read placement[0..n) only during the call; copy to retain it.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

typedef void (*QueensVisitor)(const int *placement, int n, void *context);

typedef struct {
    int n, placement[10], columns[10], descending[21], ascending[21];
    size_t count;
    QueensVisitor visit;
    void *context;
} QueensSearch;

static void search_queens(QueensSearch *state, int row) {
    if (row == state->n) {
        ++state->count; /* At most 724 solutions for n<=10. */
        if (state->visit) state->visit(state->placement, state->n, state->context);
        return;
    }
    for (int column = 0; column < state->n; ++column) {
        int down = row - column + state->n, up = row + column;
        if (state->columns[column] || state->descending[down] || state->ascending[up]) continue;
        state->placement[row] = column;
        state->columns[column] = state->descending[down] = state->ascending[up] = 1;
        search_queens(state, row + 1);
        state->columns[column] = state->descending[down] = state->ascending[up] = 0;
    }
}

int n_queens(int n, QueensVisitor visit, void *context, size_t *count) {
    if (!count || n < 0 || n > 10) return 0;
    QueensSearch state = {0};
    state.n = n;
    state.visit = visit;
    state.context = context;
    search_queens(&state, 0);
    *count = state.count;
    return 1;
}

#ifndef ALGO_NO_MAIN
static void print_placement(const int *placement, int n, void *context) {
    (void)context;
    for (int i = 0; i < n; ++i) printf("%s%d", i ? " " : "", placement[i]);
    printf("\n");
}

int main(void) {
    size_t count = 0;
    int status = n_queens(0, NULL, NULL, &count);
    assert(status == 1 && count == 1);
    status = n_queens(2, NULL, NULL, &count);
    assert(status == 1 && count == 0);
    status = n_queens(8, NULL, NULL, &count);
    assert(status == 1 && count == 92);
    status = n_queens(-1, NULL, NULL, &count);
    assert(status == 0);
    status = n_queens(4, print_placement, NULL, &count);
    assert(status == 1 && count == 2);
    return status == 1 ? 0 : 1;
}
#endif
