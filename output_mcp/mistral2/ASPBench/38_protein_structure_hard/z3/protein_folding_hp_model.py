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

# Constraint 3: Non-sequential contacts (only pairs with |i-j|>1 contribute to energy)
# Energy is the sum of -1 for each non-sequential H-H contact
energy = Int("energy")
opt.add(energy == Sum(
    If(
        And(
            i < j - 1,  # |i-j| > 1
            residue_types[i] == "H",
            residue_types[j] == "H",
            Or(
                And(coords[i][0] == coords[j][0] + 1, coords[i][1] == coords[j][1]),  # i is right of j
                And(coords[i][0] == coords[j][0] - 1, coords[i][1] == coords[j][1]),  # i is left of j
                And(coords[i][0] == coords[j][0], coords[i][1] == coords[j][1] + 1),  # i is above j
                And(coords[i][0] == coords[j][0], coords[i][1] == coords[j][1] - 1)   # i is below j
            )
        ),
        -1,
        0
    )
    for i in range(N) for j in range(i + 2, N)
))

# Objective: Minimize energy
opt.minimize(energy)

# Bounds for coordinates (to keep the problem tractable)
for i in range(N):
    x, y = coords[i]
    opt.add(x >= -10, x <= 10)
    opt.add(y >= -10, y <= 10)

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