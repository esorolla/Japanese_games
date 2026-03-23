"""
Tkinter GUI for the Samurai Sudoku solver.
Imports solver logic from samurai_solver.py without modifying it.

Layout: Canvas-based 21×21 grid.
  Active cells – white (single grid) or light-blue (overlap zone)
  Dead zones   – plain white canvas background, no grid lines drawn
  Grid lines   – drawn explicitly only inside each of the 5 sub-grids
"""
import copy
import tkinter as tk
from tkinter import messagebox

from samurai_solver import (
    solve_samurai, is_active, get_subgrids,
    BOARD_SIZE, SUBGRID_ORIGINS, BOX_SIZE, SUBGRID_SIZE,
)

# Colours
CLR_BG      = "#f0f0f0"
CLR_GRID_BG = "#ffffff"   # single-grid active cell
CLR_OVERLAP = "#ddeeff"   # cell shared by two sub-grids
CLR_GIVEN   = "#000000"   # pre-filled digits
CLR_SOLVED  = "#1a6fbf"   # digits filled by the solver
CLR_CORRECT = "#2e7d32"   # user digit matching the solution
CLR_WRONG   = "#c62828"   # user digit not matching the solution
CLR_LINE    = "#333333"   # grid lines

CELL   = 34   # pixel size of each cell
MARGIN = 4    # canvas margin in pixels


