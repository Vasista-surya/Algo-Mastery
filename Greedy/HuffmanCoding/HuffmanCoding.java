import java.util.*;

/** Huffman symbols are UTF-16 char units; frequencies are positive long values
 * whose sum fits long (overflow throws ArithmeticException). Empty -> empty;
 * one symbol -> "0". Merge ties use minimum character in each subtree.
 * Build O(K log K+S) time/O(K+S) space, S=sum of codeword lengths.
 * Codec O(S+B+L), B bits, L chars; validates external prefix-free codebooks.
 * Invalid input, unknown symbols, invalid/truncated bits throw IllegalArgumentException.
 */
public class HuffmanCoding {
    private static final class Node {
        final long frequency;
        final char minimum;
        final Character symbol;
        final Node left, right;
        Node(char symbol, long frequency) {
            this.frequency = frequency; this.minimum = symbol; this.symbol = symbol;
            this.left = null; this.right = null;
        }
        Node(Node left, Node right) {
            this.frequency = Math.addExact(left.frequency, right.frequency);
            this.minimum = (char)Math.min(left.minimum, right.minimum);
            this.symbol = null; this.left = left; this.right = right;
        }
    }
    private static final class Path {
        final Node node;
        final String prefix;
        Path(Node node, String prefix) { this.node = node; this.prefix = prefix; }
    }
    private static final class Trie {
        final Trie[] child = new Trie[2];
        Character symbol;
    }

    public static Map<Character, String> huffmanCodes(Map<Character, Long> frequencies) {
        if (frequencies == null) throw new IllegalArgumentException("null frequencies");
        PriorityQueue<Node> heap = new PriorityQueue<>(Comparator
            .comparingLong((Node node) -> node.frequency).thenComparingInt(node -> node.minimum));
        for (Map.Entry<Character, Long> entry : frequencies.entrySet()) {
            if (entry.getKey() == null || entry.getValue() == null || entry.getValue() <= 0)
                throw new IllegalArgumentException("nonnull symbols and positive frequencies required");
            heap.add(new Node(entry.getKey(), entry.getValue()));
        }
        Map<Character, String> codes = new TreeMap<>();
        if (heap.isEmpty()) return codes;
        while (heap.size() > 1) {
            Node left = heap.remove(), right = heap.remove();
            heap.add(new Node(left, right));
        }
        Deque<Path> stack = new ArrayDeque<>();
        stack.push(new Path(heap.remove(), ""));
        while (!stack.isEmpty()) {
            Path path = stack.pop();
            if (path.node.symbol != null) {
                codes.put(path.node.symbol, path.prefix.isEmpty() ? "0" : path.prefix);
            } else {
                stack.push(new Path(path.node.right, path.prefix + "1"));
                stack.push(new Path(path.node.left, path.prefix + "0"));
            }
        }
        return codes;
    }

    private static Trie trie(Map<Character, String> codes) {
        if (codes == null) throw new IllegalArgumentException("null codebook");
        Trie root = new Trie();
        for (Map.Entry<Character, String> entry : codes.entrySet()) {
            String code = entry.getValue();
            if (entry.getKey() == null || code == null || code.isEmpty())
                throw new IllegalArgumentException("nonnull symbols and nonempty codewords required");
            Trie node = root;
            for (int i = 0; i < code.length(); i++) {
                char bit = code.charAt(i);
                if (bit != '0' && bit != '1') throw new IllegalArgumentException("nonbinary codeword");
                if (node.symbol != null) throw new IllegalArgumentException("prefix collision");
                int index = bit - '0';
                if (node.child[index] == null) node.child[index] = new Trie();
                node = node.child[index];
            }
            if (node.symbol != null || node.child[0] != null || node.child[1] != null)
                throw new IllegalArgumentException("duplicate codeword or prefix");
            node.symbol = entry.getKey();
        }
        return root;
    }

    public static String encode(String text, Map<Character, String> codes) {
        if (text == null) throw new IllegalArgumentException("null text");
        trie(codes);
        Map<Character, String> lookup = new HashMap<>(codes);
        StringBuilder bits = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            String code = lookup.get(text.charAt(i));
            if (code == null) throw new IllegalArgumentException("unknown symbol");
            bits.append(code);
        }
        return bits.toString();
    }

    public static String decode(String bits, Map<Character, String> codes) {
        if (bits == null) throw new IllegalArgumentException("null bits");
        Trie root = trie(codes), node = root;
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < bits.length(); i++) {
            char bit = bits.charAt(i);
            if (bit != '0' && bit != '1') throw new IllegalArgumentException("nonbinary stream");
            node = node.child[bit - '0'];
            if (node == null) throw new IllegalArgumentException("invalid bitstream");
            if (node.symbol != null) {
                text.append(node.symbol.charValue());
                node = root;
            }
        }
        if (node != root) throw new IllegalArgumentException("truncated codeword");
        return text.toString();
    }

    public static void main(String[] args) {
        Map<Character, Long> frequencies = new HashMap<>();
        frequencies.put('a', 5L); frequencies.put('b', 2L); frequencies.put('c', 1L);
        Map<Character, String> codes = huffmanCodes(frequencies);
        String bits = encode("abaca", codes);
        assert decode(bits, codes).equals("abaca");
        assert huffmanCodes(Collections.emptyMap()).isEmpty();
        assert decode("", Collections.emptyMap()).isEmpty();
        assert huffmanCodes(Collections.singletonMap('x', 7L)).get('x').equals("0");
        assert decode("000", Collections.singletonMap('x', "0")).equals("xxx");
        frequencies.clear(); frequencies.put('b', 1L); frequencies.put('a', 1L);
        assert huffmanCodes(frequencies).get('a').equals("0");
        boolean rejected = false;
        try { decode("1", Collections.singletonMap('x', "0")); }
        catch (IllegalArgumentException expected) { rejected = true; }
        assert rejected;
        boolean overflow = false;
        frequencies.clear(); frequencies.put('a', Long.MAX_VALUE); frequencies.put('b', 1L);
        try { huffmanCodes(frequencies); }
        catch (ArithmeticException expected) { overflow = true; }
        assert overflow;
        System.out.println("Codes: " + codes + "; encoded: " + bits);
    }
}
