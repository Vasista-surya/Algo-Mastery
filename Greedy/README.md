# Greedy algorithms

```text
Greedy/
  ActivitySelection/ActivitySelection.{py,java,c}
  FractionalKnapsack/FractionalKnapsack.{py,java,c}
  HuffmanCoding/HuffmanCoding.{py,java,c}
```

Each brace expansion denotes three standalone files. Python exposes reusable
functions; Java uses a public class matching the filename, with nested helpers;
C is C99. Every file runs a deterministic demo and meaningful assertions without
input. Java self-checks need `-ea`; C needs assertions enabled (no `NDEBUG`).
Inputs are not mutated. Python imports do not run demos. All algorithms have
deterministic tie rules.

## Activity selection

Choose a maximum-size set of mutually compatible activities, not a maximum-value
set. Each activity is `(start, finish)` with **integer `start < finish`**. Negative
times are valid; empty/zero-duration intervals are deliberately rejected. Touching
endpoints are compatible: `next_start >= previous_finish`. Sort by
`(finish, start, original_index)` and return **original indices in scheduled order**.
Empty input returns an empty selection.

- Python: `activity_selection(activities) -> list[int]`; accepts an iterable of
  pairs, arbitrary-size integer times (not bool). Invalid intervals: `ValueError`.
- Java: `ActivitySelection.activitySelection(Activity[] activities) -> List<Integer>`;
  nested `Activity(long start, long finish)`. Invalid/null input:
  `IllegalArgumentException`. Comparisons avoid subtraction overflow.
- C: nested records are ordinary `Activity { long long start, finish; }` structs:

```c
int activity_selection(const Activity *activities, size_t n,
                       size_t *selected, size_t capacity, size_t *count);
```

C permits `n <= 4096`; output needs `n` `size_t` slots. `count` is mandatory.
Status `0` success, `-1` invalid interval/input/limit, `-2` missing or short output.
No time arithmetic is performed, so full `long long` endpoints are supported.

```python
from Greedy.ActivitySelection.ActivitySelection import activity_selection

assert activity_selection([(5, 9), (1, 2), (3, 4), (0, 6), (5, 7), (8, 9)]) == [1, 2, 4, 5]
```

Time `O(N log N)`, space `O(N)`. For C, the sorting term assumes `qsort` has that
complexity; ISO C does not specify its worst-case complexity.

## Fractional knapsack

Items are **divisible**, with `(value, weight)` integer pairs, `value >= 0`,
`weight > 0`; capacity is a nonnegative integer. This is not 0/1 knapsack.
Return the total value and the fraction of **each item in original input order**.
Sort by decreasing value/weight; ratio ties use original index. Zero-value items
are skipped. Empty items and zero capacity are valid, but invalid items are still
validated when capacity is zero.

- Python: `fractional_knapsack(items, capacity) -> (Fraction total, list[Fraction] shares)`.
  Uses stdlib `fractions.Fraction` for exact ratios, shares and totals. Arbitrarily
  large integers are supported; booleans/floats/negative values/zero weights raise
  `ValueError`. `items` may be an iterable of pairs.
- Java: `FractionalKnapsack.fractionalKnapsack(Item[] items, long capacity) -> Result`.
  Nested `Item(long value, long weight)`; `Result` has `double total`, `double[] shares`.
  Value/capacity must be `0..10^9`, weight `1..10^9`; invalid/null inputs throw
  `IllegalArgumentException`. Ratios compare exact bounded long cross-products
  (at most `10^18`); shares/totals are approximate doubles.
- C: `Item { long long value, weight; }`, same numeric bounds as Java, `n <= 4096`:

```c
int fractional_knapsack(const Item *items, size_t n, long long capacity,
                        double *shares, size_t shares_capacity, double *total);
```

C output needs `n` double slots and a nonnull `total`. Status `0` success,
`-1` invalid input/domain, `-2` short/missing shares buffer. Bounded cross-products
fit `long long`; bounded totals remain finite. Compare floating results with a
tolerance rather than expecting bitwise equality with Python rational results.

```python
from fractions import Fraction
from Greedy.FractionalKnapsack.FractionalKnapsack import fractional_knapsack

assert fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50) == (240, [1, 1, Fraction(2, 3)])
assert fractional_knapsack([(8, 3)], 1) == (Fraction(8, 3), [Fraction(1, 3)])
```

Time `O(N log N)`, space `O(N)` excluding arbitrary-precision arithmetic costs.
C's sorting bound has the same `qsort` qualification as activity selection.

## Huffman coding

Build a binary prefix-free codebook minimizing frequency-weighted code length.
Merge ties compare `(frequency, smallest_symbol_in_subtree)`; the first removed
subtree gets bit `0`, the second gets `1`. This makes results independent of mapping
insertion order. It is a deterministic Huffman tree, not a canonical-code format.

- Empty alphabet: empty codebook; only empty text/bitstreams are valid.
- Single symbol: code **`"0"`**, so repetition count is preserved.
- Python/Java frequency entries must be strictly positive; omit absent symbols.
  C uses a full histogram, where zero explicitly means absent.
- Unknown symbols, nonbinary bits, impossible paths and truncated final codewords
  are rejected. Python/Java also validate supplied external codebooks for nonempty
  binary codewords, duplicate words, and prefix collisions. A bitstream alone does
  not carry the codebook; decoding needs the same codebook.
