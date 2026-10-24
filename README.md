# Algo Mastery — Data Structures & Algorithms

A hands-on collection of **DSA** and **Design & Analysis of Algorithms (DAA)**
for learning, problem solving, and interview preparation.

**56 algorithm/topic folders · 168 implementations · Python, Java, and C**

Every algorithm has its own folder with three independently runnable source
files. The original `Sorting-Algorithms/` and `Searching Algorithms/` names,
including their existing filenames, are preserved. The remaining categories
follow the same **category → algorithm → language files** structure.

## Repository structure

```text
Algo-Mastery/
├── Sorting-Algorithms/       # 9 sorting algorithms
├── Searching Algorithms/    # 5 searching algorithms (space in folder name)
├── Arrays/                  # Kadane, prefix sums, sliding window, two pointers
├── Strings/                 # Naive matching, KMP, Rabin–Karp, Z
├── LinkedList/              # Reverse, detect cycles, merge sorted lists
├── Stack/                   # Infix/postfix, expression evaluation, brackets
├── Queue/                   # Circular queue
├── Trees/                   # Traversals, level order, height/diameter, BST
├── Heaps/                   # Binary min-heap operations
├── Graphs/                  # Traversals, ordering, shortest paths, forests
├── Greedy/                  # Activity selection, fractional knapsack, Huffman
├── DynamicProgramming/      # Six dynamic programming problems
├── Backtracking/            # N-Queens, Sudoku, permutations/combinations
├── BranchAndBound/          # Exact traveling salesman search
├── DivideAndConquer/        # Convex hull; technique notes in category README
├── tests/                   # Python unit, regression, and structure tests
├── tools/check_examples.py  # Compile and exercise all three languages
├── requirements-dev.txt     # Optional pytest runner
└── README.md
```

For example:

```text
Arrays/
├── README.md
├── Kadane/
│   ├── Kadane.py
│   ├── Kadane.java
│   └── Kadane.c
├── PrefixSum/
├── SlidingWindow/
└── TwoPointers/
```

## Algorithm catalog

All entries below have **Python, Java, and C** implementations. Category READMEs
describe signatures, return values, complexity, input limits, and edge cases.

| Category | Implementations |
| --- | --- |
| [Sorting](Sorting-Algorithms/README.md) | Bubble, Selection, Insertion, Merge, Quick, Heap, Counting, Radix, Bucket |
| [Searching](Searching%20Algorithms/README.md) | Linear, Binary, Jump, Interpolation, Exponential |
| [Arrays](Arrays/README.md) | Kadane (maximum subarray), Prefix Sum, fixed-width Sliding Window, sorted Two Pointers |
| [Strings](Strings/README.md) | Naive Pattern Matching, KMP, Rabin–Karp, Z Algorithm |
| [Linked lists](LinkedList/README.md) | Reverse Linked List, Floyd Cycle Detection, Merge Sorted Lists |
| [Stacks](Stack/README.md) | Infix to Postfix, Postfix Expression Evaluation, Balanced Parentheses |
| [Queues](Queue/README.md) | Circular Queue: enqueue, dequeue, peek, capacity checks |
| [Trees](Trees/README.md) | Preorder/Inorder/Postorder, Level Order, Height and Diameter, BST insert/search/delete |
| [Heaps](Heaps/README.md) | Min-Heap: push, pop, peek, capacity checks |
| [Graphs](Graphs/README.md) | BFS, DFS, Topological Sort, Dijkstra, Kruskal, Prim, Bellman–Ford, Floyd–Warshall |
| [Greedy](Greedy/README.md) | Activity Selection, Fractional Knapsack, Huffman coding/encoding/decoding |
| [Dynamic programming](DynamicProgramming/README.md) | Fibonacci, 0/1 Knapsack, LCS, LIS, Coin Change, Matrix Chain Multiplication |
| [Backtracking](Backtracking/README.md) | N-Queens, Sudoku Solver, Permutations and Combinations |
| [Branch and bound](BranchAndBound/README.md) | Traveling Salesman Problem with lower-bound pruning |
| [Geometry / technique notes](DivideAndConquer/README.md) | Convex Hull using Andrew's monotone chain |

