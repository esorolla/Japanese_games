"""
Random Sudoku puzzle generator.

Generates a complete valid 9x9 board via randomised backtracking, then
removes cells to produce a puzzle. The resulting puzzle is derived from a
unique complete solution but does not guarantee a unique solution after
removal (checking would add significant time). For gameplay purposes this
is acceptable: the solver will always find a valid solution.
"""
import random

BOARD_SIZE = 9
BOX_SIZE   = 3


def _is_valid(board, r, c, num):
    if num in board[r]:
        return False
    for row in range(BOARD_SIZE):
        if board[row][c] == num:
            return False
    br = (r // BOX_SIZE) * BOX_SIZE
    bc = (c // BOX_SIZE) * BOX_SIZE
    for row in range(br, br + BOX_SIZE):
        for col in range(bc, bc + BOX_SIZE):
            if board[row][col] == num:
                return False
    return True


def _fill_board(board):
    """Fill empty cells with random valid digits via backtracking."""
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == 0:
                nums = list(range(1, BOARD_SIZE + 1))
                random.shuffle(nums)
                for num in nums:
                    if _is_valid(board, r, c, num):
                        board[r][c] = num
                        if _fill_board(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def generate_puzzle(num_clues: int = 35) -> list[list[int]]:
    """
    Return a 9x9 Sudoku puzzle with approximately num_clues given cells.
    Empty cells are represented as 0.
    """
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    _fill_board(board)

    cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
    random.shuffle(cells)
    to_remove = BOARD_SIZE * BOARD_SIZE - num_clues
    for r, c in cells[:to_remove]:
        board[r][c] = 0

    return board
