from z3 import *

# Create a 3x3 grid of integer variables
square = [[Int(f"cell_{r}_{c}") for c in range(3)] for r in range(3)]

solver = Solver()

# Constraint 1: Each cell contains a number from 1 to 9
for r in range(3):
    for c in range(3):
        solver.add(square[r][c] >= 1)
        solver.add(square[r][c] <= 9)

# Constraint 2: Each number 1-9 appears exactly once (all cells distinct)
all_cells = [square[r][c] for r in range(3) for c in range(3)]
solver.add(Distinct(all_cells))

magic_sum = 15

# Constraint 3: All three rows sum to 15
for r in range(3):
    solver.add(Sum([square[r][c] for c in range(3)]) == magic_sum)

# Constraint 4: All three columns sum to 15
for c in range(3):
    solver.add(Sum([square[r][c] for r in range(3)]) == magic_sum)

# Constraint 5: Both diagonals sum to 15
solver.add(Sum([square[i][i] for i in range(3)]) == magic_sum)
solver.add(Sum([square[i][2 - i] for i in range(3)]) == magic_sum)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Magic Square found:")
    for r in range(3):
        row_vals = [str(m.eval(square[r][c])) for c in range(3)]
        print(" ".join(row_vals))
    print("valid = True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")