- Python symbols are single-character strings (Unicode code points), Java symbols
  are UTF-16 `char` units, C symbols are unsigned bytes. ASCII alphabets with the
  same frequencies produce matching codewords across languages. Other alphabets
  require an explicitly chosen text encoding when moving data between languages.

### Python

```python
huffman_codes(frequencies)  # {single-character str: positive int} -> {str: bitstring}
encode(text, codes)         # str -> '0'/'1' bitstring
decode(bits, codes)         # complete bitstring -> str
```

Invalid domains/codebooks/streams raise `ValueError`; non-mapping frequency or
codebook inputs are outside the contract. Frequencies are arbitrary-precision
integers, with booleans rejected.

```python
from Greedy.HuffmanCoding.HuffmanCoding import huffman_codes, encode, decode

codes = huffman_codes({"a": 5, "b": 2, "c": 1})
assert codes == {"a": "1", "b": "01", "c": "00"}
assert decode(encode("abaca", codes), codes) == "abaca"
assert huffman_codes({"x": 7}) == {"x": "0"}
```

### Java

```java
Map<Character, String> HuffmanCoding.huffmanCodes(Map<Character, Long> frequencies);
String HuffmanCoding.encode(String text, Map<Character, String> codes);
String HuffmanCoding.decode(String bits, Map<Character, String> codes);
```

These are API signatures (omit the class qualifier when declaring methods).
Frequencies are positive longs with total at most `Long.MAX_VALUE`; merging uses
`Math.addExact`, throwing `ArithmeticException` on overflow. Invalid/null data
throws `IllegalArgumentException`. Results are sorted by character for printing.
Helpers are nested and traversal is iterative.

### C99

`Huffman` contains its tree and `codes[256][256]`. Call `huffman_build` successfully
before use and keep that object unmodified. `codes[byte]` is a NUL-terminated
codeword, or empty for an absent symbol. No external-codebook import API is offered.

```c
int huffman_build(const unsigned long long *frequencies, size_t count, Huffman *book);
int huffman_encode(const Huffman *book, const unsigned char *text, size_t length,
                   char *bits, size_t capacity, size_t *bit_count);
int huffman_decode(const Huffman *book, const char *bits, size_t bit_count,
                   unsigned char *text, size_t capacity, size_t *length);
```

- Requires 8-bit bytes (checked at compile time). `count` must equal 256; the
  histogram may be all zero. Total frequency must fit `ULLONG_MAX`; unsigned
  frequencies cannot represent negative values.
- At most 511 nodes and 255 bits per codeword; 256-character slots include the
  NUL terminator. Tree and codebook storage are bounded (roughly 80 KiB on common
  platforms); no recursion or heap allocation is used.
- Encoding accepts raw bytes with explicit length (embedded NUL bytes work).
  Encoded output is ASCII bits **with a NUL terminator**. Capacity includes that
  terminator; `bit_count` does not. Even an empty encoding needs one output byte.
  Required size addition is overflow-checked before writing.
- Decoding takes an explicit bit count, ignoring any trailing string terminator.
  Output is raw bytes **without a terminator**; `length` reports the byte count.
  Empty decode needs no output buffer. Null input is allowed for a zero input length.
- Scalar count/length pointers are mandatory. Status `0` success, `-1` invalid
  input/unknown symbol/invalid stream, `-2` missing or short output buffer,
  `-3` frequency/size overflow. Ignore outputs on any failure. A failed build
  leaves `book.valid == 0`.

### Huffman complexity

Let `K` be the alphabet size, `S` the sum of all codeword lengths, `L` the number
of text symbols, and `B` the number of encoded bits.

| Operation | Time | Space |
| --- | --- | --- |
| Python/Java build (heap) | `O(K log K + S)` | `O(K+S)` |
| C build (linear minimum selection) | `O(256 + K^2 + S)` | fixed tree/codebook capacities |
| Python/Java encode/decode, including codebook validation | `O(S+B+L)` | `O(S+B+L)` including output |
| C encode | `O(B+L)` | caller's output, constant auxiliary space |
| C decode | `O(B)` | caller's output, constant auxiliary space |

`S` can be quadratic in `K` for very skewed trees; codeword materialization is
included in these bounds. Python integer arithmetic adds bit-length costs.

## C ownership and running examples

All C routines use checked fixed capacities, caller-owned buffers and bounded
workspace. There are no allocations to free. Activity/knapsack input or array
output pointers may be null only for `n == 0`; scalar output pointers are mandatory.
Inputs, outputs, scalar outputs and the Huffman object must not overlap. Callers
must supply valid storage for stated lengths/capacities. Define `ALGORITHM_NO_MAIN`
to include an individual C file in a custom driver; each example has independent
types/constants. Do not concatenate independent C examples into one translation unit.

Commands to run from the repository root:

```text
python Greedy/HuffmanCoding/HuffmanCoding.py
javac Greedy/HuffmanCoding/HuffmanCoding.java
java -ea -cp Greedy/HuffmanCoding HuffmanCoding
cc -std=c99 -Wall -Wextra -pedantic Greedy/HuffmanCoding/HuffmanCoding.c -o huffman-demo
./huffman-demo
python -m unittest discover -s tests -p "test_graphs_greedy.py"
python -m pytest -q
```

Replace the algorithm name for other demos. The stdlib test suite depends on the
shared `tests/_loader.py`. Run `python tools/check_examples.py` to also check
every Java and C demo.
