"""
Random Samurai Sudoku puzzle generator.

Strategy
--------
1. Generate the centre grid (Grid 2) as a complete valid 9x9.
2. Each outer grid shares one 3x3 corner box with the centre grid.
   Pre-fill that shared box and generate the rest of the outer grid
   independently via randomised backtracking.
3. Remove cells randomly to produce the puzzle.

Because the 4 outer grids only overlap with the centre (not with each
other), they can be generated independently once the centre is fixed.
"""
import copy
import random

from samurai_solver import BOARD_SIZE, SUBGRID_ORIGINS, is_active
from sudoku_generator import _is_valid, _fill_board


def _make_9x9_with_fixed(fixed: list[tuple[int, int, int]]):
    """
    Generate a complete 9x9 board where `fixed` cells are pre-placed.
    fixed: list of (local_row, local_col, value).
    Returns the board or None on failure.
    """
    board = [[0] * 9 for _ in range(9)]
    for lr, lc, v in fixed:
        board[lr][lc] = v
    return board if _fill_board(board) else None


def generate_complete_samurai() -> list[list[int]]:
    """
    Return a fully filled valid 21x21 Samurai Sudoku board.
    Dead-zone cells are left as 0.
    """
    while True:
        # Step 1 – generate the centre grid (origin 6, 6)
        centre = [[0] * 9 for _ in range(9)]
        _fill_board(centre)

        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        cr, cc = SUBGRID_ORIGINS[2]          # (6, 6)
        for r in range(9):
            for c in range(9):
                board[cr + r][cc + c] = centre[r][c]

        # Step 2 – generate each outer grid using its overlap with the centre
        # (grid_idx,  overlap corner in grid-local coords,  in centre-local coords)
        outer_configs = [
            (0, (6, 6), (0, 0)),   # Grid 0 bottom-right box  ↔  centre top-left box
            (1, (6, 0), (0, 6)),   # Grid 1 bottom-left box   ↔  centre top-right box
            (3, (0, 6), (6, 0)),   # Grid 3 top-right box     ↔  centre bottom-left box
            (4, (0, 0), (6, 6)),   # Grid 4 top-left box      ↔  centre bottom-right box
        ]

        success = True
        for grid_idx, (olr, olc), (clr, clc) in outer_configs:
            gr, gc = SUBGRID_ORIGINS[grid_idx]
            fixed = [
                (olr + dr, olc + dc, centre[clr + dr][clc + dc])
                for dr in range(3) for dc in range(3)
            ]
            outer = _make_9x9_with_fixed(fixed)
            if outer is None:
                success = False
                break
            for r in range(9):
                for c in range(9):
                    board[gr + r][gc + c] = outer[r][c]

        if success:
            return board
        # Rare failure – retry with a fresh centre grid


def generate_samurai_puzzle(
    num_clues: int = 150,
) -> tuple[list[list[int]], list[list[int]]]:
    """
    Return (puzzle, solution) for a 21x21 Samurai Sudoku.

    puzzle   – num_clues cells filled, the rest are 0.
    solution – the fully solved board (saved before cells are removed).

    The total number of active cells is 369 (5 grids minus 4 shared 3x3 boxes).
    A typical value for num_clues is 120-160 (~30 per sub-grid on average).
    """
    board = generate_complete_samurai()
    solution = copy.deepcopy(board)
    active = [(r, c) for r in range(BOARD_SIZE)
              for c in range(BOARD_SIZE) if is_active(r, c)]
    random.shuffle(active)
    for r, c in active[num_clues:]:
        board[r][c] = 0
    return board, solution
