# Branch and bound: Traveling Salesman

`TravelingSalesman/TravelingSalesman.{py,java,c}` implement an exact
**depth-first branch-and-bound** search for a minimum Hamiltonian cycle starting
and ending at vertex 0. The matrix may be directed/asymmetric. The deterministic
demos exercise a four-city optimum, zero-cost edges, absent edges, and no tour.

## APIs and results

| Language | API | Result |
| --- | --- | --- |
| Python | `traveling_salesman(matrix)` | `(cost, path_tuple)` or `None` if no tour |
| Java | `TravelingSalesman.travelingSalesman(long[][] matrix)` | Nested `Tour` with public `long cost`, `int[] path`; `null` if no tour |
| C99 | `int traveling_salesman(const long long *weights, int n, int cells, TspTour *out)` | Status `1` tour, `0` no tour, `-1` invalid input |

C uses a **flat row-major** matrix of exactly `cells == n*n` entries and a
caller-owned result:

```c
typedef struct {
    long long cost;
    int path[13];
    int length;
} TspTour;
```

Only `path[0..length)` is part of the result. The struct remains unchanged on
no-tour/invalid results. No heap memory is allocated by the C implementation.
Callers must provide the stated input length and a valid output pointer.

## Input contract and empty cases

- Square matrices of **0..12 vertices**. Python accepts lists/tuples of
  lists/tuples with integer entries, rejecting booleans. Java rejects null
  arrays/rows. C validates negative dimensions and the supplied cell count.
- **Diagonal must be zero.** Off-diagonal `-1` explicitly means **absent edge**.
  Edge weights `0..10^9` are allowed, including zero; all other values are invalid.
  Input matrices are not changed.
- No solution is distinct from an empty graph and from a zero-cost tour.
  The empty graph has cost 0 and path `[]` (Python `()`). A singleton has cost 0
  and path `[0,0]`, representing no edge traversal. C accepts null weights only
  when n=0 and cells=0.
- For n>=2, the path has n+1 entries, visits each vertex once, and explicitly
  closes at 0. A missing closing edge prevents a tour.
- Vertices are tried in increasing order. Only strict improvements replace the
  incumbent, giving the lexicographically first minimum-cost path on ties.
- Python raises `ValueError` for invalid input; Java throws
  `IllegalArgumentException`. Invalid input never masquerades as no tour.

## Why the bound is valid

For a partial path with paid cost g, endpoint u, and unvisited set R, any
completion must select one outgoing edge from **every vertex in `{u} union R`**.
Each such edge must target a vertex in `R union {0}`, excluding its own source.
For each required source, compute the cheapest present edge to that relaxed
destination set, and add these minima to g.

This relaxation permits multiple sources to choose the same destination and
permits premature return to 0. Removing those constraints can only lower the
cost relative to a real completion. Consequently:

1. If a source has no eligible outgoing edge, the branch is infeasible.
2. If the sum is at least the best complete tour cost, no strict improvement is
   possible and the branch is pruned.
3. A prefix whose paid cost already reaches the incumbent can also be pruned
   because all real edge weights are nonnegative.

The incumbent starts unset and is updated only after finding a complete cycle
with an existing return edge. The implementation genuinely evaluates this bound
at internal search nodes; it is not a permutation enumerator with a misleading name.

## Complexity, numeric safety, and practical limits

Worst-case time is O(n^2*n!), including O(n^2) work per lower-bound evaluation.
Search memory is O(n), beyond the O(n^2) input matrix. Small examples may prune
heavily, but the worst case remains factorial, including some sparse no-tour
instances. The limit of 12 is a safety ceiling, not a speed guarantee.

Each bound comprises the paid prefix plus relaxed remaining edges: at most n
edge terms, each at most `10^9`. Costs and bounds are therefore at most
`12*10^9`, comfortably within Java `long`
and C99 `long long`. Infinity sentinels are never added. C uses fixed arrays
sized for the limit and targets ordinary 32-bit-or-wider `int`/`size_t` platforms.

## Run demos and tests

From the repository root:

```sh
python BranchAndBound/TravelingSalesman/TravelingSalesman.py
javac BranchAndBound/TravelingSalesman/TravelingSalesman.java
java -cp BranchAndBound/TravelingSalesman TravelingSalesman
cc -std=c99 -Wall -Wextra -pedantic BranchAndBound/TravelingSalesman/TravelingSalesman.c -o tsp_demo
./tsp_demo
python -m unittest discover -s tests -p test_optimization.py
```

Python imports are side-effect-free. Java checks explicitly throw
`AssertionError`, so `-ea` is optional. Keep Python `-O` and C `NDEBUG` disabled
for demo assertions. Define `ALGO_NO_MAIN` to reuse the C implementation without
its demo entry point. Python tests use the shared `tests/_loader.py`
and compare small directed/sparse graphs with brute-force tour enumeration.
Run `python tools/check_examples.py` to also check every Java and C demo.
