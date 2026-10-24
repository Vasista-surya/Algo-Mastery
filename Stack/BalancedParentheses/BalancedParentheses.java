import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Objects;

/** Match (), [], {} in O(n) time and O(n) space. Other characters are ignored,
 * including quotes: this is a bracket checker, not a programming-language parser.
 * Empty text is balanced; null throws NullPointerException.
 */
public class BalancedParentheses {
    public static boolean isBalanced(String text) {
        Objects.requireNonNull(text, "text");
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else if (c == ')' || c == ']' || c == '}') {
                char expected = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (stack.isEmpty() || stack.pop() != expected) return false;
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        assert isBalanced("");
        assert isBalanced("a * (b + [c - {d}])");
        assert !isBalanced("([)]");
        assert !isBalanced(")");
        assert !isBalanced("((");
        System.out.println(isBalanced("{[()]}"));
    }
}
