from z3 import *

# Benchmark mode flag (True for benchmark mode)
BENCHMARK_MODE = True

# Create 3x3 matrix of integer variables
square = [[Int(f'c_{i}_{j}') for j in range(3)] for i in range(3)]
solver = Solver()

# Constraint 1: each cell is between 1 and 9
for i in range(3):
    for j in range(3):
        solver.add(square[i][j] >= 1, square[i][j] <= 9)

# Constraint 2: all numbers 1..9 appear exactly once (Distinct)
all_cells = [square[i][j] for i in range(3) for j in range(3)]
solver.add(Distinct(all_cells))

# Helper: sum of a list of Z3 expressions
def z3sum(lst):
    return Sum(lst)

magic_sum = 15

# Constraint 3: rows sum to 15
for i in range(3):
    solver.add(z3sum(square[i]) == magic_sum)

# Constraint 4: columns sum to 15
for j in range(3):
    solver.add(z3sum([square[i][j] for i in range(3)]) == magic_sum)

# Constraint 5: diagonals sum to 15
solver.add(z3sum([square[i][i] for i in range(3)]) == magic_sum)
solver.add(z3sum([square[i][2-i] for i in range(3)]) == magic_sum)

# Check for a solution
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for i in range(3):
        row_vals = [m.eval(square[i][j]).as_long() for j in range(3)]
        print(f"row{i+1} = {row_vals}")
    # Also print full square in matrix form
    print("square = [")
    for i in range(3):
        print("  [" + ", ".join(str(m.eval(square[i][j])) for j in range(3)) + "],")
    print("]")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (model-finding error, should refine)")
else:
    print("STATUS: unknown")