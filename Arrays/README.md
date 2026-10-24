# Array techniques

Each algorithm directory contains independent `Name.py`, `Name.java`, and
`Name.c` programs. Running a file prints a deterministic example and performs
assertion-based self-checks. No input is requested. Python APIs use snake_case;
Java uses the corresponding camelCase static methods on the filename's class.
Inputs are not modified.

| Directory | Python API and example | Time | Extra space |
| --- | --- | --- | --- |
| `Kadane` | `max_subarray([-2, 1, -3, 4, -1, 2, 1]) == 6` | O(n) | O(1) |
| `PrefixSum` | `p = prefix_sums([2, -1, 3, 5])`; `range_sum(p, 1, 3) == 2` | O(n) build; O(1) query | O(n) build; O(1) query |
| `SlidingWindow` | `max_window_sum([2, -1, 3, 5], 2) == 8` | O(n) | O(1) |
| `TwoPointers` | `two_sum_sorted([-4, -1, 0, 3, 5], 2) == (1, 3)` | O(n), including validation | O(1) |

## Contracts and boundaries

- **Kadane:** maximum **nonempty** contiguous subarray sum. Empty input is
  invalid; all-negative input returns its largest element, not zero.
- **Prefix sums:** returns `n + 1` entries, starting with zero, even for empty
  input (`[0]`). Ranges are half-open `[start, end)` with
  `0 <= start <= end <= n`; an empty range returns zero. Queries expect an
  unmodified builder result and validate the bounds/leading zero, rather than
  rescanning all entries. Python also validates the accessed entry types.
- **Sliding window:** maximum sum of **exactly** `width` consecutive elements.
  Require `1 <= width <= n`; zero/negative/oversized widths and empty arrays are
  invalid. Negative maximum sums are retained.
- **Two pointers:** require nondecreasing input; duplicates are allowed and
  unsorted input is rejected. Return distinct zero-based indices `left < right`,
  not values. Start at both ends, move left for a too-small sum and right for a
  too-large sum, and return the first equality encountered. This is deterministic
  but not a promise of the lexicographically first pair. No pair (including
  empty/singleton input) is `None` in Python or `null` in Java.

Python expects sequences of built-in integers (not floats or bools), with integer
widths/bounds/targets. Integer arithmetic has arbitrary precision. Invalid integer
types raise `TypeError`; invalid sizes, ranges and ordering raise `ValueError`.
The stated complexities count integer arithmetic as constant time; very large
Python integers incur additional bit-arithmetic costs.

Java accepts `int[]` and returns `long` sums / `long[]` prefixes. Two-sum accepts
a `long` target and returns an `int[2]`. Null arrays raise `NullPointerException`;
invalid sizes/ranges/order raise `IllegalArgumentException`. Widened sums of any
Java int array fit in `long`; prefix construction rejects a length that cannot
accommodate the extra entry. `rangeSum` uses checked subtraction, so malformed
caller-crafted prefixes can raise `ArithmeticException`.

## C99 APIs and limits

```c
int max_subarray(const int32_t *values, size_t n, int64_t *result);
int prefix_sums(const int32_t *values, size_t n, int64_t **out);
int range_sum(const int64_t *prefix, size_t length,
              size_t start, size_t end, int64_t *out);
int max_window_sum(const int32_t *values, size_t n, size_t width, int64_t *result);
int two_sum_sorted(const int32_t *values, size_t n, int64_t target,
                   size_t *left_index, size_t *right_index);
```

- Requires C99 with `int32_t`/`int64_t`. All input lengths are limited to
  `INT32_MAX`; with 32-bit elements this keeps every running/subarray sum inside
  signed 64-bit range. Two-sum widens **before** adding. Prefix queries check
  subtraction overflow even for malformed prefix values.
- Pointers must reference the stated number of live elements; C cannot inspect
  the underlying allocation length. Output pointers must be writable and must
  not overlap input storage. The two index-output pointers must be distinct.
- Null data pointers are allowed only for zero-length input. Kadane and sliding
  windows still reject empty input. Output pointers are always required.
  Sizes use `size_t`; pass nonnegative lengths, never a negative signed value.
- Most APIs return `1` on success and `0` on invalid input or allocation failure.
  Two-sum returns `1` found, `0` absent, `-1` invalid. Scalar/index outputs stay
  unchanged on failure or no match.
- `prefix_sums` initializes `*out` to `NULL`, checks allocation-size arithmetic,
  and allocates `n + 1` entries on success. Pass a fresh output variable and
  `free(*out)` after use (also for empty input). `range_sum` takes this array's
  length, **n + 1**, not n. Other algorithms do not allocate.

## Run examples

From `Arrays/Kadane` (substitute the other directory/class names):

```text
python Kadane.py
javac Kadane.java
java -ea Kadane
cc -std=c99 -Wall -Wextra -pedantic Kadane.c -o kadane
./kadane
```

Keep Python assertions enabled, enable Java assertions with `-ea`, and compile C
without `-DNDEBUG`. Platform-specific executable invocation may differ.
Python regression tests are in `tests/test_foundations.py` and use the repository's
`tests/_loader.py`; run discovery from the root with
`python -m unittest discover -s tests -p "test_foundations.py"`.
