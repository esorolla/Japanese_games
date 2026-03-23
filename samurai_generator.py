"""
Random Samurai Sudoku puzzle generator.

Strategy
--------
1. Generates the center grid (Grid 2) as a complete valid 9x9.
2. Each outer grid shares one 3x3 corner box with the center grid.
   Pre-fills that shared box and generates the rest of the outer grid
   independently via randomized backtracking.
3. Removes cells randomly to produce the puzzle.

Because the 4 outer grids only overlap with the center (not with each
other), they can be generated independently once the center is fixed.
"""
import copy
import random

from samurai_solver import BOARD_SIZE, SUBGRID_ORIGINS, is_active
from sudoku_generator import _is_valid, _fill_board


def _make_9x9_with_fixed(fixed: list[tuple[int, int, int]]):
    """Generates a complete 9×9 board with pre-placed cells.

    Parameters
    ----------
    fixed : list[tuple[int, int, int]]
        Each entry is (local_row, local_col, value) — cells that must
        be placed before backtracking begins (e.g. overlap zone digits).

    Returns
    -------
    list[list[int]] | None
        The completed 9×9 board, or None if no valid completion exists.
    """
    board = [[0] * 9 for _ in range(9)]
    for lr, lc, v in fixed:
        board[lr][lc] = v
    return board if _fill_board(board) else None


def generate_complete_samurai() -> list[list[int]]:
    """Returns a fully filled valid 21×21 Samurai Sudoku board.

    Generates the center sub-grid first, then builds each outer sub-grid
    by pre-filling its shared 3×3 corner box and completing the rest via
    randomized backtracking. Retries automatically on the rare occasion
    that an outer sub-grid cannot be completed.

    Dead-zone cells (positions that belong to no sub-grid) are left as 0.

    Returns
    -------
    list[list[int]]
        A 21×21 grid with all 369 active cells filled.
    """
    while True:
        # Step 1 – generates the center grid (origin 6, 6)
        centre = [[0] * 9 for _ in range(9)]
        _fill_board(centre)

        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        cr, cc = SUBGRID_ORIGINS[2]          # (6, 6)
        for r in range(9):
            for c in range(9):
                board[cr + r][cc + c] = centre[r][c]

        # Step 2 – generates each outer grid using its overlap with the center
        # (grid_idx,  overlap corner in grid-local coords,  in center-local coords)
        outer_configs = [
            (0, (6, 6), (0, 0)),   # Grid 0 bottom-right box  ↔  center top-left box
            (1, (6, 0), (0, 6)),   # Grid 1 bottom-left box   ↔  center top-right box
            (3, (0, 6), (6, 0)),   # Grid 3 top-right box     ↔  center bottom-left box
            (4, (0, 0), (6, 6)),   # Grid 4 top-left box      ↔  center bottom-right box
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
        # Rare failure – retries with a fresh center grid


def generate_samurai_puzzle(
    num_clues: int = 150,
) -> tuple[list[list[int]], list[list[int]]]:
    """
    Returns (puzzle, solution) for a 21x21 Samurai Sudoku.

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
