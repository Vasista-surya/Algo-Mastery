package com.algomastery.app;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/** The native app mirrors the repository's 56 documented algorithm folders. */
final class AlgorithmCatalog {
    static final class Algorithm {
        final String slug;
        final String name;
        final String category;
        final String description;
        final String time;
        final String space;
        final String source;
        final boolean interactive;

        Algorithm(String slug, String name, String category, String description, String time,
                  String space, String source, boolean interactive) {
            this.slug = slug;
            this.name = name;
            this.category = category;
            this.description = description;
            this.time = time;
            this.space = space;
            this.source = source;
            this.interactive = interactive;
        }
    }

    private static Algorithm a(String slug, String name, String category, String description,
                               String time, String space, String source) {
        return new Algorithm(slug, name, category, description, time, space, source, false);
    }

    private static Algorithm interactive(String slug, String name, String category, String description,
                                         String time, String space, String source) {
        return new Algorithm(slug, name, category, description, time, space, source, true);
    }

    static List<Algorithm> all() {
        return ITEMS;
    }

    static Algorithm bySlug(String slug) {
        for (Algorithm algorithm : ITEMS) if (algorithm.slug.equals(slug)) return algorithm;
        return null;
    }

    static List<String> categories() {
        return Arrays.asList("All topics", "Sorting", "Searching", "Arrays", "Strings", "Linked lists", "Stacks", "Queues", "Trees", "Heaps", "Graphs", "Greedy", "Dynamic programming", "Backtracking", "Branch & bound", "Geometry");
    }

