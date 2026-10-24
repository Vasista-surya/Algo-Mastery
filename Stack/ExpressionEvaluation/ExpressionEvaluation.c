/* C99 postfix stack evaluation: O(n) time, fixed O(1024) scratch space.
 * Tokens: unsigned ASCII integers or binary + - * /, separated by ASCII
 * whitespace. No unary signs/parentheses. Division truncates toward zero.
 * Literals/results are bounded to +/-10^9. C99 long long safely holds every
 * temporary (largest product 10^18). At most 1024 input bytes are accepted.
 * On failure the caller's result is unchanged. No dynamic allocations.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

#define EVAL_LIMIT 1024
#define MAX_VALUE 1000000000LL
typedef enum { EVAL_OK, EVAL_INVALID, EVAL_CAPACITY, EVAL_RANGE, EVAL_DIV_ZERO } EvalStatus;

static int is_space(char c) {
    return c != '\0' && strchr(" \t\n\r\v\f", c) != NULL;
}

EvalStatus evaluate_postfix(const char *expression, long long *result) {
    long long stack[EVAL_LIMIT];
    size_t top = 0, i = 0;
    if (!expression || !result) return EVAL_INVALID;
    if (strlen(expression) > EVAL_LIMIT) return EVAL_CAPACITY;
    while (expression[i]) {
        size_t start, length;
        long long value = 0;
        if (is_space(expression[i])) { ++i; continue; }
        start = i;
        while (expression[i] && !is_space(expression[i])) ++i;
        length = i - start;
        if (expression[start] >= '0' && expression[start] <= '9') {
            for (size_t j = start; j < i; ++j) {
                if (expression[j] < '0' || expression[j] > '9') return EVAL_INVALID;
                value = value * 10 + expression[j] - '0';
                if (value > MAX_VALUE) return EVAL_RANGE;
            }
        } else {
            char op = expression[start];
            long long left, right;
            if (length != 1 || !strchr("+-*/", op) || top < 2) return EVAL_INVALID;
            right = stack[--top];
            left = stack[--top];
            switch (op) {
                case '+': value = left + right; break;
                case '-': value = left - right; break;
                case '*': value = left * right; break;
                default:
                    if (right == 0) return EVAL_DIV_ZERO;
                    value = left / right;
            }
            if (value < -MAX_VALUE || value > MAX_VALUE) return EVAL_RANGE;
        }
        if (top == EVAL_LIMIT) return EVAL_CAPACITY;
        stack[top++] = value;
    }
    if (top != 1) return EVAL_INVALID;
    *result = stack[0];
    return EVAL_OK;
}

int main(void) {
    long long value = 0;
    EvalStatus status = evaluate_postfix("12 3 4 2 - * +", &value);
    assert(status == EVAL_OK && value == 18);
    printf("%lld\n", value);
    status = evaluate_postfix("0 7 - 3 /", &value);
    assert(status == EVAL_OK && value == -2);
    status = evaluate_postfix("", &value);
    assert(status == EVAL_INVALID && value == -2);
    status = evaluate_postfix("1 2", &value);
    assert(status == EVAL_INVALID);
    status = evaluate_postfix("1 +", &value);
    assert(status == EVAL_INVALID);
    status = evaluate_postfix("1 0 /", &value);
    assert(status == EVAL_DIV_ZERO);
    status = evaluate_postfix("1000000000 1000000000 *", &value);
    assert(status == EVAL_RANGE);
    status = evaluate_postfix("2+", &value);
    assert(status == EVAL_INVALID);
    {
        char boundary[EVAL_LIMIT + 2];
        memset(boundary, '0', EVAL_LIMIT);
        boundary[EVAL_LIMIT] = '\0';
        status = evaluate_postfix(boundary, &value);
        assert(status == EVAL_OK && value == 0);
        boundary[EVAL_LIMIT] = '0';
        boundary[EVAL_LIMIT + 1] = '\0';
        status = evaluate_postfix(boundary, &value);
        assert(status == EVAL_CAPACITY && value == 0);
    }
    return 0;
}
