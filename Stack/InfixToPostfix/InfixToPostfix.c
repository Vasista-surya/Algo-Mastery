/* C99 shunting-yard conversion: O(n) time, O(n) output, fixed O(LIMIT)
 * scratch. Grammar: expr=term{(+|-)term}, term=atom{(*|/)atom},
 * atom=DIGITS|'('expr')'. ASCII whitespace; binary operators only.
 * Literals 0..10^9; at most 1024 input bytes. Output is space-separated.
 * Caller supplies a non-overlapping output buffer; ignore it on failure.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

#define INFIX_LIMIT 1024
typedef enum { INFIX_OK, INFIX_INVALID, INFIX_CAPACITY, INFIX_RANGE } InfixStatus;

static int is_space(char c) {
    return c != '\0' && strchr(" \t\n\r\v\f", c) != NULL;
}

static int precedence(char c) {
    return c == '+' || c == '-' ? 1 : c == '*' || c == '/' ? 2 : 0;
}

static int append_token(char *out, size_t capacity, size_t *used,
                        const char *token, size_t length) {
    size_t separator = *used != 0;
    if (*used >= capacity || separator >= capacity - *used ||
        length >= capacity - *used - separator) return 0;
    if (separator) out[(*used)++] = ' ';
    memcpy(out + *used, token, length);
    *used += length;
    out[*used] = '\0';
    return 1;
}

InfixStatus infix_to_postfix(const char *expression, char *out, size_t capacity) {
    char operators[INFIX_LIMIT];
    size_t top = 0, used = 0, i = 0;
    int need_operand = 1;
    if (!expression || !out) return INFIX_INVALID;
    if (capacity == 0) return INFIX_CAPACITY;
    out[0] = '\0';
    if (strlen(expression) > INFIX_LIMIT) return INFIX_CAPACITY;
    while (expression[i]) {
        char c = expression[i];
        if (is_space(c)) { ++i; continue; }
        if (c >= '0' && c <= '9') {
            size_t start = i;
            long long value = 0;
            if (!need_operand) return INFIX_INVALID;
            while (expression[i] >= '0' && expression[i] <= '9') {
                value = value * 10 + expression[i++] - '0';
                if (value > 1000000000LL) return INFIX_RANGE;
            }
            if (!append_token(out, capacity, &used, expression + start, i - start))
                return INFIX_CAPACITY;
            need_operand = 0;
            continue;
        }
        if (c == '(' && need_operand) {
            if (top == INFIX_LIMIT) return INFIX_CAPACITY;
            operators[top++] = c;
        } else if (c == ')' && !need_operand) {
            while (top && operators[top - 1] != '(') {
                if (!append_token(out, capacity, &used, &operators[--top], 1))
                    return INFIX_CAPACITY;
            }
            if (!top) return INFIX_INVALID;
            --top;
        } else if (precedence(c) && !need_operand) {
            while (top && operators[top - 1] != '(' &&
                   precedence(operators[top - 1]) >= precedence(c)) {
                if (!append_token(out, capacity, &used, &operators[--top], 1))
                    return INFIX_CAPACITY;
            }
            if (top == INFIX_LIMIT) return INFIX_CAPACITY;
            operators[top++] = c;
            need_operand = 1;
        } else {
            return INFIX_INVALID;
        }
        ++i;
    }
    if (need_operand) return INFIX_INVALID;
    while (top) {
        if (operators[top - 1] == '(') return INFIX_INVALID;
        if (!append_token(out, capacity, &used, &operators[--top], 1))
            return INFIX_CAPACITY;
    }
    return INFIX_OK;
}

int main(void) {
    char out[2 * INFIX_LIMIT + 1];
    const char *invalid[] = {"", "()", "1 2", "1+", "(1", "1)", "-2"};
    InfixStatus status = infix_to_postfix("12 + 3 * (4 - 2)", out, sizeof out);
    assert(status == INFIX_OK && strcmp(out, "12 3 4 2 - * +") == 0);
    puts(out);
    for (size_t i = 0; i < sizeof invalid / sizeof invalid[0]; ++i) {
        status = infix_to_postfix(invalid[i], out, sizeof out);
        assert(status == INFIX_INVALID);
    }
    status = infix_to_postfix("1+2", out, 5);
    assert(status == INFIX_CAPACITY); /* "1 2 +" needs six bytes with NUL. */
    status = infix_to_postfix("1+2", out, 6);
    assert(status == INFIX_OK && strcmp(out, "1 2 +") == 0);
    status = infix_to_postfix("1000000001", out, sizeof out);
    assert(status == INFIX_RANGE);
    {
        char boundary[INFIX_LIMIT + 2];
        memset(boundary, '0', INFIX_LIMIT);
        boundary[INFIX_LIMIT] = '\0';
        status = infix_to_postfix(boundary, out, sizeof out);
        assert(status == INFIX_OK && strlen(out) == INFIX_LIMIT);
        boundary[INFIX_LIMIT] = '0';
        boundary[INFIX_LIMIT + 1] = '\0';
        status = infix_to_postfix(boundary, out, sizeof out);
        assert(status == INFIX_CAPACITY);
    }
    return 0;
}