    private static final List<Algorithm> ITEMS;
    static {
        List<Algorithm> items = new ArrayList<>();
        items.add(interactive("bubble-sort", "Bubble Sort", "Sorting", "Repeatedly swap adjacent values that are out of order.", "O(n²)", "O(1)", "Sorting-Algorithms/BubbleSort/Bubble-Sort.py"));
        items.add(a("selection-sort", "Selection Sort", "Sorting", "Select the smallest remaining value and place it at the frontier.", "O(n²)", "O(1)", "Sorting-Algorithms/SelectionSort/SelectionSort.py"));
        items.add(a("insertion-sort", "Insertion Sort", "Sorting", "Grow a sorted prefix by inserting each next value into place.", "O(n²)", "O(1)", "Sorting-Algorithms/InsertionSort/InsertionSort.py"));
        items.add(a("merge-sort", "Merge Sort", "Sorting", "Split the input, sort each half, then merge ordered runs.", "O(n log n)", "O(n)", "Sorting-Algorithms/MergeSort/MergeSort.py"));
        items.add(a("quick-sort", "Quick Sort", "Sorting", "Partition around a pivot and recurse over the two sides.", "O(n log n) avg", "O(log n) avg", "Sorting-Algorithms/QuickSort/QuickSort.py"));
        items.add(a("heap-sort", "Heap Sort", "Sorting", "Build a heap and repeatedly move its maximum to the end.", "O(n log n)", "O(log n)", "Sorting-Algorithms/HeapSort/HeapSort.py"));
        items.add(a("counting-sort", "Counting Sort", "Sorting", "Count occurrences across a bounded integer range and rebuild in order.", "O(n + k)", "O(k)", "Sorting-Algorithms/CountingSort/CountingSort.py"));
        items.add(a("radix-sort", "Radix Sort", "Sorting", "Order non-negative integers one digit position at a time.", "O(d(n + 10))", "O(n + 10)", "Sorting-Algorithms/RadixSort/RadixSort.py"));
        items.add(a("bucket-sort", "Bucket Sort", "Sorting", "Distribute values into range buckets, sort each bucket, and concatenate.", "Distribution-dependent", "O(n)", "Sorting-Algorithms/BucketSort/BucketSort.py"));
        items.add(a("linear-search", "Linear Search", "Searching", "Scan values from left to right until the key is found.", "O(n)", "O(1)", "Searching Algorithms/Linear Search/LinearSearch.py"));
        items.add(interactive("binary-search", "Binary Search", "Searching", "Halve a sorted search interval after every comparison.", "O(log n)", "O(1)", "Searching Algorithms/Binary Search/BinarySearch.py"));
        items.add(a("jump-search", "Jump Search", "Searching", "Jump through sorted blocks, then scan the candidate block.", "O(√n)", "O(1)", "Searching Algorithms/Jump Search/JumpSearch.py"));
        items.add(a("interpolation-search", "Interpolation Search", "Searching", "Estimate a likely position for uniformly distributed sorted values.", "O(log log n) uniform", "O(1)", "Searching Algorithms/Interpolation Search/InterpolationSearch.py"));
        items.add(a("exponential-search", "Exponential Search", "Searching", "Expand a power-of-two window, then binary-search its bounds.", "O(log i) near match", "O(1)", "Searching Algorithms/Exponential Search/ExponentialSearch.py"));
        items.add(interactive("kadane", "Kadane's Algorithm", "Arrays", "Track the best non-empty contiguous subarray ending at each position.", "O(n)", "O(1)", "Arrays/Kadane/Kadane.py"));
        items.add(a("prefix-sum", "Prefix Sum", "Arrays", "Precompute cumulative totals so later range queries become constant time.", "O(n) build", "O(n)", "Arrays/PrefixSum/PrefixSum.py"));
        items.add(a("sliding-window", "Sliding Window", "Arrays", "Move a fixed-width window while updating its sum incrementally.", "O(n)", "O(1)", "Arrays/SlidingWindow/SlidingWindow.py"));
        items.add(a("two-pointers", "Two Pointers", "Arrays", "Use sorted endpoints to move toward a target pair without backtracking.", "O(n)", "O(1)", "Arrays/TwoPointers/TwoPointers.py"));
        items.add(a("naive-pattern-matching", "Naive Pattern Matching", "Strings", "Try every alignment and compare the pattern character by character.", "O(nm)", "O(1)", "Strings/NaivePatternMatching/NaivePatternMatching.py"));
        items.add(a("kmp", "KMP", "Strings", "Reuse a prefix table to skip comparisons after a mismatch.", "O(n + m)", "O(m)", "Strings/KMP/KMP.py"));
        items.add(a("rabin-karp", "Rabin–Karp", "Strings", "Compare rolling polynomial hashes, then verify every hash hit literally.", "O(nm) worst", "O(1)", "Strings/RabinKarp/RabinKarp.py"));
        items.add(a("z-algorithm", "Z Algorithm", "Strings", "Build prefix-match lengths over a combined pattern and text.", "O(n + m)", "O(n + m)", "Strings/ZAlgorithm/ZAlgorithm.py"));
        items.add(a("reverse-linked-list", "Reverse Linked List", "Linked lists", "Rewire next pointers in place to reverse a singly linked list.", "O(n)", "O(1)", "LinkedList/ReverseLinkedList/ReverseLinkedList.py"));
        items.add(a("cycle-detection", "Floyd Cycle Detection", "Linked lists", "Move a slow and a fast pointer to detect whether links loop.", "O(n)", "O(1)", "LinkedList/CycleDetection/CycleDetection.py"));
        items.add(a("merge-sorted-lists", "Merge Sorted Lists", "Linked lists", "Stably weave two sorted linked lists into one ordered chain.", "O(n + m)", "O(1)", "LinkedList/MergeSortedLists/MergeSortedLists.py"));
        items.add(a("infix-to-postfix", "Infix to Postfix", "Stacks", "Use an operator stack to make precedence explicit in postfix form.", "O(n)", "O(n)", "Stack/InfixToPostfix/InfixToPostfix.py"));
        items.add(a("expression-evaluation", "Postfix Evaluation", "Stacks", "Evaluate postfix tokens with a stack of intermediate values.", "O(n)", "O(n)", "Stack/ExpressionEvaluation/ExpressionEvaluation.py"));
        items.add(a("balanced-parentheses", "Balanced Parentheses", "Stacks", "Push opening brackets and match each close against the latest opener.", "O(n)", "O(n)", "Stack/BalancedParentheses/BalancedParentheses.py"));
        items.add(a("circular-queue", "Circular Queue", "Queues", "Reuse fixed-capacity slots with head and tail indices that wrap around.", "O(1)", "O(capacity)", "Queue/CircularQueue/CircularQueue.py"));
        items.add(a("tree-traversals", "Tree Traversals", "Trees", "Visit a binary tree in preorder, inorder, or postorder.", "O(n)", "O(h)", "Trees/TreeTraversals/TreeTraversals.py"));
        items.add(a("level-order-traversal", "Level Order Traversal", "Trees", "Visit tree nodes breadth-first, one depth level at a time.", "O(n)", "O(w)", "Trees/LevelOrderTraversal/LevelOrderTraversal.py"));
        items.add(a("height-and-diameter", "Height & Diameter", "Trees", "Compute subtree heights and the longest path in one postorder pass.", "O(n)", "O(h)", "Trees/HeightAndDiameter/HeightAndDiameter.py"));
        items.add(a("binary-search-tree", "Binary Search Tree", "Trees", "Maintain ordered set semantics through insert, search, delete, and inorder.", "O(h)", "O(1)", "Trees/BinarySearchTree/BinarySearchTree.py"));
        items.add(a("min-heap", "Binary Min-Heap", "Heaps", "Keep the smallest value at the root through sift-up and sift-down.", "O(log n)", "O(1)", "Heaps/MinHeap/MinHeap.py"));
        items.add(a("bfs", "Breadth-First Search", "Graphs", "Explore a directed graph in layers from a chosen source.", "O(V + E)", "O(V + E)", "Graphs/BFS/BFS.py"));
        items.add(a("dfs", "Depth-First Search", "Graphs", "Follow one branch as far as possible before backtracking.", "O(V + E)", "O(V + E)", "Graphs/DFS/DFS.py"));
        items.add(a("topological-sort", "Topological Sort", "Graphs", "Order a directed acyclic graph so every edge points forward.", "O(V + E)", "O(V + E)", "Graphs/TopologicalSort/TopologicalSort.py"));
        items.add(a("dijkstra", "Dijkstra's Algorithm", "Graphs", "Expand the nearest unsettled vertex to find non-negative shortest paths.", "O(V² + E)", "O(V + E)", "Graphs/Dijkstra/Dijkstra.py"));
        items.add(a("kruskal", "Kruskal's Algorithm", "Graphs", "Build a minimum spanning forest by accepting the lightest safe edges.", "O(V + E log E)", "O(V + E)", "Graphs/Kruskal/Kruskal.py"));
        items.add(a("prim", "Prim's Algorithm", "Graphs", "Grow each forest component from its cheapest frontier edge.", "O(V² + E)", "O(V + E)", "Graphs/Prim/Prim.py"));
        items.add(a("bellman-ford", "Bellman–Ford", "Graphs", "Relax every edge repeatedly and detect source-reachable negative cycles.", "O(VE + V²)", "O(V + E)", "Graphs/BellmanFord/BellmanFord.py"));
        items.add(a("floyd-warshall", "Floyd–Warshall", "Graphs", "Improve every pair distance by allowing one more intermediate vertex.", "O(V³ + E)", "O(V²)", "Graphs/FloydWarshall/FloydWarshall.py"));
        items.add(a("activity-selection", "Activity Selection", "Greedy", "Choose the largest compatible set by finishing as early as possible.", "O(n log n)", "O(n)", "Greedy/ActivitySelection/ActivitySelection.py"));
        items.add(a("fractional-knapsack", "Fractional Knapsack", "Greedy", "Take the highest value-to-weight ratio while capacity remains.", "O(n log n)", "O(n)", "Greedy/FractionalKnapsack/FractionalKnapsack.py"));
        items.add(a("huffman-coding", "Huffman Coding", "Greedy", "Merge the least frequent symbols to produce a prefix-free codebook.", "O(K log K)", "O(K)", "Greedy/HuffmanCoding/HuffmanCoding.py"));
        items.add(a("fibonacci", "Fibonacci DP", "Dynamic programming", "Build Fibonacci values iteratively while retaining only the last two.", "O(n)", "O(1)", "DynamicProgramming/Fibonacci/Fibonacci.py"));
        items.add(a("knapsack-01", "0/1 Knapsack", "Dynamic programming", "Fill a capacity table while using every item at most once.", "O(nC)", "O(C)", "DynamicProgramming/Knapsack01/Knapsack01.py"));
        items.add(a("longest-common-subsequence", "Longest Common Subsequence", "Dynamic programming", "Reuse a two-string table to measure the longest ordered shared subsequence.", "O(mn)", "O(min(m,n))", "DynamicProgramming/LongestCommonSubsequence/LongestCommonSubsequence.py"));
        items.add(a("longest-increasing-subsequence", "Longest Increasing Subsequence", "Dynamic programming", "Maintain the smallest tail for each increasing subsequence length.", "O(n log n)", "O(n)", "DynamicProgramming/LongestIncreasingSubsequence/LongestIncreasingSubsequence.py"));
        items.add(a("coin-change", "Coin Change", "Dynamic programming", "Minimize the number of unlimited-use coins needed for an amount.", "O(kA)", "O(A)", "DynamicProgramming/CoinChange/CoinChange.py"));
        items.add(a("matrix-chain-multiplication", "Matrix Chain Multiplication", "Dynamic programming", "Choose a parenthesization that minimizes scalar multiplication work.", "O(n³)", "O(n²)", "DynamicProgramming/MatrixChainMultiplication/MatrixChainMultiplication.py"));
        items.add(a("n-queens", "N-Queens", "Backtracking", "Place one queen per row while pruning occupied columns and diagonals.", "O(n·n!)", "O(n)", "Backtracking/NQueens/NQueens.py"));
        items.add(a("sudoku-solver", "Sudoku Solver", "Backtracking", "Fill a valid 9×9 board using constraint checks and MRV search.", "O(81·9ᵉ)", "O(81 + e)", "Backtracking/SudokuSolver/SudokuSolver.py"));
        items.add(a("permutations-and-combinations", "Permutations & Combinations", "Backtracking", "Enumerate positional arrangements and increasing-index selections.", "Output-sensitive", "O(n)", "Backtracking/PermutationsAndCombinations/PermutationsAndCombinations.py"));
        items.add(a("traveling-salesman", "Traveling Salesman", "Branch & bound", "Find the exact minimum Hamiltonian cycle while pruning with a lower bound.", "O(n²·n!)", "O(n)", "BranchAndBound/TravelingSalesman/TravelingSalesman.py"));
        items.add(a("convex-hull", "Convex Hull", "Geometry", "Build the outer boundary with Andrew's monotone chain scan.", "O(n log n)", "O(n)", "DivideAndConquer/ConvexHull/ConvexHull.py"));
        ITEMS = Collections.unmodifiableList(items);
    }
}
