# Dynamic programming

Each algorithm directory contains standalone `Name.py`, `Name.java`, and
`Name.c` implementations with reusable functions and deterministic demos.
The demos contain real expected-result checks and never read interactive input.
Java helper types are nested within the matching public class.

## APIs and complexity

Space below excludes the caller's input. Except for Python Fibonacci, arithmetic
is bounded to the documented ranges and can be treated as constant cost.

| Directory | Python API | Java static API | Result | Time / auxiliary space |
| --- | --- | --- | --- | --- |
| `Fibonacci` | `fibonacci(n)` | `Fibonacci.fibonacci(n)` | `F(n)`, with `F(0)=0` | O(n) additions / O(1) integer slots |
| `Knapsack01` | `knapsack_01(weights, values, capacity)` | `Knapsack01.knapsack01(int[], int[], int)` | Maximum value, no item reconstruction | O((n+1)(C+1)) / O(C+1) |
| `LongestCommonSubsequence` | `lcs_length(a, b)` | `LongestCommonSubsequence.lcsLength(String, String)` | LCS **length** | O(mn) DP work / O(min(m,n)+1) |
| `LongestIncreasingSubsequence` | `lis_length(values)` | `LongestIncreasingSubsequence.lisLength(int[])` | Strict LIS **length**, using binary-searched tails | O(n log(n+1)) / O(n) |
| `CoinChange` | `min_coins(coins, amount)` | `CoinChange.minCoins(int[], int)` | **Minimum number of coins**, unlimited reuse; `-1` if impossible | O((k+1)(A+1)) / O(A+1) |
| `MatrixChainMultiplication` | `matrix_chain_cost(dimensions)` | `MatrixChainMultiplication.matrixChainCost(int[])` | Minimum scalar multiplication count, no actual matrix multiplication | O(n^3) / O(n^2) |

Knapsack/coin bounds include table initialization even for empty item/coin lists.
Validation adds linear input scanning; LCS scans the longer string even when
the shorter is empty, so its full bound is O(mn+m+n).
Python integer comparisons in LIS also depend on the supplied integers' bit size.

### Contracts and practical limits

- **Fibonacci:** Python accepts integer `n` in `0..10000` with arbitrary-precision
  results. Its bit complexity is O(n^2) time and O(n) space. Java returns `long`
  and permits `0..92`. C returns `unsigned long long` and permits `0..93`.
  Neither bounded implementation computes the overflowing next term.
- **Knapsack:** up to 1000 items, equal weight/value lengths, capacity `0..100000`,
  and each weight/value in `0..10^9`. Values are nonnegative. Empty items give
  zero. A zero-weight item contributes **once**, including at zero capacity;
  positive-weight items cannot be reused. Descending capacity updates enforce
  0/1 semantics. Totals are at most `10^12`; Java/C return 64-bit-capable values.
- **LCS:** two non-null strings of at most 2000 units each. Empty input gives zero.
  Python compares Unicode code points, Java UTF-16 code units, and C bytes of
  NUL-terminated strings. Use ASCII for identical cross-language semantics.
- **LIS:** at most 100000 integers; empty gives zero. Equal values do not extend
  a subsequence. Python accepts arbitrary-size integers; Java/C accept `int`.
- **Coin change:** at most 1000 denominations, each an integer in `1..10^9`;
  amount `0..100000`. Duplicate denominations are allowed and have no effect on
  the minimum. Empty coins give zero only for amount zero, otherwise `-1`.
  Zero/negative denominations are rejected even when the amount is zero.
- **Matrix chain:** `dimensions[i] x dimensions[i+1]` describes matrix i.
  At most 101 dimensions (100 matrices), all in `1..100000`. `[]`, `[d]`, and
  `[rows, cols]` have zero cost. Every supplied dimension is still validated.
  Any parenthesization uses at most 99 products, each at most `10^15`, so the
  total is at most `99*10^15`, safely below signed 64-bit maximum. Java also
  uses exact arithmetic guards; C checks intermediate additions/products.
  Dimensions outside these conservative limits are rejected rather than wrapped.

Python containers are lists or tuples (strings for LCS); integer parameters
reject booleans and non-integers with `ValueError`. Java uses
`IllegalArgumentException` for invalid inputs, including null arrays/strings.
Inputs are not modified. These are bounded educational APIs: the largest
accepted knapsack/coin problems can still require 100 million updates.

## C99 API and memory ownership

Target ordinary C99 implementations with at least 32-bit `int`/`size_t` and
at least 64-bit `long long`. No VLAs or compiler-specific integer extensions
are used. Callers must supply arrays of the stated lengths and real output
pointers. A null array is allowed only for a zero-length input; LCS requires
non-null, NUL-terminated strings, including for empty strings.

```c
int fibonacci(int n, unsigned long long *out);
int knapsack_01(const int *weights, const int *values, int n,
                int capacity, long long *out);
int lcs_length(const char *a, const char *b, int *out);
int lis_length(const int *values, int n, int *out);
int min_coins(const int *coins, int k, int amount, int *out);
int matrix_chain_cost(const int *dimensions, int dimension_count, long long *out);
```

All return `1` on successful computation, `0` on invalid input, and (where
allocation is needed) `-1` on allocation/size failure. Matrix chain reserves
`-2` for defensive overflow detection, unreachable under its accepted limits.
The output value is unchanged on errors. **Coin change's status `1` with
`*out == -1` means a valid but unreachable amount**, not allocation failure.
All internal heap allocations are size-checked and freed before returning;
no heap ownership passes to the caller. Negative sizes/capacities are rejected.

## Run demos and reuse functions

From the repository root, for example:

```sh
python DynamicProgramming/Knapsack01/Knapsack01.py
javac DynamicProgramming/Knapsack01/Knapsack01.java
java -cp DynamicProgramming/Knapsack01 Knapsack01
cc -std=c99 -Wall -Wextra -pedantic DynamicProgramming/Knapsack01/Knapsack01.c -o knapsack_demo
./knapsack_demo
```

Substitute any directory/basename from the table to run another demo. Python
imports have no demo side effects. Java checks explicitly throw `AssertionError`
and run without `-ea`. Keep Python optimization (`-O`) and C `NDEBUG` disabled
to retain their assertions. Each C file guards its demo with `ALGO_NO_MAIN`, so
it can be compiled with `-DALGO_NO_MAIN` or included in a small consumer that
defines that macro before the include. Keep these standalone examples in
separate translation units rather than concatenating their source.

The shared stdlib tests are in `tests/test_optimization.py`, using the
shared `tests/_loader.py`:

```sh
python -m unittest discover -s tests -p test_optimization.py
python -m pytest -q
```

Run `python tools/check_examples.py` to also check every Java and C demo.
