"""Deterministic binary Huffman coding of single-character string symbols.

Positive integer frequencies; empty mapping -> {}; one symbol -> '0'.
Merge ties use the smallest symbol in each subtree (Unicode order).
Build O(K log K + S) time/O(K + S) space, S = total codeword length;
encode/decode O(S + B + L), B bits, L text length. Integers cannot overflow.
Codec functions validate external codebooks as nonempty binary, prefix-free
words. Unknown symbols, malformed/truncated bitstreams raise ValueError.
"""

import heapq


def huffman_codes(frequencies):
    """Return {symbol: bitstring}; input mapping is not modified."""
    heap = []
    for symbol, frequency in frequencies.items():
        if type(symbol) is not str or len(symbol) != 1:
            raise ValueError("symbols must be single-character strings")
        if type(frequency) is not int or frequency <= 0:
            raise ValueError("frequencies must be positive integers")
        heap.append((frequency, symbol, symbol))
    heapq.heapify(heap)
    if not heap:
        return {}
    while len(heap) > 1:
        fa, sa, left = heapq.heappop(heap)
        fb, sb, right = heapq.heappop(heap)
        # Active subtrees have disjoint symbols, hence distinct minimum symbols.
        heapq.heappush(heap, (fa + fb, min(sa, sb), (left, right)))
    codes = {}
    stack = [(heap[0][2], "")]
    while stack:
        node, prefix = stack.pop()
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            left, right = node
            stack.append((right, prefix + "1"))
            stack.append((left, prefix + "0"))
    return dict(sorted(codes.items()))


def _trie(codes):
    root = {}
    for symbol, code in codes.items():
        if type(symbol) is not str or len(symbol) != 1:
            raise ValueError("symbols must be single-character strings")
        if type(code) is not str or not code or any(bit not in "01" for bit in code):
            raise ValueError("codes must be nonempty binary strings")
        node = root
        for bit in code:
            if None in node:
                raise ValueError("codebook is not prefix-free")
            node = node.setdefault(bit, {})
        if node:
            raise ValueError("duplicate codeword or prefix")
        node[None] = symbol
    return root


def encode(text, codes):
    """Encode a string with a validated codebook, returning a bitstring."""
    if type(text) is not str:
        raise ValueError("text must be a string")
    _trie(codes)
    try:
        return "".join(codes[symbol] for symbol in text)
    except KeyError as error:
        raise ValueError("symbol missing from codebook") from error


def decode(bits, codes):
    """Decode complete binary codewords; empty bits decode to empty text."""
    if type(bits) is not str:
        raise ValueError("bits must be a string")
    root = _trie(codes)
    node = root
    text = []
    for bit in bits:
        if bit not in "01" or bit not in node:
            raise ValueError("invalid bitstream")
        node = node[bit]
        if None in node:
            text.append(node[None])
            node = root
    if node is not root:
        raise ValueError("truncated codeword")
    return "".join(text)


if __name__ == "__main__":
    codes = huffman_codes({"a": 5, "b": 2, "c": 1})
    bits = encode("abaca", codes)
    assert decode(bits, codes) == "abaca"
    assert huffman_codes({}) == {} and decode("", {}) == ""
    assert huffman_codes({"x": 7}) == {"x": "0"}
    assert decode("000", {"x": "0"}) == "xxx"
    assert huffman_codes({"b": 1, "a": 1}) == {"a": "0", "b": "1"}
    print("Codes:", codes, "Encoded:", bits)
