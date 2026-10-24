import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Objects;

/** Evaluate whitespace-separated postfix using O(n) time/space.
 * Tokens: unsigned ASCII integers or binary + - * /. No parentheses/unary signs.
 * Literals and intermediate results have magnitude <=10^9; long arithmetic
 * safely holds the largest temporary product (10^18). Division truncates to zero.
 */
public class ExpressionEvaluation {
    public static final long MAX_VALUE = 1_000_000_000L;

    public static long evaluatePostfix(String expression) {
        Objects.requireNonNull(expression, "expression");
        for (int i = 0; i < expression.length(); i++) {
            if ("0123456789+-*/ \t\n\r\u000b\f".indexOf(expression.charAt(i)) < 0)
                throw new IllegalArgumentException("invalid character");
        }
        if (expression.trim().isEmpty()) throw new IllegalArgumentException("empty expression");
        Deque<Long> stack = new ArrayDeque<>();
        for (String token : expression.trim().split("[ \\t\\n\\r\\x0B\\f]+")) {
            if (token.matches("[0-9]+")) {
                long value = 0;
                for (int i = 0; i < token.length(); i++) {
                    value = value * 10 + token.charAt(i) - '0';
                    if (value > MAX_VALUE) throw new ArithmeticException("literal exceeds 10^9");
                }
                stack.push(value);
                continue;
            }
            if (token.length() != 1 || "+-*/".indexOf(token.charAt(0)) < 0 || stack.size() < 2)
                throw new IllegalArgumentException("invalid token or insufficient operands");
            long right = stack.pop(), left = stack.pop(), value;
            switch (token.charAt(0)) {
                case '+': value = left + right; break;
                case '-': value = left - right; break;
                case '*': value = left * right; break;
                default:
                    if (right == 0) throw new ArithmeticException("division by zero");
                    value = left / right;
            }
            if (value < -MAX_VALUE || value > MAX_VALUE)
                throw new ArithmeticException("intermediate result exceeds +/-10^9");
            stack.push(value);
        }
        if (stack.size() != 1) throw new IllegalArgumentException("expected one result");
        return stack.pop();
    }

    public static void main(String[] args) {
        long result = evaluatePostfix("12 3 4 2 - * +");
        assert result == 18;
        assert evaluatePostfix("0 7 - 3 /") == -2;
        for (String invalid : new String[]{"", "1 2", "1 +", "2+"}) {
            boolean rejected = false;
            try { evaluatePostfix(invalid); }
            catch (IllegalArgumentException ex) { rejected = true; }
            assert rejected;
        }
        for (String invalid : new String[]{"1 0 /", "1000000000 1 +", "1000000001"}) {
            boolean rejected = false;
            try { evaluatePostfix(invalid); }
            catch (ArithmeticException ex) { rejected = true; }
            assert rejected;
        }
        System.out.println(result);
    }
}
