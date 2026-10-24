/* Exact directed TSP, depth-first branch-and-bound; O(n^2*n!) worst time,
 * O(n) search space (fixed storage for n<=12). Row-major weights[n*n].
 * Diagonal 0; -1 means absent; 0..10^9 are weights. Costs <=12*10^9.
 * Return 1 tour, 0 no tour, -1 invalid. Output unchanged except on success.
 * Empty graph: cost=0,length=0; singleton: cost=0,path={0,0},length=2.
 */
#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    long long cost;
    int path[13];
    int length;
} TspTour;

typedef struct {
    const long long *weights;
    int n, visited[12], path[13], found;
    TspTour best;
} TspSearch;

static long long lower_bound(const TspSearch *state, int last, long long cost) {
    /* Every completion needs one outgoing edge for last and each unvisited
     * vertex, targeting an unvisited vertex or 0. Independent minima relax
     * distinct destinations and cycle order, so this cannot overestimate. */
    long long bound = cost;
    for (int source = 0; source < state->n; ++source) {
        if (state->visited[source] && source != last) continue;
        long long cheapest = LLONG_MAX;
        for (int destination = 0; destination < state->n; ++destination) {
            if (destination == source || (state->visited[destination] && destination != 0)) continue;
            long long edge = state->weights[source * state->n + destination];
            if (edge >= 0 && edge < cheapest) cheapest = edge;
        }
        if (cheapest == LLONG_MAX) return LLONG_MAX;
        bound += cheapest;
    }
    return bound;
}

static void search_tsp(TspSearch *state, int depth, int last, long long cost) {
    if (depth == state->n) {
        long long closing = state->weights[last * state->n];
        if (closing >= 0 && (!state->found || cost + closing < state->best.cost)) {
            state->path[depth] = 0;
            state->best.cost = cost + closing;
            state->best.length = state->n + 1;
            memcpy(state->best.path, state->path, (size_t)(state->n + 1) * sizeof(int));
            state->found = 1;
        }
        return;
    }
    long long bound = lower_bound(state, last, cost);
    if (bound == LLONG_MAX || (state->found && bound >= state->best.cost)) return;
    for (int vertex = 1; vertex < state->n; ++vertex) {
        long long edge = state->weights[last * state->n + vertex];
        if (state->visited[vertex] || edge < 0
                || (state->found && cost + edge >= state->best.cost)) continue;
        state->visited[vertex] = 1;
        state->path[depth] = vertex;
        search_tsp(state, depth + 1, vertex, cost + edge);
        state->visited[vertex] = 0;
    }
}

int traveling_salesman(const long long *weights, int n, int cells, TspTour *out) {
    if (!out || n < 0 || n > 12) return -1;
    if (cells != n * n || (n > 0 && !weights)) return -1;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            long long edge = weights[i * n + j];
            if (edge < -1 || edge > 1000000000LL || (i == j && edge != 0)) return -1;
        }
    }
    TspSearch state = {0};
    state.weights = weights;
    state.n = n;
    if (n <= 1) {
        state.best.length = n == 0 ? 0 : 2;
        *out = state.best;
        return 1;
    }
    state.visited[0] = 1;
    search_tsp(&state, 1, 0, 0);
    if (!state.found) return 0;
    *out = state.best;
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const long long weights[] = {0,10,15,20, 10,0,35,25, 15,35,0,30, 20,25,30,0};
    const long long no_tour[] = {0,1,-1,0}, zero[] = {0,0,0,0};
    const long long directed[] = {0,0,-1, -1,0,2, 3,-1,0};
    const int expected[] = {0,1,3,2,0};
    TspTour result = {0};
    int status = traveling_salesman(NULL, 0, 0, &result);
    assert(status == 1 && result.cost == 0 && result.length == 0);
    status = traveling_salesman(zero, 1, 1, &result);
    assert(status == 1 && result.cost == 0 && result.length == 2);
    status = traveling_salesman(no_tour, 2, 4, &result);
    assert(status == 0);
    status = traveling_salesman(zero, 2, 4, &result);
    assert(status == 1 && result.cost == 0);
    status = traveling_salesman(directed, 3, 9, &result);
    assert(status == 1 && result.cost == 5);
    status = traveling_salesman(weights, -1, 0, &result);
    assert(status == -1);
    status = traveling_salesman(weights, 4, 16, &result);
    assert(status == 1 && result.cost == 80 && result.length == 5);
    assert(memcmp(result.path, expected, sizeof(expected)) == 0);
    if (status != 1) return 1;
    printf("Minimum tour: %lld; path:", result.cost);
    for (int i = 0; i < result.length; ++i) printf(" %d", result.path[i]);
    printf("\n");
    return 0;
}
#endif
