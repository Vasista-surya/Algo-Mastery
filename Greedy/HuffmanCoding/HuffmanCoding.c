/* C99 Huffman for 256 byte symbols (requires 8-bit unsigned char).
 * Histogram: 256 unsigned long long frequencies; zero means absent.
 * Empty supported; singleton code "0"; ties (frequency,minimum byte).
 * Frequency sum must fit ULLONG_MAX. Build O(K^2+S), S=sum code lengths,
 * using linear minimum selection; encode O(B+L), decode O(B).
 * Fixed caller-owned Huffman stores <=511 nodes and 256 code slots of 256
 * chars (max length 255 + NUL). No allocation/free or recursion.
 * 0 success, -1 invalid, -2 output capacity, -3 numeric/size overflow.
 * Codec requires an unmodified, successfully built Huffman object.
 * Inputs/outputs/object must not overlap. Ignore output on nonzero status.
 */
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#if UCHAR_MAX != 255
#error "HuffmanCoding requires 8-bit bytes"
#endif

enum { SYMBOLS = 256, MAX_NODES = 511, CODE_CAPACITY = 256 };
typedef struct {
    unsigned long long frequency;
    int minimum, symbol, left, right, parent;
} HuffmanNode;
typedef struct {
    HuffmanNode nodes[MAX_NODES];
    char codes[SYMBOLS][CODE_CAPACITY];
    int root, node_count, valid;
} Huffman;

static int minimum_node(const Huffman *book, const int *active) {
    int best = -1;
    for (int i = 0; i < book->node_count; ++i)
        if (active[i] && (best == -1 ||
            book->nodes[i].frequency < book->nodes[best].frequency ||
            (book->nodes[i].frequency == book->nodes[best].frequency &&
             book->nodes[i].minimum < book->nodes[best].minimum))) best = i;
    return best;
}

int huffman_build(const unsigned long long *frequencies, size_t count, Huffman *book) {
    int active[MAX_NODES] = {0}, remaining = 0;
    if (!book) return -1;
    memset(book, 0, sizeof(*book));
    book->root = -1;
    if (!frequencies || count != SYMBOLS) return -1;
    for (int symbol = 0; symbol < SYMBOLS; ++symbol) {
        if (frequencies[symbol]) {
            int i = book->node_count++;
            HuffmanNode node = {frequencies[symbol], symbol, symbol, -1, -1, -1};
            book->nodes[i] = node;
            active[i] = 1;
            ++remaining;
        }
    }
    while (remaining > 1) {
        int left = minimum_node(book, active), right, index;
        unsigned long long sum;
        if (left < 0) return -1;
        active[left] = 0;
        right = minimum_node(book, active);
        if (right < 0) return -1;
        active[right] = 0;
        if (book->nodes[left].frequency > ULLONG_MAX - book->nodes[right].frequency) return -3;
        sum = book->nodes[left].frequency + book->nodes[right].frequency;
        if (book->node_count >= MAX_NODES) return -1;
        index = book->node_count++;
        book->nodes[index].frequency = sum;
        book->nodes[index].minimum = book->nodes[left].minimum < book->nodes[right].minimum
            ? book->nodes[left].minimum : book->nodes[right].minimum;
        book->nodes[index].symbol = -1;
        book->nodes[index].left = left; book->nodes[index].right = right;
        book->nodes[index].parent = -1;
        book->nodes[left].parent = index; book->nodes[right].parent = index;
        active[index] = 1;
        --remaining;
    }
    book->root = minimum_node(book, active);
    for (int i = 0; i < book->node_count; ++i) {
        if (book->nodes[i].symbol >= 0) {
            char reverse[CODE_CAPACITY];
            size_t length = 0;
            int node = i, symbol = book->nodes[i].symbol;
            while (book->nodes[node].parent != -1) {
                int parent = book->nodes[node].parent;
                if (length >= CODE_CAPACITY - 1) return -1;
                reverse[length++] = book->nodes[parent].left == node ? '0' : '1';
                node = parent;
            }
            if (!length) reverse[length++] = '0';
            for (size_t j = 0; j < length; ++j) book->codes[symbol][j] = reverse[length - 1 - j];
            book->codes[symbol][length] = '\0';
        }
    }
    book->valid = 1;
    return 0;
}

static int valid_book(const Huffman *book) {
    return book && book->valid == 1 && book->node_count >= 0 && book->node_count <= MAX_NODES &&
        ((book->node_count == 0 && book->root == -1) ||
         (book->node_count > 0 && book->root >= 0 && book->root < book->node_count));
}

static size_t code_length(const char *code) {
    size_t length = 0;
    while (length < CODE_CAPACITY && code[length]) {
        if (code[length] != '0' && code[length] != '1') return 0;
        ++length;
    }
    return length < CODE_CAPACITY ? length : 0;
}

/* NUL-terminated ASCII bits; capacity includes terminator, *bit_count excludes it.
 * Even empty encoding requires capacity >= 1. Text is raw bytes, length explicit.
 */
int huffman_encode(const Huffman *book, const unsigned char *text, size_t length,
                   char *bits, size_t capacity, size_t *bit_count) {
    size_t required = 0, position = 0;
    if (!bit_count) return -1;
    *bit_count = 0;
    if (!valid_book(book) || (length && !text)) return -1;
    for (size_t i = 0; i < length; ++i) {
        size_t size = code_length(book->codes[text[i]]);
        if (!size) return -1;
        if (required > SIZE_MAX - size) return -3;
        required += size;
    }
    if (required == SIZE_MAX) return -3;
    if (!bits || capacity < required + 1) return -2;
    for (size_t i = 0; i < length; ++i) {
        size_t size = code_length(book->codes[text[i]]);
        memcpy(bits + position, book->codes[text[i]], size);
        position += size;
    }
    bits[required] = '\0';
    *bit_count = required;
    return 0;
}

