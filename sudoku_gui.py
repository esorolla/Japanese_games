"""
Tkinter GUI for the Sudoku solver.
Imports the solver logic from sudoku_solver.py without modifying it.
"""
import tkinter as tk
from tkinter import messagebox

from sudoku_solver import solve_Sudoku as _solve_board

BOARD_SIZE = 9
BOX_SIZE = 3

# Colours
CLR_BG        = "#f0f0f0"
CLR_GRID_BG   = "#ffffff"
CLR_GIVEN     = "#000000"   # pre-filled digits
CLR_SOLVED    = "#1a6fbf"   # digits filled by the solver
CLR_BOX_THICK = "#333333"   # thick border between 3×3 boxes
CLR_BOX_THIN  = "#aaaaaa"   # thin border between cells within a box


class SudokuGUI:
    def __init__(self, root: tk.Tk, initial_board=None) -> None:
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.resizable(True, True)
        self.root.configure(bg=CLR_BG)
        self.cells: dict[tuple[int, int], tk.Entry] = {}
        self._build_grid()
        self._build_buttons()
        if initial_board is not None:
            self._load_board(initial_board)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_grid(self) -> None:
        """Draw the 9×9 input grid with thicker lines between the 3×3 boxes."""
        outer = tk.Frame(self.root, bg=CLR_BOX_THICK, bd=2, relief="solid")
        outer.pack(padx=15, pady=(15, 5))

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                # Extra padding creates the visual thick border between boxes
                pad_top    = (3, 1) if r % BOX_SIZE == 0 else (1, 1)
                pad_left   = (3, 1) if c % BOX_SIZE == 0 else (1, 1)

                vcmd = (self.root.register(self._validate_cell), "%P")
                entry = tk.Entry(
                    outer,
                    width=2,
                    font=("Arial", 28, "bold"),
                    justify="center",
                    fg=CLR_GIVEN,
                    bg=CLR_GRID_BG,
                    bd=1,
                    relief="solid",
                    highlightthickness=0,
                    validate="key",
                    validatecommand=vcmd,
                )
                entry.grid(
                    row=r, column=c,
                    padx=pad_left,
                    pady=pad_top,
                    ipady=8,
                )
                self.cells[(r, c)] = entry

    def _build_buttons(self) -> None:
        btn_frame = tk.Frame(self.root, bg=CLR_BG)
        btn_frame.pack(pady=(5, 5))

        btn_style = dict(font=("Arial", 12), width=8, relief="groove", cursor="hand2")
        tk.Button(btn_frame, text="Solve", command=self._on_solve,
                  bg="#4a90d9", fg="white", **btn_style).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Clear", command=self._on_clear,
                  bg="#e07050", fg="white", **btn_style).pack(side="left", padx=6)

        self.status_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Arial", 11), bg=CLR_BG).pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_cell(self, new_value: str) -> bool:
        """Allow only a single digit 1-9, or an empty cell."""
        if new_value == "":
            return True
        return len(new_value) == 1 and new_value in "123456789"

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _read_board(self) -> list[list[int]]:
        board = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                raw = self.cells[(r, c)].get().strip()
                row.append(int(raw) if raw else 0)
            board.append(row)
        return board

    def _display_solution(self, solved: list[list[int]],
                          original: list[list[int]]) -> None:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                entry = self.cells[(r, c)]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, str(solved[r][c]))
                # Colour: black for given digits, blue for solver-filled digits
                entry.config(fg=CLR_GIVEN if original[r][c] != 0 else CLR_SOLVED)

    def _on_solve(self) -> None:
        board = self._read_board()
        original = [row[:] for row in board]   # snapshot before solver mutates it

        result = _solve_board([row[:] for row in board])

        if result is None:
            self.status_var.set("No solution found!")
            messagebox.showerror("Unsolvable", "This board has no solution.")
        else:
            self._display_solution(result, original)
            self.status_var.set("Solved!")

    def _on_clear(self) -> None:
        for entry in self.cells.values():
            entry.config(state="normal", fg=CLR_GIVEN)
            entry.delete(0, tk.END)
        self.status_var.set("")

    def _load_board(self, board: list[list[int]]) -> None:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != 0:
                    self.cells[(r, c)].insert(0, str(board[r][c]))


if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
