from z3 import *

# Create solver
solver = Solver()

# Each die has 6 faces, values from {0, 1, 2, 3, 4, 5, 6}
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Domain constraints: each face value in {0, 1, 2, 3, 4, 5, 6}
for die in [A, B, C]:
    for face in die:
        solver.add(face >= 0)
        solver.add(face <= 6)

# --- Helper: count how many of the 36 matchups X beats Y ---
# X beats Y if X[i] > Y[j]
# We'll create symbolic counts using If/Sum

def count_wins(X, Y):
    """Return Z3 expression for number of (i,j) pairs where X[i] > Y[j]"""
    return Sum([If(X[i] > Y[j], 1, 0) for i in range(6) for j in range(6)])

# A beats B: P(A > B) > 0.5  => wins > 18
wins_A_over_B = count_wins(A, B)
solver.add(wins_A_over_B > 18)

# B beats C: P(B > C) > 0.5  => wins > 18
wins_B_over_C = count_wins(B, C)
solver.add(wins_B_over_C > 18)

# C beats A: P(C > A) > 0.5  => wins > 18
wins_C_over_A = count_wins(C, A)
solver.add(wins_C_over_A > 18)

# Also ensure no ties dominate: we want strict > 0.5, so > 18 is correct for 36 matchups.
# But we should also consider ties: if X[i] == Y[j], that's not a win for either.
# The count_wins function correctly counts only strict >.

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    
    # Extract face values
    A_vals = [m.eval(A[i]).as_long() for i in range(6)]
    B_vals = [m.eval(B[i]).as_long() for i in range(6)]
    C_vals = [m.eval(C[i]).as_long() for i in range(6)]
    
    # Compute actual win counts
    def compute_wins(X_vals, Y_vals):
        cnt = 0
        for x in X_vals:
            for y in Y_vals:
                if x > y:
                    cnt += 1
        return cnt
    
    w_AB = compute_wins(A_vals, B_vals)
    w_BC = compute_wins(B_vals, C_vals)
    w_CA = compute_wins(C_vals, A_vals)
    
    print("STATUS: sat")
    print(f"A = {A_vals}")
    print(f"B = {B_vals}")
    print(f"C = {C_vals}")
    print(f"A beats B: {w_AB}/36 = {w_AB/36:.4f}")
    print(f"B beats C: {w_BC}/36 = {w_BC/36:.4f}")
    print(f"C beats A: {w_CA}/36 = {w_CA/36:.4f}")
    
    # Output in requested format
    print()
    print("dice = {")
    print(f'    "A": {A_vals},')
    print(f'    "B": {B_vals},')
    print(f'    "C": {C_vals}')
    print("}")
    print("win_probabilities = {")
    print(f'    "A_beats_B": {w_AB/36:.4f},')
    print(f'    "B_beats_C": {w_BC/36:.4f},')
    print(f'    "C_beats_A": {w_CA/36:.4f}')
    print("}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")