class SamuraiGUI:
    def __init__(self, root: tk.Tk, initial_board=None, on_home=None,
                 regenerate_fn=None, initial_solution=None) -> None:
        self.root = root
        self._on_home = on_home
        self._regenerate_fn = regenerate_fn
        self._solution: list[list[int]] | None = None
        self._given: set[tuple[int, int]] = set()
        self.root.title("Samurai Sudoku Solver")
        self.root.resizable(True, True)
        self.root.configure(bg=CLR_BG)
        self.cells: dict[tuple[int, int], tk.Entry] = {}
        self._build_grid()
        self._build_buttons()
        if initial_board is not None:
            self._load_board(initial_board)
            if initial_solution is not None:
                self._solution = initial_solution
            else:
                result = solve_samurai(copy.deepcopy(initial_board))
                if result is not None:
                    self._solution = result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _cell_bg(self, r, c) -> str:
        return CLR_OVERLAP if len(get_subgrids(r, c)) > 1 else CLR_GRID_BG

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_grid(self) -> None:
        W = BOARD_SIZE * CELL + 2 * MARGIN
        H = BOARD_SIZE * CELL + 2 * MARGIN

        canvas = tk.Canvas(
            self.root, width=W, height=H,
            bg="white", highlightthickness=1, highlightbackground=CLR_LINE,
        )
        canvas.pack(padx=10, pady=(10, 5))

        # Draw grid lines for each sub-grid only (dead zones stay blank)
        for gr, gc in SUBGRID_ORIGINS:
            x0 = MARGIN + gc * CELL
            y0 = MARGIN + gr * CELL
            x1 = x0 + SUBGRID_SIZE * CELL
            y1 = y0 + SUBGRID_SIZE * CELL

            for i in range(SUBGRID_SIZE + 1):
                w = 2 if i % BOX_SIZE == 0 else 1
                y = y0 + i * CELL
                canvas.create_line(x0, y, x1, y, width=w, fill=CLR_LINE)
                x = x0 + i * CELL
                canvas.create_line(x, y0, x, y1, width=w, fill=CLR_LINE)

        # Place Entry widgets for active cells
        vcmd = (self.root.register(self._validate_cell), "%P")

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if not is_active(r, c):
                    continue

                cx = MARGIN + c * CELL + CELL // 2
                cy = MARGIN + r * CELL + CELL // 2

                entry = tk.Entry(
                    canvas,
                    font=("Arial", 14, "bold"),
                    justify="center",
                    fg=CLR_GIVEN,
                    bg=self._cell_bg(r, c),
                    bd=0,
                    relief="flat",
                    highlightthickness=0,
                    validate="key",
                    validatecommand=vcmd,
                )
                canvas.create_window(
                    cx, cy, window=entry,
                    width=CELL - 4, height=CELL - 4,
                    anchor="center",
                )
                self.cells[(r, c)] = entry

    def _build_buttons(self) -> None:
        btn_frame = tk.Frame(self.root, bg=CLR_BG)
        btn_frame.pack(pady=(5, 5))

        btn_style = dict(font=("Arial", 12), relief="groove", cursor="hand2")
        if self._regenerate_fn is None:
            tk.Button(btn_frame, text="Display solution", command=self._on_display_solution,
                      bg="#4a90d9", fg="white", **btn_style).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Clear", command=self._on_clear,
                      bg="#e07050", fg="white", **btn_style).pack(side="left", padx=6)
        else:
            tk.Button(btn_frame, text="Check solution", command=self._on_check_solution,
                      bg="#4a90d9", fg="white", **btn_style).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Regenerate", command=self._on_regenerate,
                      bg="#e07050", fg="white", **btn_style).pack(side="left", padx=6)
        if self._on_home is not None:
            tk.Button(btn_frame, text="Home", command=self._on_home,
                      bg="#6c757d", fg="white", **btn_style).pack(side="left", padx=6)

        self.status_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Arial", 11), bg=CLR_BG).pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_cell(self, new_value: str) -> bool:
        """Allow only a single digit 1-9, or an empty cell."""
        return new_value == "" or (len(new_value) == 1 and new_value in "123456789")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _read_board(self) -> list[list[int]]:
        board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for (r, c), entry in self.cells.items():
            raw = entry.get().strip()
            if raw:
                board[r][c] = int(raw)
        return board

    def _display_solution(self, solved: list[list[int]],
                          original: list[list[int]]) -> None:
        for (r, c), entry in self.cells.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(solved[r][c]))
            entry.config(fg=CLR_GIVEN if original[r][c] != 0 else CLR_SOLVED)

    def _on_check_solution(self) -> None:
        if self._solution is None:
            return
        all_correct = True
        for (r, c), entry in self.cells.items():
            if (r, c) in self._given:
                continue
            val = entry.get().strip()
            if not val:
                all_correct = False
            elif int(val) == self._solution[r][c]:
                entry.config(fg=CLR_CORRECT)
            else:
                entry.config(fg=CLR_WRONG)
                all_correct = False
        if all_correct:
            self.status_var.set("Victory! Puzzle solved correctly!")
            messagebox.showinfo("Victory!", "Congratulations! You solved the puzzle!")

    def _on_regenerate(self) -> None:
        for (r, c), entry in self.cells.items():
            entry.config(state="normal", fg=CLR_GIVEN, bg=self._cell_bg(r, c))
            entry.delete(0, tk.END)
        self._given = set()
        self._solution = None
        self.status_var.set("")
        new_board, new_solution = self._regenerate_fn()
        self._load_board(new_board)
        self._solution = new_solution

    def _on_display_solution(self) -> None:
        board    = self._read_board()
        original = copy.deepcopy(board)

        if self._solution is None:
            result = solve_samurai(copy.deepcopy(board))
            if result is None:
                self.status_var.set("No solution found!")
                messagebox.showerror("Unsolvable", "This board has no solution.")
                return
            self._solution = result

        self._display_solution(self._solution, original)
        self.status_var.set("Solved!")

    def _on_clear(self) -> None:
        for (r, c), entry in self.cells.items():
            entry.config(state="normal", fg=CLR_GIVEN, bg=self._cell_bg(r, c))
            entry.delete(0, tk.END)
        self.status_var.set("")

    def _load_board(self, board: list[list[int]]) -> None:
        for (r, c), entry in self.cells.items():
            if board[r][c] != 0:
                entry.insert(0, str(board[r][c]))
                self._given.add((r, c))


if __name__ == "__main__":
    root = tk.Tk()
    SamuraiGUI(root)
    root.mainloop()
