export const product = {
  name: 'Algo-Mastery',
  tagline: 'Master the Logic. Own the Algorithm.',
  version: '0.1.0',
  packageName: 'com.algomastery.app',
  repository: 'https://github.com/Vasista-surya/Algo-Mastery',
  release: {
    status: 'development',
    version: '0.1.0',
    apkUrl: '',
    fileName: 'algo-mastery-debug.apk',
    size: 'Pending first release',
    checksum: 'Published with the GitHub Release'
  }
};

export const categories = [
  { id: 'all', label: 'All topics', icon: '◎', description: 'The complete learning map' },
  { id: 'sorting', label: 'Sorting', icon: '↕', description: 'Ordering and partitioning' },
  { id: 'searching', label: 'Searching', icon: '⌕', description: 'Find signal in sorted data' },
  { id: 'arrays', label: 'Arrays', icon: '▦', description: 'Patterns for linear data' },
  { id: 'strings', label: 'Strings', icon: 'Aa', description: 'Literal pattern matching' },
  { id: 'linked-lists', label: 'Linked lists', icon: '◌', description: 'Pointer-driven structures' },
  { id: 'stacks', label: 'Stacks', icon: '▤', description: 'LIFO state and parsing' },
  { id: 'queues', label: 'Queues', icon: '⇥', description: 'FIFO state and buffering' },
  { id: 'trees', label: 'Trees', icon: '⌁', description: 'Hierarchies and traversal' },
  { id: 'heaps', label: 'Heaps', icon: '▴', description: 'Priority-driven access' },
  { id: 'graphs', label: 'Graphs', icon: '✣', description: 'Routes, flow, and reachability' },
  { id: 'greedy', label: 'Greedy', icon: '↗', description: 'Local choices with proof' },
  { id: 'dynamic-programming', label: 'Dynamic programming', icon: '◫', description: 'Reuse overlapping work' },
  { id: 'backtracking', label: 'Backtracking', icon: '↶', description: 'Search, choose, undo' },
  { id: 'branch-and-bound', label: 'Branch & bound', icon: '⌘', description: 'Exact search with pruning' },
  { id: 'divide-and-conquer', label: 'Geometry', icon: '◇', description: 'Constructive technique notes' }
];

const base = 'https://github.com/Vasista-surya/Algo-Mastery/blob/main/';

