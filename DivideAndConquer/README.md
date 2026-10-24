# Convex hull: actual technique and category placement

This folder holds the roadmap's convex-hull example. The actual divide-and-conquer
algorithms, Merge Sort and Quick Sort, remain in the original sorting folders.
`ConvexHull/ConvexHull.{py,java,c}` uses **Andrew's monotone chain**:
lexicographically sort points, remove duplicates, then scan lower and upper
chains while removing non-left turns. **This is not a divide-and-conquer hull
implementation**; no recursive tangent/merge algorithm is claimed.

## APIs

| Language | API | Result |
| --- | --- | --- |
| Python | `convex_hull(points)` | List of `(x, y)` tuples |
| Java | `ConvexHull.convexHull(ConvexHull.Point[] points)` | Fresh `Point[]` of immutable nested points |
| C99 | `int convex_hull(const Point *points, int n, Point *output, int capacity, int *out_count)` | Status plus caller-owned output buffer/count |

Java creates points with `new ConvexHull.Point(long x, long y)`; coordinates are
public final fields. C defines `typedef struct { long long x, y; } Point;`.
All implementations leave input order/data unchanged (C also allows the output
buffer to alias the input, in which case successful output replaces it).

## Contracts and edge cases

- At most **100000 points**, with **integer** coordinates in `[-10^9,10^9]`.
  Python accepts list/tuple containers and coordinate pairs; floats, booleans,
  malformed pairs, and out-of-range coordinates raise `ValueError`. Java rejects
  null arrays/points; its point constructor rejects out-of-range coordinates
  with `IllegalArgumentException`.
- Vertices are returned **counterclockwise**, starting with the lexicographically
  smallest point, without a repeated closing vertex. For fewer than three
  extreme vertices, orientation is not meaningful.
- Duplicate points are removed. Collinear points in the interior of hull edges
  are omitted, so a fully collinear set returns just its two extreme endpoints.
  Empty input returns an empty hull, and a single distinct point returns itself.
- Exact integer cross products determine orientation, avoiding floating-point
  tolerances. Coordinate differences have magnitude at most `2*10^9`; each
  product at most `4*10^18`, and their difference at most `8*10^18`, below signed
  64-bit maximum. C/Java validate coordinate bounds before orientation arithmetic.

## Complexity and C memory handling

Time O(n log n), auxiliary/output memory O(n). C uses an in-place heapsort on
an allocated copy to guarantee O(n log n) sorting, followed by linear scans.
Python and Java use their standard sorting implementations. Every point is
pushed/popped only a constant number of times after sorting.

C return statuses:

| Status | Meaning | Output behavior |
| --- | --- | --- |
| `1` | Success | `output[0..*out_count)` holds the hull |
| `0` | Invalid inputs, dimensions, coordinates, or pointer/capacity combination | Outputs unchanged |
| `-1` | Allocation/size failure | Outputs unchanged |
| `-2` | Insufficient capacity | `*out_count` gives required count; buffer unchanged |

`out_count` is required. Negative n/capacity is invalid. Input must contain n
points; output must really contain capacity slots. Null input is allowed only
for n=0. A null output with capacity=0 is a size query: nonempty hulls return
`-2`, while empty input succeeds with count zero. Positive capacity requires a
non-null output. Do not alias `out_count` with input/output storage. All internal
allocations are size-checked and freed on every exit; returned points belong
to the caller's buffer. C99 with at least 32-bit `int`/`size_t` and at least
64-bit `long long` is the target.

## Run demos and tests

From the repository root:

```sh
python DivideAndConquer/ConvexHull/ConvexHull.py
javac DivideAndConquer/ConvexHull/ConvexHull.java
java -cp DivideAndConquer/ConvexHull ConvexHull
cc -std=c99 -Wall -Wextra -pedantic DivideAndConquer/ConvexHull/ConvexHull.c -o hull_demo
./hull_demo
python -m unittest discover -s tests -p test_optimization.py
```

Demos include duplicate, collinear, empty, and large-coordinate checks and never
read interactive input. Python imports do not execute demos. Java checks throw
`AssertionError` without requiring `-ea`. Keep Python `-O` and C `NDEBUG` disabled
for their assertions. Define `ALGO_NO_MAIN` to reuse C code without its demo.
The Python tests use the shared `tests/_loader.py`, comparing small
point sets to an independent supporting-line reference as well as checking hull
orientation and containment. `python tools/check_examples.py` checks all language demos.
