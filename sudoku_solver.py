"""
Backtracking solver for standard 9×9 Sudoku.

Functions
---------
solve_Sudoku(board) – validates and solves a board in place; returns the solved
                      board or None if no solution exists.
print_board(board)  – prints the board to stdout in a readable grid format.
"""
import math


BOARD_SIZE = 9
BOX_SIZE = 3


def print_board(board):
    """Prints a 9×9 Sudoku board to stdout with box separators.

    Parameters
    ----------
    board : list[list[int]]
        9×9 grid where 0 represents an empty cell.
    """
    separator = ("+" + "-" * (BOX_SIZE * 2 + 1)) * BOX_SIZE + "+"

    for r in range(BOARD_SIZE):
        if r % BOX_SIZE == 0:
            print(separator)
        row_str = ""
        for c in range(BOARD_SIZE):
            if c % BOX_SIZE == 0:
                row_str += "| "
            cell = str(board[r][c]) if board[r][c] != 0 else "."
            row_str += cell + " "
        print(row_str + "|")
    print(separator)


def solve_Sudoku(board):
    """Solves a 9×9 Sudoku puzzle in place using recursive backtracking.

    Validates the initial clues first. If any clue already conflicts with
    another, returns None immediately. Otherwise, fills all empty cells and
    returns the solved board. The board list is mutated in place.

    Parameters
    ----------
    board : list[list[int]]
        9×9 grid where 0 represents an empty cell.

    Returns
    -------
    list[list[int]] | None
        The solved board, or None if the puzzle has no solution.
    """

    def initial_check():
        """Returns False if any pre-filled digit conflicts with another in
        its row, column, or 3×3 box; otherwise return True."""
        for r in range(0, BOARD_SIZE):
            for c in range(0, BOARD_SIZE):
                if board[r][c] == 0:
                    continue
                else:
                    if is_repeated(r, c, board[r][c]):
                        print(f"The element in row {r+1}, and col {c+1}, board[{r+1}][{c+1}]: {board[r][c]} is repeated!")
                        return False
        return True

    def is_repeated(r, c, num):
        """Returns True if num already appears elsewhere in the same row,
        column, or 3×3 box as cell (r, c)."""
        for row in range(0, BOARD_SIZE):
            if board[row][c] == num and row != r:
                return True
        for col in range(0, BOARD_SIZE):
            if board[r][col] == num and col != c:
                return True

        # Computes the top - left corner of the box for cell(r, c):
            box_r = r // BOX_SIZE * BOX_SIZE
            box_c = c // BOX_SIZE * BOX_SIZE

        # Then iterates over the 3×3 box and check if num appears in another cell:
        for row in range(box_r, box_r + int(BOARD_SIZE/BOX_SIZE)):
            for col in range(box_c, box_c + int(BOARD_SIZE/BOX_SIZE)):
                if board[row][col] == num and (row != r or col != c):
                    return True
        return False

    def is_valid(row, col, num):
        """Returns True if placing num at (row, col) violates no row,
        column, or 3×3 box constraint in the current board state."""
        for c in range(0, BOARD_SIZE):
            if board[row][c] == num:
                return False

        for r in range(0, BOARD_SIZE):
            if board[r][col] == num:
                return False

        box_r = row // BOX_SIZE * BOX_SIZE
        box_c = col // BOX_SIZE * BOX_SIZE
        for r in range(box_r, box_r + BOX_SIZE):
            for c in range(box_c, box_c + BOX_SIZE):
                if board[r][c] == num:
                    return False

        return True

    def solve():
        """Recursively fills empty cells via backtracking.

        Returns True when all cells are validly filled, False when a
        dead-end is reached (triggers backtracking in the caller).
        """
        for r in range(0, BOARD_SIZE):
            for c in range(0, BOARD_SIZE):
                if board[r][c] == 0:
                    for num in range(1, BOARD_SIZE + 1):
                        if is_valid(r, c, num):
                            board[r][c] = num
                            if solve():
                                return True
                            board[r][c] = 0  # Backtrack
                    return False  # no valid num found for this cell
        return True  # all cells filled

    print("Initial board:")
    print_board(board)
    if initial_check():
        print("Board is valid")
        solve()
        print("Solved board:")
        print_board(board)
        return board
    else:
        print("Board is invalid")
        print("No solution can be found!")
        return None