export const algorithms = [
  // Sorting
  { slug: 'bubble-sort', name: 'Bubble Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Repeatedly swap adjacent values that are out of order.',
    complexity: { time: 'O(n²)', space: 'O(1)', best: 'O(n)' },
    example: '[7, 3, 5, 1] → [1, 3, 5, 7]',
    source: 'Sorting-Algorithms/BubbleSort/Bubble-Sort.py', interactive: 'sort' },
  { slug: 'selection-sort', name: 'Selection Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Select the smallest remaining value and place it at the frontier.',
    complexity: { time: 'O(n²)', space: 'O(1)', best: 'O(n²)' }, example: '[64, 25, 12, 22] → [12, 22, 25, 64]', source: 'Sorting-Algorithms/SelectionSort/SelectionSort.py' },
  { slug: 'insertion-sort', name: 'Insertion Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Grow a sorted prefix by inserting each next value into place.',
    complexity: { time: 'O(n²)', space: 'O(1)', best: 'O(n)' }, example: '[5, 2, 4] → [2, 4, 5]', source: 'Sorting-Algorithms/InsertionSort/InsertionSort.py' },
  { slug: 'merge-sort', name: 'Merge Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Split the input, sort each half, then merge ordered runs.',
    complexity: { time: 'O(n log n)', space: 'O(n)', best: 'O(n log n)' }, example: '[8, 3, 5, 4] → [3, 4, 5, 8]', source: 'Sorting-Algorithms/MergeSort/MergeSort.py' },
  { slug: 'quick-sort', name: 'Quick Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Partition around a pivot and recurse over the two sides.',
    complexity: { time: 'O(n log n) avg', space: 'O(log n) avg', best: 'O(n log n)' }, example: '[10, 7, 8, 9] → [7, 8, 9, 10]', source: 'Sorting-Algorithms/QuickSort/QuickSort.py' },
  { slug: 'heap-sort', name: 'Heap Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Build a heap and repeatedly move its maximum to the end.',
    complexity: { time: 'O(n log n)', space: 'O(log n)', best: 'O(n log n)' }, example: '[4, 10, 3, 5] → [3, 4, 5, 10]', source: 'Sorting-Algorithms/HeapSort/HeapSort.py' },
  { slug: 'counting-sort', name: 'Counting Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Count occurrences across a bounded integer range and rebuild in order.',
    complexity: { time: 'O(n + k)', space: 'O(k)', best: 'O(n + k)' }, example: '[4, 2, 2, 8] → [2, 2, 4, 8]', source: 'Sorting-Algorithms/CountingSort/CountingSort.py' },
  { slug: 'radix-sort', name: 'Radix Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Order non-negative integers one digit position at a time.',
    complexity: { time: 'O(d(n + 10))', space: 'O(n + 10)', best: 'O(d(n + 10))' }, example: '[170, 45, 75] → [45, 75, 170]', source: 'Sorting-Algorithms/RadixSort/RadixSort.py' },
  { slug: 'bucket-sort', name: 'Bucket Sort', category: 'sorting', categoryLabel: 'Sorting',
    description: 'Distribute values into range buckets, sort each bucket, and concatenate.',
    complexity: { time: 'Distribution-dependent', space: 'O(n)', best: 'Approx. O(n)' }, example: '[10, -1, 5] → [-1, 5, 10]', source: 'Sorting-Algorithms/BucketSort/BucketSort.py' },

  // Searching
  { slug: 'linear-search', name: 'Linear Search', category: 'searching', categoryLabel: 'Searching',
    description: 'Scan values from left to right until the key is found.',
    complexity: { time: 'O(n)', space: 'O(1)', best: 'O(1)' }, example: '[8, 3, 7], key 3 → index 1', source: 'Searching Algorithms/Linear Search/LinearSearch.py' },
  { slug: 'binary-search', name: 'Binary Search', category: 'searching', categoryLabel: 'Searching',
    description: 'Halve a sorted search interval after every comparison.',
    complexity: { time: 'O(log n)', space: 'O(1)', best: 'O(1)' }, example: '[1, 3, 7, 9], key 7 → index 2', source: 'Searching Algorithms/Binary Search/BinarySearch.py', interactive: 'binary' },
  { slug: 'jump-search', name: 'Jump Search', category: 'searching', categoryLabel: 'Searching',
    description: 'Jump through sorted blocks, then scan the candidate block.',
    complexity: { time: 'O(√n)', space: 'O(1)', best: 'O(1)' }, example: '[1, 3, 7, 9], key 7 → index 2', source: 'Searching Algorithms/Jump Search/JumpSearch.py' },
  { slug: 'interpolation-search', name: 'Interpolation Search', category: 'searching', categoryLabel: 'Searching',
    description: 'Estimate a likely position for uniformly distributed sorted values.',
    complexity: { time: 'O(log log n) uniform', space: 'O(1)', best: 'O(1)' }, example: '[10, 20, 30, 40], key 30 → index 2', source: 'Searching Algorithms/Interpolation Search/InterpolationSearch.py' },
  { slug: 'exponential-search', name: 'Exponential Search', category: 'searching', categoryLabel: 'Searching',
    description: 'Expand a power-of-two window, then binary-search its bounds.',
    complexity: { time: 'O(log i) near match', space: 'O(1)', best: 'O(1)' }, example: '[2, 4, 8, 16], key 8 → index 2', source: 'Searching Algorithms/Exponential Search/ExponentialSearch.py' },

  // Arrays
  { slug: 'kadane', name: "Kadane's Algorithm", category: 'arrays', categoryLabel: 'Arrays',
    description: 'Track the best non-empty contiguous subarray ending at each position.',
    complexity: { time: 'O(n)', space: 'O(1)', best: 'O(n)' }, example: '[-2, 1, -3, 4, -1, 2, 1] → 6', source: 'Arrays/Kadane/Kadane.py', interactive: 'kadane' },
  { slug: 'prefix-sum', name: 'Prefix Sum', category: 'arrays', categoryLabel: 'Arrays',
    description: 'Precompute cumulative totals so later range queries become constant time.',
    complexity: { time: 'O(n) build', space: 'O(n)', best: 'O(1) query' }, example: '[2, -1, 3, 5], [1, 3) → 2', source: 'Arrays/PrefixSum/PrefixSum.py' },
  { slug: 'sliding-window', name: 'Sliding Window', category: 'arrays', categoryLabel: 'Arrays',
    description: 'Move a fixed-width window while updating its sum incrementally.',
    complexity: { time: 'O(n)', space: 'O(1)', best: 'O(n)' }, example: '[2, -1, 3, 5], width 2 → 8', source: 'Arrays/SlidingWindow/SlidingWindow.py' },
  { slug: 'two-pointers', name: 'Two Pointers', category: 'arrays', categoryLabel: 'Arrays',
    description: 'Use sorted endpoints to move toward a target pair without backtracking.',
    complexity: { time: 'O(n)', space: 'O(1)', best: 'O(n)' }, example: '[-4, -1, 0, 3, 5], target 2 → (1, 3)', source: 'Arrays/TwoPointers/TwoPointers.py' },

  // Strings
  { slug: 'naive-pattern-matching', name: 'Naive Pattern Matching', category: 'strings', categoryLabel: 'Strings',
    description: 'Try every alignment and compare the pattern character by character.',
    complexity: { time: 'O(nm)', space: 'O(1)', best: 'O(n + m)' }, example: '"abababa", "aba" → [0, 2, 4]', source: 'Strings/NaivePatternMatching/NaivePatternMatching.py' },
  { slug: 'kmp', name: 'KMP', category: 'strings', categoryLabel: 'Strings',
    description: 'Reuse a prefix table to skip comparisons after a mismatch.',
    complexity: { time: 'O(n + m)', space: 'O(m)', best: 'O(n + m)' }, example: '"abababa", "aba" → [0, 2, 4]', source: 'Strings/KMP/KMP.py' },
  { slug: 'rabin-karp', name: 'Rabin–Karp', category: 'strings', categoryLabel: 'Strings',
    description: 'Compare rolling polynomial hashes, then verify every hash hit literally.',
    complexity: { time: 'O(nm) worst', space: 'O(1)', best: 'O(n + m)' }, example: '"a\0a\0", "a\0" → [0, 2]', source: 'Strings/RabinKarp/RabinKarp.py' },
  { slug: 'z-algorithm', name: 'Z Algorithm', category: 'strings', categoryLabel: 'Strings',
    description: 'Build prefix-match lengths over a combined pattern and text.',
    complexity: { time: 'O(n + m)', space: 'O(n + m)', best: 'O(n + m)' }, example: '"ababa", "aba" → [0, 2]', source: 'Strings/ZAlgorithm/ZAlgorithm.py' },

  // Linked lists, stacks, queues, trees, heaps
  { slug: 'reverse-linked-list', name: 'Reverse Linked List', category: 'linked-lists', categoryLabel: 'Linked lists', description: 'Rewire next pointers in place to reverse a singly linked list.', complexity: { time: 'O(n)', space: 'O(1)', best: 'O(n)' }, example: '1 → 2 → 3 becomes 3 → 2 → 1', source: 'LinkedList/ReverseLinkedList/ReverseLinkedList.py' },
  { slug: 'cycle-detection', name: 'Floyd Cycle Detection', category: 'linked-lists', categoryLabel: 'Linked lists', description: 'Move a slow and a fast pointer to detect whether links loop.', complexity: { time: 'O(n)', space: 'O(1)', best: 'O(1)' }, example: '1 → 2 → 3 → 2 → … → cycle', source: 'LinkedList/CycleDetection/CycleDetection.py' },
  { slug: 'merge-sorted-lists', name: 'Merge Sorted Lists', category: 'linked-lists', categoryLabel: 'Linked lists', description: 'Stably weave two sorted linked lists into one ordered chain.', complexity: { time: 'O(n + m)', space: 'O(1)', best: 'O(n + m)' }, example: '1 → 3 + 1 → 2 → 1 → 1 → 2 → 3', source: 'LinkedList/MergeSortedLists/MergeSortedLists.py' },
  { slug: 'infix-to-postfix', name: 'Infix to Postfix', category: 'stacks', categoryLabel: 'Stacks', description: 'Use an operator stack to make precedence explicit in postfix form.', complexity: { time: 'O(n)', space: 'O(n)', best: 'O(n)' }, example: '12 + 3 * (4 - 2) → 12 3 4 2 - * +', source: 'Stack/InfixToPostfix/InfixToPostfix.py' },
  { slug: 'expression-evaluation', name: 'Postfix Evaluation', category: 'stacks', categoryLabel: 'Stacks', description: 'Evaluate postfix tokens with a stack of intermediate values.', complexity: { time: 'O(n)', space: 'O(n)', best: 'O(n)' }, example: '12 3 4 2 - * + → 18', source: 'Stack/ExpressionEvaluation/ExpressionEvaluation.py' },
  { slug: 'balanced-parentheses', name: 'Balanced Parentheses', category: 'stacks', categoryLabel: 'Stacks', description: 'Push opening brackets and match each close against the latest opener.', complexity: { time: 'O(n)', space: 'O(n)', best: 'O(n)' }, example: 'a*(b+[c-{d}]) → balanced', source: 'Stack/BalancedParentheses/BalancedParentheses.py' },
  { slug: 'circular-queue', name: 'Circular Queue', category: 'queues', categoryLabel: 'Queues', description: 'Reuse fixed-capacity slots with head and tail indices that wrap around.', complexity: { time: 'O(1)', space: 'O(capacity)', best: 'O(1)' }, example: 'enqueue 10, 20, 30 → dequeue 10 → enqueue 40', source: 'Queue/CircularQueue/CircularQueue.py' },
  { slug: 'tree-traversals', name: 'Tree Traversals', category: 'trees', categoryLabel: 'Trees', description: 'Visit a binary tree in preorder, inorder, or postorder.', complexity: { time: 'O(n)', space: 'O(h)', best: 'O(n)' }, example: 'pre: [1, 2, 4, 5, 3]', source: 'Trees/TreeTraversals/TreeTraversals.py' },
  { slug: 'level-order-traversal', name: 'Level Order Traversal', category: 'trees', categoryLabel: 'Trees', description: 'Visit tree nodes breadth-first, one depth level at a time.', complexity: { time: 'O(n)', space: 'O(w)', best: 'O(n)' }, example: '[1, 2, 3, 4, 5]', source: 'Trees/LevelOrderTraversal/LevelOrderTraversal.py' },
  { slug: 'height-and-diameter', name: 'Height & Diameter', category: 'trees', categoryLabel: 'Trees', description: 'Compute subtree heights and the longest path in one postorder pass.', complexity: { time: 'O(n)', space: 'O(h)', best: 'O(n)' }, example: 'sample tree → height 2, diameter 3', source: 'Trees/HeightAndDiameter/HeightAndDiameter.py' },
  { slug: 'binary-search-tree', name: 'Binary Search Tree', category: 'trees', categoryLabel: 'Trees', description: 'Maintain ordered set semantics through insert, search, delete, and inorder.', complexity: { time: 'O(h)', space: 'O(1)', best: 'O(log n) balanced' }, example: 'insert 5, 3, 7 → inorder [3, 5, 7]', source: 'Trees/BinarySearchTree/BinarySearchTree.py' },
  { slug: 'min-heap', name: 'Binary Min-Heap', category: 'heaps', categoryLabel: 'Heaps', description: 'Keep the smallest value at the root through sift-up and sift-down.', complexity: { time: 'O(log n)', space: 'O(1)', best: 'O(1) peek' }, example: '[5, -2, 8, -2, 1] → pop order [-2, -2, 1, 5, 8]', source: 'Heaps/MinHeap/MinHeap.py' },

  // Graphs
  { slug: 'bfs', name: 'Breadth-First Search', category: 'graphs', categoryLabel: 'Graphs', description: 'Explore a directed graph in layers from a chosen source.', complexity: { time: 'O(V + E)', space: 'O(V + E)', best: 'O(V + E)' }, example: '0 → [0, 2, 1, 3, 4]', source: 'Graphs/BFS/BFS.py', interactive: 'bfs' },
  { slug: 'dfs', name: 'Depth-First Search', category: 'graphs', categoryLabel: 'Graphs', description: 'Follow one branch as far as possible before backtracking.', complexity: { time: 'O(V + E)', space: 'O(V + E)', best: 'O(V + E)' }, example: '0 → [0, 2, 3, 1, 4]', source: 'Graphs/DFS/DFS.py' },
  { slug: 'topological-sort', name: 'Topological Sort', category: 'graphs', categoryLabel: 'Graphs', description: 'Order a directed acyclic graph so every edge points forward.', complexity: { time: 'O(V + E)', space: 'O(V + E)', best: 'O(V + E)' }, example: '0→2, 1→2, 2→3 → [0, 1, 4, 2, 3]', source: 'Graphs/TopologicalSort/TopologicalSort.py' },
  { slug: 'dijkstra', name: "Dijkstra's Algorithm", category: 'graphs', categoryLabel: 'Graphs', description: 'Expand the nearest unsettled vertex to find non-negative shortest paths.', complexity: { time: 'O(V² + E)', space: 'O(V + E)', best: 'O(V² + E)' }, example: '0→2 (1), 2→1 (2) → dist [0, 3, 1, ∞]', source: 'Graphs/Dijkstra/Dijkstra.py' },
  { slug: 'kruskal', name: "Kruskal's Algorithm", category: 'graphs', categoryLabel: 'Graphs', description: 'Build a minimum spanning forest by accepting the lightest safe edges.', complexity: { time: 'O(V + E log E)', space: 'O(V + E)', best: 'O(V + E log E)' }, example: 'weighted graph → minimum spanning forest', source: 'Graphs/Kruskal/Kruskal.py' },
  { slug: 'prim', name: "Prim's Algorithm", category: 'graphs', categoryLabel: 'Graphs', description: 'Grow each forest component from its cheapest frontier edge.', complexity: { time: 'O(V² + E)', space: 'O(V + E)', best: 'O(V² + E)' }, example: 'disconnected graph → minimum spanning forest', source: 'Graphs/Prim/Prim.py' },
  { slug: 'bellman-ford', name: 'Bellman–Ford', category: 'graphs', categoryLabel: 'Graphs', description: 'Relax every edge repeatedly and detect source-reachable negative cycles.', complexity: { time: 'O(VE + V²)', space: 'O(V + E)', best: 'O(VE + V²)' }, example: '0→1 (4), 1→2 (-6) → [0, 4, -2, ∞]', source: 'Graphs/BellmanFord/BellmanFord.py' },
  { slug: 'floyd-warshall', name: 'Floyd–Warshall', category: 'graphs', categoryLabel: 'Graphs', description: 'Improve every pair distance by allowing one more intermediate vertex.', complexity: { time: 'O(V³ + E)', space: 'O(V²)', best: 'O(V³ + E)' }, example: 'all-pairs shortest paths with negative edges', source: 'Graphs/FloydWarshall/FloydWarshall.py' },

  // Greedy, DP, backtracking and geometry
  { slug: 'activity-selection', name: 'Activity Selection', category: 'greedy', categoryLabel: 'Greedy', description: 'Choose the largest compatible set by finishing as early as possible.', complexity: { time: 'O(n log n)', space: 'O(n)', best: 'O(n log n)' }, example: 'intervals → original indices [1, 2, 4, 5]', source: 'Greedy/ActivitySelection/ActivitySelection.py' },
  { slug: 'fractional-knapsack', name: 'Fractional Knapsack', category: 'greedy', categoryLabel: 'Greedy', description: 'Take the highest value-to-weight ratio while capacity remains.', complexity: { time: 'O(n log n)', space: 'O(n)', best: 'O(n log n)' }, example: 'capacity 50 → total value 240', source: 'Greedy/FractionalKnapsack/FractionalKnapsack.py' },
  { slug: 'huffman-coding', name: 'Huffman Coding', category: 'greedy', categoryLabel: 'Greedy', description: 'Merge the least frequent symbols to produce a prefix-free codebook.', complexity: { time: 'O(K log K)', space: 'O(K)', best: 'O(K log K)' }, example: '{a:5,b:2,c:1} → a:1, b:01, c:00', source: 'Greedy/HuffmanCoding/HuffmanCoding.py' },
  { slug: 'fibonacci', name: 'Fibonacci DP', category: 'dynamic-programming', categoryLabel: 'Dynamic programming', description: 'Build Fibonacci values iteratively while retaining only the last two.', complexity: { time: 'O(n)', space: 'O(1)', best: 'O(n)' }, example: 'F(10) → 55', source: 'DynamicProgramming/Fibonacci/Fibonacci.py' },
  { slug: 'knapsack-01', name: '0/1 Knapsack', category: 'dynamic-programming', categoryLabel: 'Dynamic programming', description: 'Fill a capacity table while using every item at most once.', complexity: { time: 'O(nC)', space: 'O(C)', best: 'O(nC)' }, example: 'weights [10,20,30], values [60,100,120], C=50 → 220', source: 'DynamicProgramming/Knapsack01/Knapsack01.py' },
  { slug: 'longest-common-subsequence', name: 'Longest Common Subsequence', category: 'dynamic-programming', categoryLabel: 'Dynamic programming', description: 'Reuse a two-string table to measure the longest ordered shared subsequence.', complexity: { time: 'O(mn)', space: 'O(min(m,n))', best: 'O(mn)' }, example: '"ABCBDAB", "BDCABA" → length 4', source: 'DynamicProgramming/LongestCommonSubsequence/LongestCommonSubsequence.py' },
  { slug: 'longest-increasing-subsequence', name: 'Longest Increasing Subsequence', category: 'dynamic-programming', categoryLabel: 'Dynamic programming', description: 'Maintain the smallest tail for each increasing subsequence length.', complexity: { time: 'O(n log n)', space: 'O(n)', best: 'O(n log n)' }, example: '[10, 9, 2, 5, 3, 7, 101] → 4', source: 'DynamicProgramming/LongestIncreasingSubsequence/LongestIncreasingSubsequence.py' },
  { slug: 'coin-change', name: 'Coin Change', category: 'dynamic-programming', categoryLabel: 'Dynamic programming', description: 'Minimize the number of unlimited-use coins needed for an amount.', complexity: { time: 'O(kA)', space: 'O(A)', best: 'O(kA)' }, example: 'coins [1,2,5], amount 11 → 3', source: 'DynamicProgramming/CoinChange/CoinChange.py' },
  { slug: 'matrix-chain-multiplication', name: 'Matrix Chain Multiplication', category: 'dynamic-programming', categoryLabel: 'Dynamic programming', description: 'Choose a parenthesization that minimizes scalar multiplication work.', complexity: { time: 'O(n³)', space: 'O(n²)', best: 'O(n³)' }, example: 'dimensions [10, 20, 30] → cost 6000', source: 'DynamicProgramming/MatrixChainMultiplication/MatrixChainMultiplication.py' },
  { slug: 'n-queens', name: 'N-Queens', category: 'backtracking', categoryLabel: 'Backtracking', description: 'Place one queen per row while pruning occupied columns and diagonals.', complexity: { time: 'O(n·n!)', space: 'O(n)', best: 'O(n·n!)' }, example: 'n=4 → 2 placements', source: 'Backtracking/NQueens/NQueens.py' },
  { slug: 'sudoku-solver', name: 'Sudoku Solver', category: 'backtracking', categoryLabel: 'Backtracking', description: 'Fill a valid 9×9 board using constraint checks and MRV search.', complexity: { time: 'O(81·9ᵉ)', space: 'O(81 + e)', best: 'Input-dependent' }, example: 'partial 9×9 board → solved board', source: 'Backtracking/SudokuSolver/SudokuSolver.py' },
  { slug: 'permutations-and-combinations', name: 'Permutations & Combinations', category: 'backtracking', categoryLabel: 'Backtracking', description: 'Enumerate positional arrangements and increasing-index selections.', complexity: { time: 'Output-sensitive', space: 'O(n)', best: 'Output-sensitive' }, example: '[1, 2, 3], k=2 → 6 combinations of positions', source: 'Backtracking/PermutationsAndCombinations/PermutationsAndCombinations.py' },
  { slug: 'traveling-salesman', name: 'Traveling Salesman', category: 'branch-and-bound', categoryLabel: 'Branch & bound', description: 'Find the exact minimum Hamiltonian cycle while pruning with a lower bound.', complexity: { time: 'O(n²·n!)', space: 'O(n)', best: 'Input-dependent' }, example: '4-city matrix → optimal cycle and cost', source: 'BranchAndBound/TravelingSalesman/TravelingSalesman.py' },
  { slug: 'convex-hull', name: 'Convex Hull', category: 'divide-and-conquer', categoryLabel: 'Geometry', description: "Build the outer boundary with Andrew's monotone chain scan.", complexity: { time: 'O(n log n)', space: 'O(n)', best: 'O(n log n)' }, example: 'points → counterclockwise hull vertices', source: 'DivideAndConquer/ConvexHull/ConvexHull.py' }
];

export const algorithmsBySlug = Object.fromEntries(algorithms.map((algorithm) => [algorithm.slug, algorithm]));

export function sourceUrl(algorithm) {
  return `${base}${algorithm.source.split('/').map(encodeURIComponent).join('/')}`;
}

export function languageSourceUrl(algorithm, extension) {
  const source = algorithm.slug === 'bubble-sort'
    ? algorithm.source.replace('Bubble-Sort.py', `BubbleSort.${extension}`)
    : algorithm.source.replace(/\.py$/, `.${extension}`);
  return `${base}${source.split('/').map(encodeURIComponent).join('/')}`;
}

export function categoryInfo(id) {
  return categories.find((category) => category.id === id) || categories[0];
}
