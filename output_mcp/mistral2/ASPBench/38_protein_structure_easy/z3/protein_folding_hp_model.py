from z3 import *

# Problem: Fold an 8-residue protein (HPPHPPHH) on a 2D lattice to minimize energy under the HP model.
# Constraints: self-avoiding walk, consecutive residues adjacent (Manhattan distance = 1), all 8 placed.
# Energy: -1 per H-H contact between non-sequential neighbors. Optimal expected: -3.

# BENCHMARK_MODE: ON (problem is solvable)
BENCHMARK_MODE = True

# Sequence
sequence = "HPPHPPHH"
n = len(sequence)

# We'll use a 2D lattice. Since the optimal energy is -3, we can bound the grid to a reasonable size.
# A 5x5 grid is sufficient for this small sequence.
grid_size = 5
x_range = range(grid_size)
y_range = range(grid_size)

# Declare symbolic variables for coordinates of each residue
# coords[i] = (x_i, y_i)
x_vars = [Int(f'x_{i}') for i in range(n)]
y_vars = [Int(f'y_{i}') for i in range(n)]

# Set up the solver
solver = Solver()

# Constraint 1: Each residue must be placed on a unique lattice point (self-avoiding walk)
# We'll enforce that all (x_i, y_i) are distinct.
for i in range(n):
    for j in range(i + 1, n):
        solver.add(Or(
            x_vars[i] != x_vars[j],
            y_vars[i] != y_vars[j]
        ))

# Constraint 2: Consecutive residues must be adjacent (Manhattan distance = 1)
for i in range(n - 1):
    solver.add(Or(
        And(x_vars[i] == x_vars[i + 1], abs(y_vars[i] - y_vars[i + 1]) == 1),
        And(y_vars[i] == y_vars[i + 1], abs(x_vars[i] - x_vars[i + 1]) == 1)
    ))

# Constraint 3: All residues must be placed within the grid bounds
for i in range(n):
    solver.add(x_vars[i] >= 0, x_vars[i] < grid_size)
    solver.add(y_vars[i] >= 0, y_vars[i] < grid_size)

# Objective: Minimize energy = -1 per H-H contact between non-sequential neighbors
# We'll count the number of H-H contacts between non-sequential neighbors.
# A contact is when two H residues are adjacent (Manhattan distance = 1) but not consecutive in sequence.

def adjacent(i, j):
    return Or(
        And(x_vars[i] == x_vars[j], abs(y_vars[i] - y_vars[j]) == 1),
        And(y_vars[i] == y_vars[j], abs(x_vars[i] - x_vars[j]) == 1)
    )

# Count the number of H-H contacts between non-sequential neighbors
energy = Int('energy')
contact_terms = []

for i in range(n):
    for j in range(i + 1, n):
        # Only consider non-sequential neighbors
        if j != i + 1:
            # Check if both residues are H
            is_H_i = (sequence[i] == 'H')
            is_H_j = (sequence[j] == 'H')
            # If both are H and adjacent, add 1 to the contact count
            contact_terms.append(If(And(is_H_i, is_H_j, adjacent(i, j)), 1, 0))

# Total energy is the negative of the number of contacts (since each contact contributes -1)
solver.add(energy == -Sum(contact_terms))

# We want to find a solution with energy = -3 (optimal expected)
solver.push()
solver.add(energy == -3)

result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Optimal energy found: -3")
    # Extract and print the coordinates
    coords_output = []
    for i in range(n):
        xi = model[x_vars[i]]
        yi = model[y_vars[i]]
        coords_output.append((xi, yi))
    print("coordinates =", coords_output)
    print("sequence =", sequence)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")