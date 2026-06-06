from z3 import *

# Solver instance
solver = Solver()

# Declare die face variables
A = [Int(f'A_{i}') for i in range(4)]
B = [Int(f'B_{i}') for i in range(4)]
C = [Int(f'C_{i}') for i in range(4)]
D = [Int(f'D_{i}') for i in range(4)]

# Value range constraints
for die in [A, B, C, D]:
    for v in die:
        solver.add(v >= 1, v <= 8)

# Sorted constraints
for die in [A, B, C, D]:
    solver.add(die[0] <= die[1], die[1] <= die[2], die[2] <= die[3])

# Sum equality constraints
sumA = Sum(A)
sumB = Sum(B)
sumC = Sum(C)
sumD = Sum(D)
solver.add(sumA == sumB, sumA == sumC, sumA == sumD)

# Win count expressions
wAB = Sum([If(A[i] > B[j], 1, 0) for i in range(4) for j in range(4)])
wBC = Sum([If(B[i] > C[j], 1, 0) for i in range(4) for j in range(4)])
wCD = Sum([If(C[i] > D[j], 1, 0) for i in range(4) for j in range(4)])
wDA = Sum([If(D[i] > A[j], 1, 0) for i in range(4) for j in range(4)])

# Win threshold constraints (>8 wins out of 16)
solver.add(wAB > 8, wBC > 8, wCD > 8, wDA > 8)

# Unique value set constraints
# Helper to get presence bool for a value v in a die

def presence(die, v):
    return Or([die[i] == v for i in range(4)])

# For each pair of dice, ensure their sets of values differ
pairs = [(A, B), (A, C), (A, D), (B, C), (B, D), (C, D)]
for die1, die2 in pairs:
    diff = Or([Xor(presence(die1, v), presence(die2, v)) for v in range(1, 9)])
    solver.add(diff)

# Check satisfiability
result = solver.check()

if result == sat:
    m = solver.model()
    # Extract values
    A_vals = [m.evaluate(v, model_completion=True).as_long() for v in A]
    B_vals = [m.evaluate(v, model_completion=True).as_long() for v in B]
    C_vals = [m.evaluate(v, model_completion=True).as_long() for v in C]
    D_vals = [m.evaluate(v, model_completion=True).as_long() for v in D]
    common_sum = m.evaluate(sumA, model_completion=True).as_long()
    wAB_val = m.evaluate(wAB, model_completion=True).as_long()
    wBC_val = m.evaluate(wBC, model_completion=True).as_long()
    wCD_val = m.evaluate(wCD, model_completion=True).as_long()
    wDA_val = m.evaluate(wDA, model_completion=True).as_long()
    print("STATUS: sat")
    print("dice = {")
    print(f"  A: {A_vals},")
    print(f"  B: {B_vals},")
    print(f"  C: {C_vals},")
    print(f"  D: {D_vals}\n}}")
    print("analysis = {")
    print(f"  common_sum: {common_sum},")
    print("  win_counts: {")
    print(f"    A_beats_B: {wAB_val},")
    print(f"    B_beats_C: {wBC_val},")
    print(f"    C_beats_D: {wCD_val},")
    print(f"    D_beats_A: {wDA_val}\n  }}")
    print("}")
elif result == unsat:
    print("STATUS: unsat")
    # In benchmark mode, unsat is non-terminal; we could trigger refinement
else:
    print("STATUS: unknown")