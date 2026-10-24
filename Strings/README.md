# Literal string matching

`NaivePatternMatching`, `KMP`, `RabinKarp`, and `ZAlgorithm` each contain matching
PascalCase `.py`, `.java`, and `.c` filenames. Every file is independent, runs a
deterministic demo without input, and includes assertion-based checks.

## Shared API and behavior

Python: `find_matches(text, pattern) -> list[int]` in each module.
Java: `ClassName.findMatches(String text, String pattern) -> List<Integer>`.

```python
find_matches("aaaa", "aa")   # [0, 1, 2] -- overlaps included
find_matches("ab", "")       # [0, 1, 2] -- every boundary
find_matches("", "")         # [0]
find_matches("", "x")        # []
find_matches("abc", "abcd")  # []
find_matches("a\0a\0", "a\0") # [0, 2] -- NUL is ordinary input
```

Results are ascending, zero-based offsets. Matching is literal and
case-sensitive: no regex, normalization, or case folding. Python requires `str`
arguments (`TypeError` otherwise); Java rejects null with `NullPointerException`.
There are no caller-supplied lengths in these two languages.

**Index units differ:** Python uses Unicode code points; Java uses UTF-16 code
units, so a supplementary character occupies two positions; C uses bytes.
For example, matching `"a"` in `"😀a"` yields Python index 1 and Java index 2.
C operating on UTF-8 bytes yields byte offset 4. ASCII offsets agree across all
three languages. Empty-pattern boundaries follow each language's index units.

## Algorithms and complexity

Let n be text length, m pattern length, k returned matches, and h hash hits.

| Algorithm | Method | Time | Working space, excluding result |
| --- | --- | --- | --- |
| Naive | Compare each possible alignment | O(n*m+n+m) worst case | O(1) |
| KMP | Prefix/suffix table; retain borders on mismatch and after matches | O(n+m) | O(m) |
| Rabin-Karp | Rolling polynomial hash, then exact verification | O(n+m+h*m), worst O(n*m+n+m) | O(1) |
| Z algorithm | Prefix-match lengths over pattern + separator + text | O(n+m) | O(n+m) |

All return the n+1 boundaries in O(n+1) time for an empty pattern. Python/Java
results use O(k) space. C deliberately allocates capacity n+1 for a simple safe
output contract (O(n+1) space), except when m > n, when no buffer is needed.
Memory availability can impose lower limits than the integer bounds below.

Rabin-Karp uses base 257 and modulus 1,000,000,007; every hash hit is verified,
so collisions affect speed, never correctness. Repetitive matches may take
quadratic time. Java uses bounded `long` intermediates; C reduces operands
before `uint64_t` multiplication. Python integers are arbitrary precision.

Z matching never relies on a character being absent from the input: Python uses
`None` between character lists, Java uses a virtual integer -1 symbol, and C
compares the virtual separator by position. NUL, `$`, and all byte/character
values remain valid input. Java rejects nontrivial combined lengths n+m+1
greater than `Integer.MAX_VALUE` with `IllegalArgumentException`.

## C99 API, ownership, and limits

Each C file exposes the same independent API:

```c
int find_matches(const unsigned char *text, size_t n,
                 const unsigned char *pattern, size_t m,
                 size_t **matches, size_t *count);
```

- Explicit byte lengths permit embedded NULs and do not require terminators.
  A data pointer may be `NULL` only when its corresponding length is zero.
  Pointers must actually cover their declared lengths; C cannot check that.
- `matches` and `count` must be writable output pointers, separate from input
  storage. Pass a fresh result variable. With valid output pointers, outputs are
  initialized to `NULL`/0 before validation. Return `1` on success, including
  no matches; `0` for invalid arguments, unsupported sizes, or allocation failure.
- Read only the first `*count` entries of `*matches`. Always `free(*matches)`
  after success, even when count is zero; `free(NULL)` is valid. The routines
  release temporary tables and any partial allocations on failure.
- Lengths are nonnegative `size_t` values. When m <= n, require n < `SIZE_MAX`
  and n+1 <= `SIZE_MAX / sizeof(size_t)` for the output buffer. KMP also checks
  its m-entry table. Z checks n+m+1 addition and the table's allocation product.
  Inputs too large for checked arithmetic are rejected before indexing them.
- C uses C99 `size_t` arithmetic, and Rabin-Karp requires `uint64_t`. No input
  buffers are written and no unchecked fixed-capacity output buffers are used.

## Run

For example, from `Strings/KMP`:

```text
python KMP.py
javac KMP.java
java -ea KMP
cc -std=c99 -Wall -Wextra -pedantic KMP.c -o kmp
./kmp
```

Keep Python assertions enabled; use Java `-ea` and C without `-DNDEBUG`.
Substitute the other algorithm names to run their demos. Python regression
tests use `tests/_loader.py`; from the repository root run
`python -m unittest discover -s tests -p "test_foundations.py"`.