**Classification note:** Merge Sort and Quick Sort are the divide-and-conquer
examples and remain in the original sorting folders. Convex Hull is stored in
`DivideAndConquer/` but uses monotone chain, **not** a recursive divide-and-conquer
hull. LIS uses the binary-search tails technique rather than quadratic DP.

## Quick start

Run commands from the repository root. No framework, service, account, or
runtime dependency is needed. The checked toolchain is **Python 3.11**, a
**Java 17 JDK** (`java` and `javac`), and **GCC 12** with C99 support.

### Python

```sh
python Arrays/Kadane/Kadane.py
python Graphs/Dijkstra/Dijkstra.py
python "Sorting-Algorithms/BubbleSort/Bubble-Sort.py"
```

Use `python3` instead if that is your system's Python command. The original
sorting/searching Python programs offer menus: **1** custom input, **2** example
cases, **3** exit. New topic programs run a small deterministic demo with
self-checks and exit. Their functions can be imported without triggering input:

```python
from Arrays.Kadane.Kadane import max_subarray
from Strings.KMP.KMP import find_matches
from DynamicProgramming.Knapsack01.Knapsack01 import knapsack_01

assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert find_matches("ababa", "aba") == [0, 2]
assert knapsack_01([10, 20, 30], [60, 100, 120], 50) == 220
```

### Java

```sh
javac -encoding UTF-8 Arrays/Kadane/Kadane.java
java -ea -cp Arrays/Kadane Kadane

javac -encoding UTF-8 "Searching Algorithms/Binary Search/BinarySearch.java"
java -ea -cp "Searching Algorithms/Binary Search" BinarySearch
```

Compile **one algorithm at a time**. Original Java examples reuse helper class
names such as `Sorting` and `Searching`, so compiling all source files into one
directory would cause collisions. The automated checker isolates every build.
`-ea` enables Java's self-check assertions.

### C

```sh
cc -std=c99 -Wall -Wextra -pedantic Arrays/Kadane/Kadane.c -o kadane-demo.out
./kadane-demo.out
```

Use `gcc` if your compiler is not named `cc`. On Windows, use an executable name
such as `kadane-demo.exe` and run `.\kadane-demo.exe`. Some original programs
(notably Jump Search) use the math library; add `-lm` at the end of their compile
command. Quote paths containing spaces.

Original C search programs read **n, n integer values, then the search key**.
Most C sorts use a menu; Bucket Sort and Radix Sort read **n, then n values**
directly. See the sorting/searching READMEs for the exact language differences.

## Tests and verification

Verified on Linux with the toolchain above: **182 Python tests passed**, and
**168 standalone example checks passed** (56 per language), including C
undefined-behavior instrumentation. Java/C checks compile each example and
exercise its demo or original sorting/searching input flow.

The Python tests use the standard library and can run without installing anything:

```sh
python -m unittest discover -s tests -q
```

Alternatively, run the same suite with pytest:

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Compile and run every example, including regression inputs for the original
sorting/searching programs:

```sh
python tools/check_examples.py

# Individual language checks:
python tools/check_examples.py --language python
python tools/check_examples.py --language java
python tools/check_examples.py --language c --sanitize
```

The checker enables Java assertions, compiles C with
`-std=c99 -Wall -Wextra -Werror -pedantic`, and builds in temporary directories
that are removed afterward. `--sanitize` adds GCC/Clang undefined-behavior
instrumentation. Missing compilers, failed checks, and timeouts produce a nonzero
exit status; they are not silently skipped. Each child command has a 30-second
timeout. The whole check's duration depends on the machine.

Coverage includes:

- Every Python algorithm's normal, empty, duplicate, and relevant invalid inputs.
- Seeded comparisons with simple reference implementations or brute-force results.
- Graph cycles, unreachable vertices, negative edges/cycles, and disconnected forests.
- Queue/heap limits, BST deletion, overlapping string matches, and linked-list cycles.
- Sudoku givens, no-solution cases, TSP optimality, and degenerate convex hulls.
- Standalone demos/self-checks in C and Java, plus sorting/searching CLI regressions.
- Language-file completeness, import safety, and README links.

