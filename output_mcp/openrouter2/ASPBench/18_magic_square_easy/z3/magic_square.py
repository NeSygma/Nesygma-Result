from z3 import *

solver = Solver()
# Create 3x3 grid of Int variables
square = [[Int(f's_{i}_{j}') for j in range(3)] for i in range(3)]
# Each cell 1..9
for i in range(3):
    for j in range(3):
        solver.add(square[i][j] >= 1, square[i][j] <= 9)
# All numbers distinct
cells = [square[i][j] for i in range(3) for j in range(3)]
solver.add(Distinct(cells))
# Row sums
for i in range(3):
    solver.add(Sum(square[i][0], square[i][1], square[i][2]) == 15)
# Column sums
for j in range(3):
    solver.add(Sum(square[0][j], square[1][j], square[2][j]) == 15)
# Diagonals
solver.add(Sum(square[0][0], square[1][1], square[2][2]) == 15)
solver.add(Sum(square[0][2], square[1][1], square[2][0]) == 15)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    # Extract square values
    sq_vals = [[m.eval(square[i][j], model_completion=True).as_long() for j in range(3)] for i in range(3)]
    print("STATUS: sat")
    print("square =", sq_vals)
    print("magic_sum = 15")
    print("valid = True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")