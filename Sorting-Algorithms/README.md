# Sorting algorithms

The original algorithm folders and filenames are preserved. Each folder contains
a standalone Python, Java, and C program. Python's bubble-sort filename is
`BubbleSort/Bubble-Sort.py`; all other basenames match the algorithm folder.

## Algorithms and complexity

All algorithms sort in ascending order and mutate the supplied array/list.
Do not rely on a common return value: most return nothing; Python Bubble Sort
also returns the same list. `n` is the number of values, `k = max - min + 1`,
and `d` is the number of decimal digits.

| Folder | Python API | Average / worst time | Auxiliary space |
| --- | --- | --- | --- |
| `BubbleSort` | `Sorting.bubble_sort(arr)` | O(n²) / O(n²); best O(n) | O(1) |
| `SelectionSort` | `selection_sort(arr)` | O(n²) / O(n²) | O(1) |
| `InsertionSort` | `insertion_sort(arr)` | O(n²) / O(n²); best O(n) | O(1) |
| `MergeSort` | `merge_sort(arr, 0, len(arr)-1)` | O(n log n) / O(n log n) | O(n) |
| `QuickSort` | `quick_sort(arr, 0, len(arr)-1)` | O(n log n) / O(n²) | O(log n) average, O(n) worst stack |
| `HeapSort` | `heap_sort(arr)` | O(n log n) / O(n log n) | O(log n) recursive heapify stack |
| `CountingSort` | `counting_sort(arr)` | O(n+k) | O(k) |
| `RadixSort` | `radix_sort(arr)` | O(d(n+10)) | O(n+10) |
| `BucketSort` | `bucket_sort(arr)` | Distribution/sort dependent; see below | Python/Java O(n), C O(n²) |

Bucket Sort distributes into `n` buckets using an integer range offset. Python
and Java use library sorting inside buckets, giving O(n log n) worst time;
C uses insertion sort, giving O(n²) worst time. Balanced bucket populations give
approximately linear distribution/merge work. C reserves a bounded teaching
matrix rather than dynamically growing buckets.

## Input contracts

- Empty arrays, duplicates, zero, and sorted/reversed inputs are supported.
- Comparison sorts and Bucket Sort accept signed integers.
- Counting Sort accepts signed integers, but rejects a value range wider than
  1,000,000 instead of attempting an unbounded allocation.
- Radix Sort accepts **nonnegative integers only**, rejecting negatives before
  modifying the input. Java/C handle the largest signed 32-bit integer without
  overflowing the final digit exponent.
- All original C demos accept `0 <= n <= 100`; Merge Sort's temporary buffer and
  Radix Sort's counting buffer share that bound. Call those C functions only
  within their documented buffer limits. The C Counting/Bucket/Radix routines
  terminate with a diagnostic on unsupported ranges/capacities or allocation
  failure; they retain the original `void` interfaces.
- Java/C inputs must fit their `int` type. Python uses arbitrary-precision
  integers, whose arithmetic cost grows with their bit length.
- The last-element pivot Quick Sort intentionally demonstrates a simple
  partition scheme. Large sorted/equal inputs have quadratic work and can exceed
  the recursive stack limit; it is not intended as a production sort.
- Python/Java menus expect well-formed numeric input; they are teaching drivers,
  not general parsers. C drivers check input counts and stop on malformed tokens.

## Run an example

From the repository root:

```sh
python Sorting-Algorithms/MergeSort/MergeSort.py
javac -encoding UTF-8 Sorting-Algorithms/MergeSort/MergeSort.java
java -cp Sorting-Algorithms/MergeSort MergeSort
cc -std=c99 -Wall -Wextra Sorting-Algorithms/MergeSort/MergeSort.c -o merge-demo.out
./merge-demo.out
```

All Python/Java sorts, and C sorts except Bucket/Radix, have a menu:
`1` custom input, `2` example cases, `3` exit. Custom input is `n`, then `n`
individual integer tokens. C Bucket/Radix read `n`, then the values directly,
without a menu. Compile Java programs separately because they repeat the
package-private helper name `Sorting`.

Tests: `python -m unittest discover -s tests -p test_sorting_searching.py`.
Use `python tools/check_examples.py` to also compile/run C and Java regression cases.
