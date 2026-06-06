from z3 import *

solver = Solver()

# 3x3 grid of integer variables
square = [[Int(f"cell_{r}_{c}") for c in range(3)] for r in range(3)]

magic_sum = 15

# Constraint 1: Each cell contains a number from 1 to 9
for r in range(3):
    for c in range(3):
        solver.add(square[r][c] >= 1, square[r][c] <= 9)

# Constraint 2: Each number 1-9 appears exactly once (all distinct)
all_cells = [square[r][c] for r in range(3) for c in range(3)]
solver.add(Distinct(all_cells))

# Constraint 3: All three rows sum to 15
for r in range(3):
    solver.add(Sum([square[r][c] for c in range(3)]) == magic_sum)

# Constraint 4: All three columns sum to 15
for c in range(3):
    solver.add(Sum([square[r][c] for r in range(3)]) == magic_sum)

# Constraint 5: Both diagonals sum to 15
solver.add(square[0][0] + square[1][1] + square[2][2] == magic_sum)
solver.add(square[0][2] + square[1][1] + square[2][0] == magic_sum)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Magic square found:")
    for r in range(3):
        row_vals = [str(m.evaluate(square[r][c]).as_long()) for c in range(3)]
        print("  " + " ".join(row_vals))
    print(f"magic_sum = {magic_sum}")
    print("valid = True")
    # Verify all constraints explicitly
    grid = [[m.evaluate(square[r][c]).as_long() for c in range(3)] for r in range(3)]
    assert sorted(sum(grid, [])) == list(range(1, 10)), "Numbers 1-9 not all present"
    for r in range(3):
        assert sum(grid[r]) == 15, f"Row {r} sum != 15"
    for c in range(3):
        assert sum(grid[r][c] for r in range(3)) == 15, f"Col {c} sum != 15"
    assert grid[0][0] + grid[1][1] + grid[2][2] == 15, "Main diagonal sum != 15"
    assert grid[0][2] + grid[1][1] + grid[2][0] == 15, "Anti-diagonal sum != 15"
    print("All constraints verified.")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")