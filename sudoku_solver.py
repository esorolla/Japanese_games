'''
This is a Python script to solve Sudoku using a recursive backtracking algorithm.
'''
import math


BOARD_SIZE = 9
BOX_SIZE = 3


def print_board(board):
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

    def initial_check():
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
        if __name__ == "__main__":
            input("Press Enter to solve the Sudoku puzzle...")
        solve()
        print("Solved board:")
        print_board(board)
        return board
    else:
        print("Board is invalid")
        print("No solution can be found!")
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # board = [[0 for _ in range(4)] for _ in range(4)]
    board = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 2, 0, 0, 3, 4, 0, 0, 0],
                [3, 0, 0, 0, 8, 0, 1, 9, 0],
                [2, 4, 0, 0, 1, 7, 0, 0, 6],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
             ]
    solve_Sudoku(board)
