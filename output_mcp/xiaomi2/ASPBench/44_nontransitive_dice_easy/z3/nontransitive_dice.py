from z3 import *

solver = Solver()

# Declare dice face variables
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Domain constraints: each face value in {0,1,2,3,4,5,6}
for die in [A, B, C]:
    for face in die:
        solver.add(face >= 0, face <= 6)

# Symmetry breaking: sort faces within each die (non-decreasing)
for die in [A, B, C]:
    for i in range(5):
        solver.add(die[i] <= die[i+1])

# Count wins: die X beats die Y if X[i] > Y[j]
# For 6-sided dice, there are 36 matchups; need > 18 wins
def win_count(X, Y):
    return Sum([If(X[i] > Y[j], 1, 0) for i in range(6) for j in range(6)])

# A beats B: more than 18 wins out of 36
solver.add(win_count(A, B) > 18)
# B beats C: more than 18 wins out of 36
solver.add(win_count(B, C) > 18)
# C beats A: more than 18 wins out of 36
solver.add(win_count(C, A) > 18)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    a_vals = [m[A[i]].as_long() for i in range(6)]
    b_vals = [m[B[i]].as_long() for i in range(6)]
    c_vals = [m[C[i]].as_long() for i in range(6)]

    # Compute actual win probabilities
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