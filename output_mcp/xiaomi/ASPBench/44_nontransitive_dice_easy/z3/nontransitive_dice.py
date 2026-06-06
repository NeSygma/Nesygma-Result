from z3 import *

solver = Solver()

# Three dice, each with 6 faces, values in {0..6}
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Domain constraints: each face value in {0, 1, 2, 3, 4, 5, 6}
for d in [A, B, C]:
    for f in d:
        solver.add(f >= 0, f <= 6)

# Non-decreasing order for each die (to break symmetry and reduce search space)
for d in [A, B, C]:
    for i in range(5):
        solver.add(d[i] <= d[i+1])

# Helper: count wins of die X over die Y
# For each pair (i,j), X[i] > Y[j] contributes 1 win
def count_wins(X, Y):
    return Sum([If(X[i] > Y[j], 1, 0) for i in range(6) for j in range(6)])

# A beats B: wins > 18 (strictly more than half of 36)
solver.add(count_wins(A, B) >= 19)
# B beats C: wins > 18
solver.add(count_wins(B, C) >= 19)
# C beats A: wins > 18
solver.add(count_wins(C, A) >= 19)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    a_vals = [m[A[i]].as_long() for i in range(6)]
    b_vals = [m[B[i]].as_long() for i in range(6)]
    c_vals = [m[C[i]].as_long() for i in range(6)]

    # Compute actual win counts
    ab_wins = sum(1 for i in range(6) for j in range(6) if a_vals[i] > b_vals[j])
    bc_wins = sum(1 for i in range(6) for j in range(6) if b_vals[i] > c_vals[j])
    ca_wins = sum(1 for i in range(6) for j in range(6) if c_vals[i] > a_vals[j])

    print("STATUS: sat")
    print(f"Dice A: {a_vals}")
    print(f"Dice B: {b_vals}")
    print(f"Dice C: {c_vals}")
    print(f"A beats B: {ab_wins}/36 = {ab_wins/36:.4f}")
    print(f"B beats C: {bc_wins}/36 = {bc_wins/36:.4f}")
    print(f"C beats A: {ca_wins}/36 = {ca_wins/36:.4f}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")