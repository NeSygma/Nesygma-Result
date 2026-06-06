from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare the compositions as symbolic constants
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Create a solver
solver = Solver()

# Position variables: pos[i] = composition at position i (0-based index, representing 1-based position i+1)
# We will use IntSort() for positions, and the values will be the compositions represented as integers for easier constraints
# Map compositions to unique integers for Z3
comp_to_int = {c: i for i, c in enumerate(compositions)}
int_to_comp = {i: c for i, c in enumerate(compositions)}

# pos[i] is the composition (as an integer) at position i (0 to 7, representing 1 to 8)
pos = [Int(f'pos_{i}') for i in range(8)]

# Each position must be assigned a unique composition
solver.add(Distinct(pos))

# Helper: composition is in a position (0-based index)
def is_comp_at(comp, pos_idx):
    # pos_idx is 0-based (0 to 7)
    return pos[pos_idx] == comp_to_int[comp]

# Constraint 1: T is immediately before F or immediately after R
# Case 1: T immediately before F
solver.add(Or(
    And(is_comp_at('T', 0), is_comp_at('F', 1)),
    And(is_comp_at('T', 1), is_comp_at('F', 2)),
    And(is_comp_at('T', 2), is_comp_at('F', 3)),
    And(is_comp_at('T', 3), is_comp_at('F', 4)),
    And(is_comp_at('T', 4), is_comp_at('F', 5)),
    And(is_comp_at('T', 5), is_comp_at('F', 6)),
    And(is_comp_at('T', 6), is_comp_at('F', 7)),
    # Case 2: T immediately after R
    And(is_comp_at('R', 0), is_comp_at('T', 1)),
    And(is_comp_at('R', 1), is_comp_at('T', 2)),
    And(is_comp_at('R', 2), is_comp_at('T', 3)),
    And(is_comp_at('R', 3), is_comp_at('T', 4)),
    And(is_comp_at('R', 4), is_comp_at('T', 5)),
    And(is_comp_at('R', 5), is_comp_at('T', 6)),
    And(is_comp_at('R', 6), is_comp_at('T', 7))
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means there are at least two compositions between F and R in either order
# We will add constraints to ensure that if F and R are placed, the number of positions between them is >= 3
F_positions = [i for i in range(8)]
R_positions = [i for i in range(8)]
for i in F_positions:
    for j in R_positions:
        if i != j:
            # If F is at i and R is at j, then |i - j| >= 3
            solver.add(Implies(And(pos[i] == comp_to_int['F'], pos[j] == comp_to_int['R']), abs(i - j) >= 3))
            solver.add(Implies(And(pos[i] == comp_to_int['R'], pos[j] == comp_to_int['F']), abs(i - j) >= 3))

# Constraint 3: O is either first or fifth (0-based: pos 0 or 4)
solver.add(Or(is_comp_at('O', 0), is_comp_at('O', 4)))

# Constraint 4: The eighth composition (0-based pos 7) is either L or H
solver.add(Or(is_comp_at('L', 7), is_comp_at('H', 7)))

# Constraint 5: P is performed at some time before S
# Find the positions of P and S and ensure P's position < S's position
solver.add(Or(
    And(is_comp_at('P', 0), Or(is_comp_at('S', 1), is_comp_at('S', 2), is_comp_at('S', 3), is_comp_at('S', 4), is_comp_at('S', 5), is_comp_at('S', 6), is_comp_at('S', 7))),
    And(is_comp_at('P', 1), Or(is_comp_at('S', 2), is_comp_at('S', 3), is_comp_at('S', 4), is_comp_at('S', 5), is_comp_at('S', 6), is_comp_at('S', 7))),
    And(is_comp_at('P', 2), Or(is_comp_at('S', 3), is_comp_at('S', 4), is_comp_at('S', 5), is_comp_at('S', 6), is_comp_at('S', 7))),
    And(is_comp_at('P', 3), Or(is_comp_at('S', 4), is_comp_at('S', 5), is_comp_at('S', 6), is_comp_at('S', 7))),
    And(is_comp_at('P', 4), Or(is_comp_at('S', 5), is_comp_at('S', 6), is_comp_at('S', 7))),
    And(is_comp_at('P', 5), Or(is_comp_at('S', 6), is_comp_at('S', 7))),
    And(is_comp_at('P', 6), is_comp_at('S', 7))
))

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means there is at least one composition between O and S in either order
O_positions = [i for i in range(8)]
S_positions = [i for i in range(8)]
for i in O_positions:
    for j in S_positions:
        if i != j:
            # If O is at i and S is at j, then |i - j| >= 2 (at least one composition in between)
            solver.add(Implies(And(pos[i] == comp_to_int['O'], pos[j] == comp_to_int['S']), abs(i - j) >= 2))
            solver.add(Implies(And(pos[i] == comp_to_int['S'], pos[j] == comp_to_int['O']), abs(i - j) >= 2))

# Additional condition for the question: S is performed fourth (0-based pos 3)
solver.add(is_comp_at('S', 3))

# Now, evaluate the multiple-choice options under this condition
# Options are lists of three compositions for positions 0, 1, 2 (1st, 2nd, 3rd)
# We will check each option to see if it is possible

found_options = []

# Option A: F, H, P
solver.push()
solver.add(is_comp_at('F', 0))
solver.add(is_comp_at('H', 1))
solver.add(is_comp_at('P', 2))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H, P, L
solver.push()
solver.add(is_comp_at('H', 0))
solver.add(is_comp_at('P', 1))
solver.add(is_comp_at('L', 2))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: O, P, R
solver.push()
solver.add(is_comp_at('O', 0))
solver.add(is_comp_at('P', 1))
solver.add(is_comp_at('R', 2))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: O, P, T
solver.push()
solver.add(is_comp_at('O', 0))
solver.add(is_comp_at('P', 1))
solver.add(is_comp_at('T', 2))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P, R, T
solver.push()
solver.add(is_comp_at('P', 0))
solver.add(is_comp_at('R', 1))
solver.add(is_comp_at('T', 2))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")