/* Decoded raw bytes, NOT NUL-terminated. Capacity and *length are in bytes.
 * Empty streams require no output buffer. Truncated/nonbinary streams fail.
 */
int huffman_decode(const Huffman *book, const char *bits, size_t bit_count,
                   unsigned char *text, size_t capacity, size_t *length) {
    size_t written = 0;
    int node;
    if (!length) return -1;
    *length = 0;
    if (!valid_book(book) || (bit_count && !bits)) return -1;
    if (book->root == -1) return bit_count ? -1 : 0;
    node = book->root;
    for (size_t i = 0; i < bit_count; ++i) {
        int symbol;
        if (bits[i] != '0' && bits[i] != '1') return -1;
        if (book->nodes[book->root].symbol >= 0) {
            if (bits[i] != '0') return -1;
        } else {
            node = bits[i] == '0' ? book->nodes[node].left : book->nodes[node].right;
            if (node < 0 || node >= book->node_count) return -1;
        }
        symbol = book->nodes[node].symbol;
        if (symbol >= 0) {
            if (symbol >= SYMBOLS) return -1;
            if (!text || written >= capacity) return -2;
            text[written++] = (unsigned char)symbol;
            node = book->root;
        }
    }
    if (node != book->root) return -1;
    *length = written;
    return 0;
}

#ifndef ALGORITHM_NO_MAIN
int main(void) {
    unsigned long long frequencies[SYMBOLS] = {0};
    Huffman book;
    char bits[64];
    unsigned char decoded[16];
    size_t bit_count, length;
    int status;
    frequencies['a'] = 5; frequencies['b'] = 2; frequencies['c'] = 1;
    status = huffman_build(frequencies, SYMBOLS, &book);
    assert(status == 0);
    if (status != 0) return 1;
    status = huffman_encode(&book, (const unsigned char *)"abaca", 5, bits, sizeof(bits), &bit_count);
    assert(status == 0);
    if (status != 0) return 1;
    status = huffman_decode(&book, bits, bit_count, decoded, sizeof(decoded), &length);
    assert(status == 0 && length == 5 && memcmp(decoded, "abaca", 5) == 0);
    if (status != 0) return 1;
    printf("Codes: a=%s b=%s c=%s; encoded: %s\n", book.codes['a'], book.codes['b'], book.codes['c'], bits);
    assert(huffman_encode(&book, (const unsigned char *)"a", 1, bits, 1, &bit_count) == -2);
    assert(huffman_encode(&book, (const unsigned char *)"x", 1, bits, sizeof(bits), &bit_count) == -1);
    assert(huffman_decode(&book, "2", 1, decoded, sizeof(decoded), &length) == -1);
    assert(huffman_decode(&book, "0", 1, decoded, sizeof(decoded), &length) == -1);
    memset(frequencies, 0, sizeof(frequencies));
    status = huffman_build(frequencies, SYMBOLS, &book);
    assert(status == 0 && book.root == -1);
    if (status != 0) return 1;
    assert(huffman_decode(&book, NULL, 0, NULL, 0, &length) == 0 && length == 0);
    frequencies['x'] = 7;
    status = huffman_build(frequencies, SYMBOLS, &book);
    assert(status == 0 && strcmp(book.codes['x'], "0") == 0);
    if (status != 0) return 1;
    assert(huffman_decode(&book, "000", 3, decoded, sizeof(decoded), &length) == 0 && length == 3);
    assert(memcmp(decoded, "xxx", 3) == 0);
    frequencies['x'] = ULLONG_MAX; frequencies['y'] = 1;
    assert(huffman_build(frequencies, SYMBOLS, &book) == -3);
    memset(frequencies, 0, sizeof(frequencies));
    frequencies['a'] = 1; frequencies['b'] = 1;
    status = huffman_build(frequencies, SYMBOLS, &book);
    assert(status == 0 && strcmp(book.codes['a'], "0") == 0 && strcmp(book.codes['b'], "1") == 0);
    if (status != 0) return 1;
    {
        unsigned char all_bytes[SYMBOLS], restored[SYMBOLS];
        char all_bits[SYMBOLS * 8 + 1];
        for (int i = 0; i < SYMBOLS; ++i) {
            frequencies[i] = 1;
            all_bytes[i] = (unsigned char)i;
        }
        status = huffman_build(frequencies, SYMBOLS, &book);
        assert(status == 0 && book.node_count == MAX_NODES);
        if (status != 0) return 1;
        for (int i = 0; i < SYMBOLS; ++i) assert(strlen(book.codes[i]) == 8);
        status = huffman_encode(&book, all_bytes, SYMBOLS, all_bits, sizeof(all_bits), &bit_count);
        assert(status == 0 && bit_count == SYMBOLS * 8);
        if (status != 0) return 1;
        status = huffman_decode(&book, all_bits, bit_count, restored, sizeof(restored), &length);
        assert(status == 0 && length == SYMBOLS && memcmp(all_bytes, restored, SYMBOLS) == 0);
        if (status != 0) return 1;
        assert(huffman_decode(&book, all_bits, bit_count, restored, SYMBOLS - 1, &length) == -2);
        assert(huffman_encode(&book, all_bytes, SYMBOLS, all_bits, SYMBOLS * 8, &bit_count) == -2);
    }
    return 0;
}
#endif
