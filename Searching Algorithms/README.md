# Searching algorithms

Original space-containing folder names are preserved. Quote their paths in shell
commands. Each algorithm contains matching Python, Java, and C source files.

| Folder | Python API | Typical / worst search time | Extra space |
| --- | --- | --- | --- |
| `Linear Search` | `linear_search(arr, key)` | O(n) / O(n) | O(1) |
| `Binary Search` | `binary_search(arr, key)` | O(log n) / O(log n) | O(1) |
| `Jump Search` | `jump_search(arr, key)` | O(√n) / O(√n) | O(1) |
| `Interpolation Search` | `interpolation_search(arr, key)` | O(log log n) for uniform values / O(n) | O(1) |
| `Exponential Search` | `exponential_search(arr, key)` | O(log(i+1)) for a match near i / O(log n) | O(1) |

Bounds describe search only, not the demo's preliminary sorting. Binary and
exponential midpoint calculations and interpolation arithmetic use bounded
integer inputs; use Java/C arrays within practical memory limits.

## Contract

- Return a **zero-based index**, or `-1` when the key is absent.
- All APIs except Linear Search require **ascending sorted input**. They do not
  sort or mutate the input themselves. Demo programs sort before calling them,
  so their printed index refers to the sorted array, not the entered order.
- Linear Search returns the first match in the original array. Other algorithms
  may return any matching index when duplicates exist.
- Empty inputs return `-1`. Uniform arrays are valid, including Interpolation
  Search (which avoids a zero denominator).
- C drivers accept at most 100 values and check input counts. Java/C keys and
  values must fit `int`. Python accepts arbitrary-precision integers.

## Running and input formats

From the repository root:

```sh
python "Searching Algorithms/Binary Search/BinarySearch.py"
javac -encoding UTF-8 "Searching Algorithms/Binary Search/BinarySearch.java"
java -cp "Searching Algorithms/Binary Search" BinarySearch
cc -std=c99 -Wall -Wextra "Searching Algorithms/Binary Search/BinarySearch.c" -lm -o binary-demo.out
./binary-demo.out
```

- **Python:** every search offers menu `1` custom input, `2` examples, `3` exit.
- **Java:** Binary Search offers the menu; the other searches use direct input.
- **C:** every search uses direct input.
- **Direct input:** enter `n`, the `n` integers, then the search key. For example,
  the tokens `5 9 1 7 3 5 7` search for `7` in five values; Binary Search reports
  index `3` in the sorted array `[1, 3, 5, 7, 9]`.
- **Menu custom input:** enter `1`, then the direct-input tokens, then `3` to exit.
  Python/Java menus expect well-formed numeric input.

Compile Java examples individually: they reuse the helper class name `Searching`.
`-lm` is needed for Jump Search on platforms where `sqrt` requires a separate
math library. All Python modules can be imported without launching a menu.

Tests: `python -m unittest discover -s tests -p test_sorting_searching.py`.
All-language checks: `python tools/check_examples.py`.
