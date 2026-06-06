from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Protein sequence
sequence = "HPHPHHPHPH"

# Number of residues
N = len(sequence)

# Create a solver for optimization
opt = Optimize()

# Declare coordinates for each residue
coords = [[Int(f"x_{i}"), Int(f"y_{i}")] for i in range(N)]

# Residue types
residue_types = [ch for ch in sequence]

# Constraint 1: Self-avoiding walk (all coordinates are distinct)
all_coords = [coord for pair in coords for coord in pair]
opt.add(Distinct(all_coords))

# Constraint 2: Connectivity (consecutive residues are adjacent)
for i in range(N - 1):
    x1, y1 = coords[i]
    x2, y2 = coords[i + 1]
    opt.add(Or(
        And(x2 == x1 + 1, y2 == y1),  # right
        And(x2 == x1 - 1, y2 == y1),  # left
        And(x2 == x1, y2 == y1 + 1),  # up
        And(x2 == x1, y2 == y1 - 1)   # down
    ))

# Energy calculation: Sum of -1 for each non-sequential H-H contact
energy = Int("energy")

# List to store the conditions for each H-H contact
contact_conditions = []

# Iterate over all pairs of residues
for i in range(N):
    for j in range(i + 2, N):  # |i-j| > 1
        xi, yi = coords[i]
        xj, yj = coords[j]
        # Check if residues i and j are adjacent (Manhattan distance = 1)
        adjacent = Or(
            And(xi == xj + 1, yi == yj),
            And(xi == xj - 1, yi == yj),
            And(xi == xj, yi == yj + 1),
            And(xi == xj, yi == yj - 1)
        )
        # Check if both residues are H
        both_H = And(residue_types[i] == "H", residue_types[j] == "H")
        # Add the condition for this contact
        contact_conditions.append(And(adjacent, both_H))

# Energy is the sum of -1 for each contact
opt.add(energy == -Sum([If(cond, 1, 0) for cond in contact_conditions]))

# Objective: Minimize energy
opt.minimize(energy)

# Bounds for coordinates (relaxed to allow more flexibility)
for i in range(N):
    x, y = coords[i]
    opt.add(x >= -20, x <= 20)
    opt.add(y >= -20, y <= 20)

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Minimum energy found:", model[energy])
    print("Coordinates:")
    for i in range(N):
        x, y = coords[i]
        print(f"Residue {i+1} ({residue_types[i]}): ({model[x]}, {model[y]})")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")