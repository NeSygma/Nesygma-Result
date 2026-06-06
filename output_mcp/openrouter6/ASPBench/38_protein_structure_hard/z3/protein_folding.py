from z3 import *

# Protein sequence: HPHPHHPHPH (10 residues)
# Index 0 to 9
H = [True, False, True, False, True, True, False, True, False, True]  # True for H, False for P

# Variables for coordinates
x = [Int(f'x_{i}') for i in range(10)]
y = [Int(f'y_{i}') for i in range(10)]

solver = Optimize()

# 1. Self-avoiding walk: all positions distinct
for i in range(10):
    for j in range(i+1, 10):
        solver.add(Or(x[i] != x[j], y[i] != y[j]))

# 2. Connectivity: consecutive residues adjacent (Manhattan distance = 1)
for i in range(9):
    solver.add(Abs(x[i] - x[i+1]) + Abs(y[i] - y[i+1]) == 1)

# 3. Bound coordinates to reasonable range (optional but helps)
for i in range(10):
    solver.add(x[i] >= -10, x[i] <= 10)
    solver.add(y[i] >= -10, y[i] <= 10)

# 4. Define contact variables for non-sequential H pairs
contact = {}
total_contacts = 0
for i in range(10):
    for j in range(i+1, 10):
        if j - i > 1:  # non-sequential
            c = Bool(f'contact_{i}_{j}')
            contact[(i,j)] = c
            # Contact occurs iff both are H and Manhattan distance = 1
            solver.add(c == And(H[i], H[j], Abs(x[i] - x[j]) + Abs(y[i] - y[j]) == 1))
            total_contacts += If(c, 1, 0)

# 5. Maximize total contacts (which minimizes energy)
solver.maximize(total_contacts)

# Check and print results
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Coordinates:")
    coords = []
    for i in range(10):
        xi = m.evaluate(x[i])
        yi = m.evaluate(y[i])
        coords.append([int(xi.as_string()), int(yi.as_string())])
        print(f"Residue {i} ({'H' if H[i] else 'P'}): ({xi}, {yi})")
    print("sequence: HPHPHHPHPH")
    print("coordinates:", coords)
    # Compute energy from model
    energy = 0
    for (i,j), c_var in contact.items():
        if m.evaluate(c_var):
            energy -= 1
    print(f"Total energy: {energy}")
    print(f"Expected minimum energy: -4")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")