These are educational implementations, not an exhaustive correctness proof or
a production-ready general-purpose library. Read each implementation's contract
before using inputs larger than the examples.

## Important conventions

- **Indices are zero-based.** Sorted search APIs require ascending input; their
  demos sort first, so returned positions refer to the sorted array.
- **Counting Sort** supports signed integers with a value range of at most
  1,000,000. **Radix Sort** requires nonnegative integers. **Bucket Sort** supports
  signed integers. The original C sorting/searching demos accept at most 100 values.
- String matching returns **all overlapping matches**. An empty pattern matches
  every boundary. Python counts code points, Java UTF-16 units, and C bytes;
  use ASCII examples for identical offsets across languages.
- Tree height and diameter count **edges**. The unbalanced BST ignores duplicates.
- Kruskal and Prim return a **minimum spanning forest** for disconnected graphs.
  Dijkstra rejects negative weights; Bellman–Ford/Floyd–Warshall report the
  negative cycles relevant to their respective contracts.
- Coin Change minimizes the number of coins with unlimited reuse. LCS and LIS
  return lengths, not reconstructed subsequences. 0/1 Knapsack uses each item
  at most once, including zero-weight items.
- C/Java numeric and capacity limits are explicit in category READMEs. C examples
  are separate translation units, not one combined executable. Error/status
  conventions differ between independent examples; check their signatures.
- Keep Python `-O` and C `NDEBUG` disabled when running demo assertions.

## Learning path

1. Start with sorting, searching, arrays, and strings.
2. Practice linked lists, stacks, queues, trees, and heaps.
3. Study graph traversal before shortest paths and spanning trees.
4. Compare greedy choices with dynamic programming and exhaustive backtracking.
5. Finish with branch-and-bound pruning and geometric degeneracies.

Before running each example, predict the result, trace the state changes, and
consider its worst-case time and space. Complexity varies by implementation:
for example, these Dijkstra/Prim examples use linear minimum selection rather
than a priority queue. Category READMEs document the actual bounds.

## Contributing

1. Keep the existing category and algorithm folder names.
2. Add matching Python, Java, and C files for a new algorithm; retain the original
   `Bubble-Sort.py` filename exception.
3. Separate reusable logic from demos; document assumptions, errors, and complexity.
4. Add meaningful tests, including edge cases, and update the catalog/category README.
5. Run the Python tests and all-language checker before submitting a pull request.

If this collection helps you, star the repository or contribute a well-tested example.

## Algo-Mastery web platform and Android companion

The repository now also contains a focused product layer around the verified
algorithm collection:

```text
web/       static responsive learning cockpit, catalog, labs, branding, tests
android/   native Java Android catalog, bookmarks, detail screens, bubble-sort lab
```

The web app intentionally uses plain HTML, CSS, and browser ES modules so it can
deploy to any static host without a runtime service or API secret. It exposes all
56 real algorithm modules, links to their exact source files, stores bookmarks in
browser-local storage, and provides tested interactive traces for Bubble Sort,
Binary Search, Kadane's Algorithm, and BFS. The Android app is native Java with
the same core catalog and a local bubble-sort trace; it is not a landing-page
WebView.

### Web build and checks

```sh
cd web
npm test
npm run build
```

The production-ready static output is written to `web/dist/`. Deploy that folder
to GitHub Pages, Netlify, Vercel, or another static host with an SPA fallback to
`index.html` if the host needs one. For a Vercel project created from the
repository root, the checked-in `vercel.json` runs the web build and publishes
`web/dist/`; no manual root-directory guess is required. Alternatively, set the
Vercel Root Directory to `web`, use `npm run build`, and set the output directory
to `dist`. The download page currently shows a clear development state because
an APK is not published to a release asset yet.

### Android build and release

```sh
cd android
./gradlew assembleDebug
```

The verified local artifact path is
`android/app/build/outputs/apk/debug/app-debug.apk`. See `android/README.md` for
package validation, signing, and GitHub Release steps. Once a real APK is
published, update the `product.release` metadata in `web/catalog.mjs` with the
release asset URL, version, size, and checksum, then run `npm run build` again.
