# Graph algorithms

Each algorithm is independent and has a matching Python module, public Java
class (helpers nested inside it), and C99 translation unit:

```text
Graphs/
  BFS/BFS.{py,java,c}
  DFS/DFS.{py,java,c}
  TopologicalSort/TopologicalSort.{py,java,c}
  Dijkstra/Dijkstra.{py,java,c}
  Kruskal/Kruskal.{py,java,c}
  Prim/Prim.{py,java,c}
  BellmanFord/BellmanFord.{py,java,c}
  FloydWarshall/FloydWarshall.{py,java,c}
```

The brace notation above denotes three actual files. Each file has a deterministic,
noninteractive demo and self-check assertions. Importing Python performs no demo.
Java requires `-ea` to enable assertions; C assertions require `NDEBUG` to be unset.

## Representation and behavior

- `n` is the number of vertices; all vertex IDs and sources must be integers in
  `[0, n)`. All edges are validated, including edges unreachable from the source.
- BFS, DFS and topological sort take **directed** `(u, v)` arcs. Shortest paths
  take **directed** `(u, v, weight)` arcs. To represent an undirected edge in these
  algorithms, supply both directions. Parallel arcs and self-loops are allowed.
- Kruskal and Prim take **undirected** `(u, v, weight)` edges, one record per edge.
  Both return a **minimum spanning forest**, never silently just one component.
  Negative weights and duplicate/parallel edges are allowed; self-loops are ignored.
  Returned edges have normalized endpoints `u <= v`. Isolated vertices are implicit
  in `n`; a forest has `n - component_count` edges. Empty input has total zero.
- BFS/DFS return only vertices reachable from the source. Neighbor order is input
  order; DFS is iterative preorder. Undirected traversal requires both arcs.
- Topological sort includes isolated vertices. Kahn's FIFO queue initially contains
  zero-indegree vertices in ascending order; later ties follow input-neighbor order.
  A cycle anywhere (including a self-loop) is reported, not returned as a partial order.
- Dijkstra rejects **every negative weight**, even in unreachable components.
- Bellman–Ford permits negative edges and rejects only **source-reachable negative
  cycles**. Unreachable cycles do not invalidate other source distances.
- Floyd–Warshall permits negative edges and rejects **any negative cycle**, since
  it solves all pairs. Parallel arcs use their minimum; the diagonal starts at zero.
  An undirected negative edge represented by two arcs is a negative cycle.
- On a negative-cycle error no distance result is usable; these APIs do not mark
  affected distances with negative infinity. Unreachable distances are positive
  infinity: Python `math.inf`, Java `INF == Long.MAX_VALUE`, C `INF == LLONG_MAX`.
  Algorithms never add to infinity. MSTs have no infinity in their results.
- An empty graph is accepted by topological sort, both forests and Floyd–Warshall.
  BFS, DFS, Dijkstra and Bellman–Ford reject it because there is no valid source.
- Inputs are not modified. Output tie rules are deterministic; Prim and Kruskal
  may choose different equally optimal forests.

## Python APIs

Edges may be any iterable of correctly sized tuples. Integers are required for
`n`, vertices, sources and weights; booleans are rejected. Integer distances/totals
are arbitrary precision (no finite overflow). Invalid domains and cycles raise
`ValueError`. Noniterable inputs are outside the API contract.

| Function | Return |
| --- | --- |
| `bfs(n, edges, source)` | vertex list |
| `dfs(n, edges, source)` | vertex list |
| `topological_sort(n, edges)` | vertex list, or `ValueError` for a cycle |
| `dijkstra(n, edges, source)` | distance list indexed by vertex |
| `bellman_ford(n, edges, source)` | distance list, or `ValueError` for reachable negative cycle |
| `floyd_warshall(n, edges)` | `n` by `n` distance list, or `ValueError` for any negative cycle |
| `kruskal(n, edges)` | `(forest_edges, total_weight)` |
| `prim(n, edges)` | `(forest_edges, total_weight)` |

```python
from Graphs.Dijkstra.Dijkstra import dijkstra
from Graphs.Prim.Prim import prim

assert dijkstra(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0) == [0, 3, 1, float("inf")]
forest, total = prim(5, [(0, 1, 4), (0, 2, 1), (1, 2, 2), (3, 4, -1)])
assert len(forest) == 3 and total == 2  # two connected components
```

## Java APIs and numeric limits

Use `Algorithm.Edge[]`; each class owns its nested immutable `Edge` type.
Unweighted constructors are `new Edge(int u, int v)`, weighted constructors are
`new Edge(int u, int v, long weight)`. No package declaration is required.

| Static method | Return |
| --- | --- |
| `BFS.bfs(int n, Edge[] edges, int source)` | `List<Integer>` |
| `DFS.dfs(int n, Edge[] edges, int source)` | `List<Integer>` |
| `TopologicalSort.topologicalSort(int n, Edge[] edges)` | `List<Integer>` |
| `Dijkstra.dijkstra(int n, Edge[] edges, int source)` | `long[]` |
| `BellmanFord.bellmanFord(int n, Edge[] edges, int source)` | `long[]` |
| `FloydWarshall.floydWarshall(int n, Edge[] edges)` | `long[][]` |
| `Kruskal.kruskal(int n, Edge[] edges)` | nested `Result`: unmodifiable `List<Edge> edges`, `long total` |
| `Prim.prim(int n, Edge[] edges)` | nested `Result`: unmodifiable `List<Edge> edges`, `long total` |

