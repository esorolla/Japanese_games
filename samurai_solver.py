"""
Samurai Sudoku solver using recursive backtracking.

A Samurai Sudoku consists of 5 overlapping 9x9 grids arranged on a 21x21 board:

    [Grid 0]      [Grid 1]
        [  Grid 2 (center)  ]
    [Grid 3]      [Grid 4]

The 4 corner 3x3 boxes of the center grid are shared with the inner corner
boxes of the surrounding grids. Cells in those overlap zones must satisfy
the constraints of both sub-grids simultaneously.
"""

BOARD_SIZE   = 21
SUBGRID_SIZE = 9
BOX_SIZE     = 3

# Top-left (row, col) origin of each of the 5 sub-grids
SUBGRID_ORIGINS = [
    (0,  0),   # Grid 0 – top-left
    (0,  12),  # Grid 1 – top-right
    (6,  6),   # Grid 2 – center
    (12, 0),   # Grid 3 – bottom-left
    (12, 12),  # Grid 4 – bottom-right
]


def get_subgrids(r, c):
    """Return the indices of all sub-grids that contain cell (r, c)."""
    return [
        i for i, (gr, gc) in enumerate(SUBGRID_ORIGINS)
        if gr <= r < gr + SUBGRID_SIZE and gc <= c < gc + SUBGRID_SIZE
    ]


def is_active(r, c):
    """Return True if (r, c) belongs to at least one sub-grid."""
    return bool(get_subgrids(r, c))


def print_board(board):
    for r in range(BOARD_SIZE):
        row_str = ""
        for c in range(BOARD_SIZE):
            if not is_active(r, c):
                row_str += "  "
            else:
                row_str += (str(board[r][c]) if board[r][c] != 0 else ".") + " "
        print(row_str)


def solve_samurai(board):
    """
    Solve a Samurai Sudoku puzzle in-place using backtracking.

    Parameters
    ----------
    board : list[list[int]]
        21x21 grid. Use 0 for empty cells; dead-zone cells are ignored.

    Returns
    -------
    board if a solution is found, else None.
    """

    def is_valid(r, c, num):
        for i in get_subgrids(r, c):
            gr, gc = SUBGRID_ORIGINS[i]
            # Row within this sub-grid
            for col in range(gc, gc + SUBGRID_SIZE):
                if col != c and board[r][col] == num:
                    return False
            # Column within this sub-grid
            for row in range(gr, gr + SUBGRID_SIZE):
                if row != r and board[row][c] == num:
                    return False
            # 3x3 box within this sub-grid
            box_r = gr + ((r - gr) // BOX_SIZE) * BOX_SIZE
            box_c = gc + ((c - gc) // BOX_SIZE) * BOX_SIZE
            for row in range(box_r, box_r + BOX_SIZE):
                for col in range(box_c, box_c + BOX_SIZE):
                    if (row != r or col != c) and board[row][col] == num:
                        return False
        return True

    def initial_check():
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if not is_active(r, c) or board[r][c] == 0:
                    continue
                val = board[r][c]
                board[r][c] = 0          # temporarily remove to check for conflicts
                if not is_valid(r, c, val):
                    board[r][c] = val
                    print(f"Conflict at ({r+1}, {c+1}) = {val}")
                    return False
                board[r][c] = val
        return True

    def solve():
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if not is_active(r, c) or board[r][c] != 0:
                    continue
                for num in range(1, SUBGRID_SIZE + 1):
                    if is_valid(r, c, num):
                        board[r][c] = num
                        if solve():
                            return True
                        board[r][c] = 0  # backtrack
                return False             # no valid digit found
        return True                      # all active cells filled

    if not initial_check():
        print("Initial board is invalid – no solution possible.")
        return None
    if solve():
        return board
    print("No solution exists for this board.")
    return None


if __name__ == '__main__':
    # Provide clues by replacing 0s with known digits.
    # Warning: solving a near-empty Samurai Sudoku with pure backtracking
    # can be very slow; supply enough clues for a well-constrained puzzle.
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    print("Initial board:")
    print_board(board)
    result = solve_samurai(board)
    if result:
        print("\nSolved board:")
        print_board(result)
