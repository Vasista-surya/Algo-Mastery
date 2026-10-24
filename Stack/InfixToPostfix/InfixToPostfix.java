import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Objects;

/** Validated shunting-yard conversion: O(n) time and O(n) space.
 * Grammar: expr = term {(+|-) term}; term = atom {(*|/) atom};
 * atom = ASCII_DIGITS | '(' expr ')'. ASCII whitespace separates tokens.
 * All operators are binary and left-associative; literals are 0..10^9.
 */
public class InfixToPostfix {
    public static final long MAX_VALUE = 1_000_000_000L;

    private static boolean isSpace(char c) {
        return " \t\n\r\u000b\f".indexOf(c) >= 0;
    }

    private static int precedence(char c) {
        return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : 0;
    }

    /** Syntax errors throw IllegalArgumentException; range errors ArithmeticException. */
    public static String infixToPostfix(String expression) {
        Objects.requireNonNull(expression, "expression");
        List<String> output = new ArrayList<>();
        Deque<Character> operators = new ArrayDeque<>();
        boolean needOperand = true;
        int i = 0;
        while (i < expression.length()) {
            char c = expression.charAt(i);
            if (isSpace(c)) {
                i++;
                continue;
            }
            if (c >= '0' && c <= '9') {
                if (!needOperand) throw new IllegalArgumentException("missing operator");
                int start = i;
                long value = 0;
                while (i < expression.length() && expression.charAt(i) >= '0'
                        && expression.charAt(i) <= '9') {
                    value = value * 10 + expression.charAt(i++) - '0';
                    if (value > MAX_VALUE) throw new ArithmeticException("literal exceeds 10^9");
                }
                output.add(expression.substring(start, i));
                needOperand = false;
                continue;
            }
            if (c == '(' && needOperand) {
                operators.push(c);
            } else if (c == ')' && !needOperand) {
                while (!operators.isEmpty() && operators.peek() != '(') {
                    output.add(String.valueOf(operators.pop()));
                }
                if (operators.isEmpty()) throw new IllegalArgumentException("unmatched ')'");
                operators.pop();
            } else if (precedence(c) > 0 && !needOperand) {
                while (!operators.isEmpty() && operators.peek() != '('
                        && precedence(operators.peek()) >= precedence(c)) {
                    output.add(String.valueOf(operators.pop()));
                }
                operators.push(c);
                needOperand = true;
            } else {
                throw new IllegalArgumentException("invalid token or missing operand/operator");
            }
            i++;
        }
        if (needOperand) throw new IllegalArgumentException("empty or incomplete expression");
        while (!operators.isEmpty()) {
            char c = operators.pop();
            if (c == '(') throw new IllegalArgumentException("unmatched '('");
            output.add(String.valueOf(c));
        }
        return String.join(" ", output);
    }

    public static void main(String[] args) {
        String result = infixToPostfix("12 + 3 * (4 - 2)");
        assert result.equals("12 3 4 2 - * +");
        assert infixToPostfix("8 / 2 / 2").equals("8 2 / 2 /");
        for (String invalid : new String[]{"", "()", "1 2", "1+", "(1", "1)", "-2"}) {
            boolean rejected = false;
            try { infixToPostfix(invalid); }
            catch (IllegalArgumentException ex) { rejected = true; }
            assert rejected;
        }
        System.out.println(result);
    }
}