Null arrays/elements and invalid vertices/domains throw `IllegalArgumentException`.
Cycles also throw `IllegalArgumentException` with an explanatory message. Weighted
algorithms limit `n` to 10,000 and weights to `[-10^9, 10^9]` (Dijkstra: `[0,10^9]`).
Long sums use `Math.addExact`; arithmetic overflow throws `ArithmeticException`.
Bellman–Ford uses synchronous rounds to bound paths to at most `n` edges even with
a negative cycle. Floyd checks diagonals each round and never returns the reserved
infinity value for a finite sum. Ordinary Java heap/array limits still apply;
10,000 is a validation ceiling, not a promise that a dense matrix fits every heap.

```java
Dijkstra.Edge[] edges = {new Dijkstra.Edge(0, 1, 7)};
long[] distance = Dijkstra.dijkstra(3, edges, 0); // [0, 7, Dijkstra.INF]
```

## C99 APIs, capacities and ownership

Each file defines its own `Edge` (`int u, v`, plus `long long weight` when weighted).
Compile/use one standalone algorithm per translation unit; generic helper type and
constant names are deliberately local to that independent example. Define
`ALGORITHM_NO_MAIN` when including a file in your own driver. No heap allocations
are performed, so no cleanup/free is required. Inputs and output buffers must be
valid for their supplied lengths and must not overlap (including scalar outputs).

All C graph functions validate `0 <= n <= 128`, `m <= 4096`, and every endpoint.
Weighted functions require `-10^9 <= weight <= 10^9`, or `0 <= weight <= 10^9` for
Dijkstra. `m` counts duplicate arcs too. Bounded sums prevent overflow in Dijkstra,
Bellman–Ford and forests; Floyd additionally checks each signed addition. Workspace
uses fixed arrays sized to these ceilings; Prim's matrix alone is about 128 KiB
on systems with 8-byte `long long`. Provide sufficient stack space (e.g. 256 KiB
for a single algorithm call plus the caller's own storage).

```c
int bfs(int n, const Edge *edges, size_t m, int source,
        int *order, size_t capacity, size_t *count);
int dfs(int n, const Edge *edges, size_t m, int source,
        int *order, size_t capacity, size_t *count);
int topological_sort(int n, const Edge *edges, size_t m,
                     int *order, size_t capacity, size_t *count);
int dijkstra(int n, const Edge *edges, size_t m, int source,
             long long *distance, size_t capacity);
int bellman_ford(int n, const Edge *edges, size_t m, int source,
                 long long *distance, size_t capacity);
int floyd_warshall(int n, const Edge *edges, size_t m,
                   long long *distance, size_t capacity);
int kruskal(int n, const Edge *edges, size_t m, Edge *forest,
            size_t capacity, size_t *count, long long *total);
int prim(int n, const Edge *edges, size_t m, Edge *forest,
         size_t capacity, size_t *count, long long *total);
```

- Capacities count **elements**, not bytes. Traversal/topological/distance buffers
  need `n` slots. Forest buffers need `max(n-1,0)` slots even if disconnected.
  Floyd needs `n*n` slots and uses flat indexing `distance[u*n+v]`.
- Scalar output pointers (`count`, `total`) are mandatory. Null edge pointers are
  allowed only when `m == 0`; null array outputs are allowed only when the required
  capacity is zero. The nonempty source APIs always require an output array.
- Status `0`: success; `1`: directed cycle (topological) or relevant negative cycle
  (Bellman/Floyd); `-1`: invalid input/domain; `-2`: missing/short output buffer;
  Floyd `-3`: checked arithmetic overflow/reserved infinity. Ignore all array and
  scalar results on failure; no ownership is transferred.

## Complexity

`V=n`, `E=number of input edges`; bounds include graph construction/validation.
Space below is logical working/output space; C reserves the documented maxima.

| Algorithm | Time | Space |
| --- | --- | --- |
| BFS / DFS / TopologicalSort | `O(V+E)` | `O(V+E)` |
| Dijkstra (linear minimum selection) | `O(V^2+E)` | `O(V+E)` |
| Kruskal | `O(V+E log E)` | `O(V+E)` |
| Prim (linear minimum selection) | `O(V^2+E)` | Python/Java `O(V+E)`; C `O(V^2)` |
| Bellman–Ford (synchronous copies) | `O(VE+V^2)` | Python `O(V+E)`; Java/C `O(V)` beyond input |
| Floyd–Warshall | `O(V^3+E)` | `O(V^2)` |

Kruskal's C sorting term assumes an `O(E log E)` `qsort`; ISO C does not guarantee
the library sorting complexity. Python arbitrary-precision arithmetic adds costs
depending on integer bit lengths. Parallel edges and isolated vertices count in
the stated bounds.

## Running and checking

From the repository root, for example:

```text
python Graphs/Dijkstra/Dijkstra.py
javac Graphs/Dijkstra/Dijkstra.java
java -ea -cp Graphs/Dijkstra Dijkstra
cc -std=c99 -Wall -Wextra -pedantic Graphs/Dijkstra/Dijkstra.c -o dijkstra-demo
./dijkstra-demo
python -m unittest discover -s tests -p "test_graphs_greedy.py"
python -m pytest -q
```

Replace the algorithm name to run another standalone demo. The stdlib unittest
suite uses the shared `tests/_loader.py` and exercises all eight graph
algorithms and all three Greedy algorithms, including invalid input and cycles.
Run `python tools/check_examples.py` to also check every Java and C demo.
