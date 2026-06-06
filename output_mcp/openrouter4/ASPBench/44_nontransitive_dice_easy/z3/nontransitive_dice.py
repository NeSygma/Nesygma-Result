from z3 import *

solver = Solver()

# Declare 6 faces for each die
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Constraint: each face value must be in {0, 1, 2, 3, 4, 5, 6}
for die in [A, B, C]:
    for face in die:
        solver.add(face >= 0, face <= 6)

# Count wins: A beats B (more than 18 of 36 matchups)
wins_A_vs_B = Sum([If(A[i] > B[j], 1, 0) for i in range(6) for j in range(6)])
solver.add(wins_A_vs_B > 18)

# Count wins: B beats C
wins_B_vs_C = Sum([If(B[i] > C[j], 1, 0) for i in range(6) for j in range(6)])
solver.add(wins_B_vs_C > 18)

# Count wins: C beats A
wins_C_vs_A = Sum([If(C[i] > A[j], 1, 0) for i in range(6) for j in range(6)])
solver.add(wins_C_vs_A > 18)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    
    # Extract face values using as_long() for Z3 integer objects
    a_vals = [m.eval(A[i]).as_long() for i in range(6)]
    b_vals = [m.eval(B[i]).as_long() for i in range(6)]
    c_vals = [m.eval(C[i]).as_long() for i in range(6)]
    
    print(f"Die A: {a_vals}")
    print(f"Die B: {b_vals}")
    print(f"Die C: {c_vals}")
    
    # Compute win probabilities
    wins_ab = sum(1 for i in range(6) for j in range(6) if a_vals[i] > b_vals[j])
    wins_bc = sum(1 for i in range(6) for j in range(6) if b_vals[i] > c_vals[j])
    wins_ca = sum(1 for i in range(6) for j in range(6) if c_vals[i] > a_vals[j])
    
    print(f"A beats B: {wins_ab}/36 = {wins_ab/36:.4f}")
    print(f"B beats C: {wins_bc}/36 = {wins_bc/36:.4f}")
    print(f"C beats A: {wins_ca}/36 = {wins_ca/36:.4f}")
    
    # Output in the requested format
    print()
    print("dice = {")
    print(f'    "A": {a_vals},')
    print(f'    "B": {b_vals},')
    print(f'    "C": {c_vals}')
    print("}")
    print("win_probabilities = {")
    print(f'    "A_beats_B": {wins_ab/36:.4f},')
    print(f'    "B_beats_C": {wins_bc/36:.4f},')
    print(f'    "C_beats_A": {wins_ca/36:.4f}')
    print("}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")