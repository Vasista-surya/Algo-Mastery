/* 9x9 Sudoku MRV backtracking: O(81*9^e) time, O(81+e) space, e<=81.
 * Flat row-major array of 81 ints; 0 is empty. No heap allocation.
 * Return 1 solved, 0 valid givens but unsolvable, -1 invalid input/capacity.
 * Fully filled boards are validated. Output changes only on success; input
 * and output may alias. Finds one solution, not uniqueness. Hard boards costly.
 */
#include <assert.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    int board[81];
    unsigned int rows[9], columns[9], boxes[9];
} SudokuSearch;

static int bit_count(unsigned int mask) {
    int count = 0;
    while (mask) { mask &= mask - 1U; ++count; }
    return count;
}

static int search_sudoku(SudokuSearch *state) {
    int chosen = -1, fewest = 10;
    unsigned int chosen_mask = 0;
    for (int index = 0; index < 81; ++index) {
        if (state->board[index] != 0) continue;
        int row = index / 9, column = index % 9, box = (row / 3) * 3 + column / 3;
        unsigned int mask = 511U & ~(state->rows[row] | state->columns[column] | state->boxes[box]);
        int count = bit_count(mask);
        if (count == 0) return 0;
        if (count < fewest) { chosen = index; chosen_mask = mask; fewest = count; }
    }
    if (chosen == -1) return 1;
    int row = chosen / 9, column = chosen % 9, box = (row / 3) * 3 + column / 3;
    for (int value = 1; value <= 9; ++value) {
        unsigned int bit = 1U << (value - 1);
        if (!(chosen_mask & bit)) continue;
        state->board[chosen] = value;
        state->rows[row] |= bit;
        state->columns[column] |= bit;
        state->boxes[box] |= bit;
        if (search_sudoku(state)) return 1;
        state->rows[row] ^= bit;
        state->columns[column] ^= bit;
        state->boxes[box] ^= bit;
        state->board[chosen] = 0;
    }
    return 0;
}

int solve_sudoku(const int *input, int cells, int *output, int capacity) {
    if (!input || !output || cells != 81 || capacity < 81) return -1;
    SudokuSearch state = {0};
    for (int index = 0; index < 81; ++index) {
        int value = input[index];
        if (value < 0 || value > 9) return -1;
        state.board[index] = value;
        if (value == 0) continue;
        int row = index / 9, column = index % 9, box = (row / 3) * 3 + column / 3;
        unsigned int bit = 1U << (value - 1);
        if ((state.rows[row] | state.columns[column] | state.boxes[box]) & bit) return -1;
        state.rows[row] |= bit;
        state.columns[column] |= bit;
        state.boxes[box] |= bit;
    }
    if (!search_sudoku(&state)) return 0;
    memcpy(output, state.board, sizeof(state.board));
    return 1;
}

#ifndef ALGO_NO_MAIN
int main(void) {
    const int puzzle[81] = {
        5,3,0,0,7,0,0,0,0, 6,0,0,1,9,5,0,0,0, 0,9,8,0,0,0,0,6,0,
        8,0,0,0,6,0,0,0,3, 4,0,0,8,0,3,0,0,1, 7,0,0,0,2,0,0,0,6,
        0,6,0,0,0,0,2,8,0, 0,0,0,4,1,9,0,0,5, 0,0,0,0,8,0,0,7,9
    };
    const int first_row[] = {5,3,4,6,7,8,9,1,2};
    int solved[81] = {0}, invalid[81], impossible[81] = {0}, scratch[81] = {0};
    int status = solve_sudoku(puzzle, 81, solved, 81);
    assert(status == 1 && memcmp(solved, first_row, sizeof(first_row)) == 0);
    if (status != 1) return 1;
    status = solve_sudoku(solved, 81, scratch, 81);
    assert(status == 1 && memcmp(solved, scratch, sizeof(solved)) == 0);
    memcpy(invalid, solved, sizeof(invalid));
    invalid[0] = invalid[1];
    status = solve_sudoku(invalid, 81, scratch, 81);
    assert(status == -1);
    for (int i = 0; i < 8; ++i) impossible[i] = i + 1;
    impossible[17] = 9;
    status = solve_sudoku(impossible, 81, scratch, 81);
    assert(status == 0 && memcmp(solved, scratch, sizeof(solved)) == 0);
    status = solve_sudoku(puzzle, 81, scratch, 80);
    assert(status == -1);
    for (int i = 0; i < 81; ++i) printf("%d%s", solved[i], i % 9 == 8 ? "\n" : " ");
    return 0;
}
#endif
