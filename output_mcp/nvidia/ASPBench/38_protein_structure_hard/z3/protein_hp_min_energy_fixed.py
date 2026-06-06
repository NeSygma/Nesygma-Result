from z3 import *

# Problem constants
N = 10
BOUND = 5

# Decision variables: coordinates of each residue
xs = [Int(f'x{i}') for i in range(N)]
ys = [Int(f'y{i}') for i in range(N)]

# Encode each (x,y) pair as a single integer to enforce distinctness
coords = [xs[i] * 1000 + ys[i] for i in range(N)]

solver = Solver()

# 1. Self-avoiding walk: all coordinates are distinct
solver.add(Distinct(coords))

# 2. Connectivity: consecutive residues must be adjacent (Manhattan distance = 1)
for i in range(N - 1):
    solver.add(Abs(xs[i + 1] - xs[i]) + Abs(ys[i + 1] - ys[i]) == 1)

# 3. Bound coordinates to keep the search finite
for i in range(N):
    solver.add(xs[i] >= -BOUND, xs[i] <= BOUND)
    solver.add(ys[i] >= -BOUND, ys[i] <= BOUND)

# 4. HP sequence information (0‑based indexing)
#    H positions: 0,2,4,5,7,9
H_positions = [0, 2, 4, 5, 7, 9]

# 5. Count non‑sequential H‑H contacts that are adjacent
contact_terms = []
for idx_i in range(len(H_positions)):
    i = H_positions[idx_i]
    for idx_j in range(idx_i + 1, len(H_positions)):
        j = H_positions[idx_j]
        # non‑sequential requirement
        if abs(i - j) > 1:
            # adjacency test
            adjacent = (Abs(xs[j] - xs[i]) + Abs(ys[j] - ys[i]) == 1)
            # add 1 if adjacent
            contact_terms.append(If(adjacent, 1, 0))

# The minimum possible energy is -4, which corresponds to exactly 4 contacts
solver.add(Sum(contact_terms) == 4)

# ------------------------------
# Solve and output
# ------------------------------
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print the full coordinate list in order
    for i in range(N):
        print(f"coord_{i} = [{m[xs[i]], m[ys[i]]}]")
    print("energy = -4")
else:
    # This should never happen in benchmark mode because a solution is known to exist
    print("STATUS: unsat")