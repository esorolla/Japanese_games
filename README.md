# Sudoku Solver

## Overview

A Python desktop application built with Tkinter for playing and solving both
standard **9×9 Sudoku** and **Samurai Sudoku** (five overlapping 9×9 grids on
a 21×21 board).

---

## Features

- Two puzzle types: Standard Sudoku and Samurai Sudoku
- Two play modes per type:
  - **Manual entry** – enter your own puzzle clues, then request the full solution
  - **Random puzzle** – play against a generated puzzle with button-triggered feedback
- **Manual mode buttons**: `Display solution`, `Clear`, `Home`
- **Random mode buttons**: `Check solution` (colors digits green ✓ / red ✗ and shows a Victory message when the puzzle is fully solved), `Regenerate` (load a new random puzzle), `Home`
- `Home` button returns to the main menu from any game screen without closing the application

---

## Requirements

- Python **3.10** or later
- `tkinter` — included in standard Python distributions on Windows and macOS
  - Linux: `sudo apt install python3-tk`

---

## How to Run

```bash
python main.py
```

---

## Project Structure

```
Sudoku_solver/
│
├── main.py                # Launcher: menu window and game-mode routing
│
├── sudoku_gui.py          # GUI for standard 9×9 Sudoku
├── sudoku_solver.py       # Backtracking solver for standard 9×9 Sudoku
├── sudoku_generator.py    # Random puzzle generator for standard 9×9 Sudoku
│
├── samurai_gui.py         # GUI for Samurai Sudoku (21×21 canvas)
├── samurai_solver.py      # Backtracking solver for Samurai Sudoku
└── samurai_generator.py   # Random puzzle generator for Samurai Sudoku
```

---

## Dependency Graph

```
main.py
├── sudoku_gui.py
│   └── sudoku_solver.py
├── samurai_gui.py
│   └── samurai_solver.py
├── sudoku_generator.py            (no internal project dependencies)
└── samurai_generator.py
    ├── samurai_solver.py          (constants: BOARD_SIZE, SUBGRID_ORIGINS, is_active)
    └── sudoku_generator.py        (helpers: _is_valid, _fill_board)
```

---

## Game Modes

| # | Mode | Board | Buttons |
|---|------|-------|---------|
| 1 | Normal Sudoku – enter your puzzle | Blank 9×9 | Display solution · Clear · Home |
| 2 | Samurai Sudoku – enter your puzzle | Blank 21×21 | Display solution · Clear · Home |
| 3 | Normal Sudoku – random puzzle | Pre-filled 9×9 | Check solution · Regenerate · Home |
| 4 | Samurai Sudoku – random puzzle | Pre-filled 21×21 | Check solution · Regenerate · Home |

---

## Color Coding

| Color | Meaning |
|-------|---------|
| Black | Pre-filled clue digit |
| Blue  | Digit filled by **Display solution** |
| Green | User digit matching the solution (after **Check solution**) |
| Red   | User digit not matching the solution (after **Check solution**) |

---

## Algorithms

### Backtracking Solver (standard and Samurai)

Both solvers use **recursive backtracking**, which is a systematic, constraint-driven
search — much more efficient than trial and error.

#### Core idea: reducing the problem size at each step

The solver scans cells left-to-right, top-to-bottom and finds the first empty one.
For that cell it tries each digit 1–9, but only commits a digit if it is **currently
valid** — i.e. it does not appear in the same row, column, or 3×3 box. This
constraint check is not a guess: a digit that fails it is **provably** incompatible
with the clues already on the board and is skipped immediately without any further
exploration.

When a valid digit is found, it is placed and `solve()` calls **itself** on the
resulting board. The key insight is that each call faces a strictly smaller problem
— one fewer empty cell — so the recursion always terminates. The two base cases are:

- **All cells are filled** → every recursive call succeeded; the function returns
  `True` and the solution propagates back up the call stack unchanged.
- **No valid digit exists for the current cell** → the partial board is a dead end.
  The function returns `False` without touching any other cell.

#### What backtracking actually means

When an inner call returns `False`, the caller does not give up — it knows that the
digit it placed was the cause of the dead end. It **erases that digit** (resets the
cell to 0) and tries the next valid digit for its own cell. If no digit works, it
too returns `False` to its own caller, which then erases its digit and continues.

This "unwind and retry" mechanism is what gives the technique its name. Crucially,
it is not random: every branch of the search tree is explored **at most once**. Once
a partial assignment is shown to lead to no solution, it is abandoned permanently.
The algorithm is therefore **complete** (it will always find a solution if one
exists) and **non-redundant** (it never re-examines a configuration it has already
ruled out).

#### Why this is far more efficient than brute force

A pure brute-force approach would enumerate all possible complete boards — 9⁸¹ ≈ 10⁷⁷
combinations for a 9×9 grid — and check each one. The backtracking solver avoids
this because the constraint check prunes entire subtrees of the search space the
moment a contradiction is detected, often after placing just a few digits. In
practice, a well-clued Sudoku puzzle is solved in milliseconds because the clues
constrain the search so tightly that very little backtracking ever occurs.

#### Samurai variant

The **Samurai solver** applies the same logic to the 21×21 board. The only
difference is in the validity check: a cell that lies in an overlap zone belongs to
two sub-grids simultaneously, so the solver validates each placement against the
row, column, and 3×3 box constraints of **every sub-grid that contains that cell**.
The recursive structure and the backtracking mechanism are identical.

---

### Puzzle Generation

#### Standard Sudoku (`sudoku_generator.py`)

1. Fill an empty 9×9 board using **randomised backtracking** to produce a
   complete valid solution.
2. Randomly remove cells, keeping a target number of clues (default: **35**).
3. Return the puzzle (0 = empty cell).

#### Samurai Sudoku (`samurai_generator.py`)

1. Generate the **centre sub-grid** (Grid 2) as a complete 9×9.
2. For each of the 4 outer sub-grids, pre-fill the 3×3 corner box it shares
   with the centre grid, then complete the sub-grid independently via
   randomised backtracking.
3. **Save the fully solved 21×21 board** as the solution before removing any cells.
4. Randomly remove cells, keeping ~**150 clues**.
5. Return `(puzzle, solution)` — the solution is passed directly to the GUI,
   avoiding a second solve pass and keeping the puzzle screen fast to open.
