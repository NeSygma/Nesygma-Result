from z3 import *

# Create an Optimize solver
opt = Optimize()

# Create a 9x9 grid of Boolean variables
# board[r][c] is True if a queen is placed at (r, c)
board = [[Bool(f"board_{r}_{c}") for c in range(9)] for r in range(9)]

# Total number of queens
num_queens = Sum([Sum(row) for row in board])

# Objective: minimize the number of queens
opt.minimize(num_queens)

# Ensure all squares are dominated
# For each square (r, c), at least one queen must be in the same row, column, or diagonal
for r in range(9):
    for c in range(9):
        # A square is dominated if:
        # 1. There is a queen in the same row, or
        # 2. There is a queen in the same column, or
        # 3. There is a queen in the same diagonal (both directions)
        opt.add(
            Or(
                # Same row
                Or([board[r][col] for col in range(9)]),
                # Same column
                Or([board[row][c] for row in range(9)]),
                # Same diagonal (top-left to bottom-right)
                Or([board[r + k][c + k] for k in range(-8, 9) if 0 <= r + k < 9 and 0 <= c + k < 9]),
                # Same diagonal (top-right to bottom-left)
                Or([board[r + k][c - k] for k in range(-8, 9) if 0 <= r + k < 9 and 0 <= c - k < 9])
            )
        )

# Check if a solution exists
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"Minimum number of queens required: {model.eval(num_queens)}")
    
    # Print the positions of the queens
    queens = []
    for r in range(9):
        for c in range(9):
            if model.eval(board[r][c]) == True:
                queens.append((r, c))
    print("Queen positions (row, col):")
    for pos in queens:
        print(pos)
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists (unexpected for this problem).")
else:
    print("STATUS: unknown")