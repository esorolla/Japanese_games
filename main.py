"""
Sudoku Game Launcher.

Presents a menu so the user can choose one of four game modes:
  1. Normal Sudoku   – blank grid, user enters their own puzzle
  2. Samurai Sudoku  – blank grid, user enters their own puzzle
  3. Normal Sudoku   – board pre-filled with a random puzzle
  4. Samurai Sudoku  – board pre-filled with a random puzzle
"""
import tkinter as tk

CLR_BG = "#f0f0f0"


def main() -> None:
    """Builds and displays the launcher menu, then starts the Tkinter event loop.

    Creates a window with four mode buttons. Clicking a button calls
    launch(mode), which hides the menu and opens the appropriate game screen.
    """
    root = tk.Tk()
    root.title("Sudoku – Choose a Game")
    root.resizable(True, True)
    root.configure(bg=CLR_BG)

    tk.Label(root, text="Sudoku Solver",
             font=("Arial", 22, "bold"), bg=CLR_BG).pack(pady=(25, 4))
    tk.Label(root, text="Select a game mode",
             font=("Arial", 12), bg=CLR_BG, fg="#555555").pack(pady=(0, 18))

    status_var = tk.StringVar()
    buttons: list[tk.Button] = []

    btn_style = dict(
        font=("Arial", 13), width=36, pady=10,
        cursor="hand2", relief="groove", bd=2,
    )

    options = [
        (1, "Normal Sudoku    –   enter your puzzle",   "#4a90d9"),
        (2, "Samurai Sudoku   –   enter your puzzle",   "#5ba85a"),
        (3, "Normal Sudoku    –   random puzzle",       "#e07050"),
        (4, "Samurai Sudoku   –   random puzzle",       "#9b59b6"),
    ]

    def launch(mode: int) -> None:
        """Disables menu buttons, generates a board if needed, hides the menu,
        and opens the game window for the selected mode.

        Parameters
        ----------
        mode : int
            1 – Normal Sudoku, manual entry
            2 – Samurai Sudoku, manual entry
            3 – Normal Sudoku, random puzzle
            4 – Samurai Sudoku, random puzzle
        """
        for btn in buttons:
            btn.config(state="disabled")

        # Shows a loading message for random modes before the (brief) generation
        if mode in (3, 4):
            status_var.set("Generating puzzle, please wait…")
            root.update()

        board = None
        regenerate_fn = None
        samurai_solution = None
        if mode == 3:
            from sudoku_generator import generate_puzzle
            board = generate_puzzle()
            regenerate_fn = generate_puzzle
        elif mode == 4:
            from samurai_generator import generate_samurai_puzzle
            board, samurai_solution = generate_samurai_puzzle()
            regenerate_fn = generate_samurai_puzzle

        # Hides the launcher and open the game as a child Toplevel
        root.withdraw()
        game_win = tk.Toplevel(root)
        game_win.protocol("WM_DELETE_WINDOW", root.destroy)

        def go_home() -> None:
            """Destroys the game window and restores the launcher menu."""
            game_win.destroy()
            status_var.set("")
            for btn in buttons:
                btn.config(state="normal")
            root.deiconify()

        if mode in (1, 3):
            from sudoku_gui import SudokuGUI
            SudokuGUI(game_win, initial_board=board, on_home=go_home, regenerate_fn=regenerate_fn)
        else:
            from samurai_gui import SamuraiGUI
            SamuraiGUI(game_win, initial_board=board, on_home=go_home,
                       regenerate_fn=regenerate_fn, initial_solution=samurai_solution)

    for mode, label, color in options:
        btn = tk.Button(
            root, text=label, bg=color, fg="white",
            command=lambda m=mode: launch(m),
            **btn_style,
        )
        btn.pack(padx=40, pady=5)
        buttons.append(btn)

    tk.Label(root, textvariable=status_var,
             font=("Arial", 10), bg=CLR_BG, fg="#888888").pack(pady=(8, 20))

    root.mainloop()


if __name__ == "__main__":
    main()
