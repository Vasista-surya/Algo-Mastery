/* C99 bracket matching: O(n) time, fixed O(1024) stack space.
 * Match (), [], {}; ignore all other bytes, including quotes. Empty is balanced.
 * At most 1024 simultaneously open brackets; overflow is an error, not false.
 * No allocations. The result output is unchanged on argument/capacity errors.
 */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>

#define BRACKET_CAPACITY 1024
typedef enum { BRACKETS_OK, BRACKETS_INVALID, BRACKETS_CAPACITY } BracketStatus;

BracketStatus is_balanced(const char *text, bool *result) {
    char stack[BRACKET_CAPACITY];
    size_t top = 0;
    if (!text || !result) return BRACKETS_INVALID;
    for (size_t i = 0; text[i]; ++i) {
        char c = text[i];
        if (c == '(' || c == '[' || c == '{') {
            if (top == BRACKET_CAPACITY) return BRACKETS_CAPACITY;
            stack[top++] = c;
        } else if (c == ')' || c == ']' || c == '}') {
            char expected = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (!top || stack[--top] != expected) {
                *result = false;
                return BRACKETS_OK;
            }
        }
    }
    *result = top == 0;
    return BRACKETS_OK;
}

int main(void) {
    bool balanced = false;
    BracketStatus status = is_balanced("{[()]}", &balanced);
    char too_deep[BRACKET_CAPACITY + 2];
    assert(status == BRACKETS_OK && balanced);
    puts(balanced ? "true" : "false");
    status = is_balanced("", &balanced);
    assert(status == BRACKETS_OK && balanced);
    status = is_balanced("([)]", &balanced);
    assert(status == BRACKETS_OK && !balanced);
    status = is_balanced(")", &balanced);
    assert(status == BRACKETS_OK && !balanced);
    for (size_t i = 0; i <= BRACKET_CAPACITY; ++i) too_deep[i] = '(';
    too_deep[BRACKET_CAPACITY + 1] = '\0';
    status = is_balanced(too_deep, &balanced);
    assert(status == BRACKETS_CAPACITY);
    status = is_balanced(NULL, &balanced);
    assert(status == BRACKETS_INVALID);
    {
        char boundary[2 * BRACKET_CAPACITY + 1];
        for (size_t i = 0; i < BRACKET_CAPACITY; ++i) {
            boundary[i] = '(';
            boundary[BRACKET_CAPACITY + i] = ')';
        }
        boundary[2 * BRACKET_CAPACITY] = '\0';
        status = is_balanced(boundary, &balanced);
        assert(status == BRACKETS_OK && balanced);
    }
    return 0;
}
