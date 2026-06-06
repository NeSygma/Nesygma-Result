from z3 import *

# Create solver
solver = Solver()

# Define positions 1 through 8 (1-indexed for clarity)
positions = [Int(f'pos_{i}') for i in range(1, 9)]

# Define composition variables
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
comp_vars = {c: Int(f'comp_{c}') for c in compositions}

# Each position has exactly one composition (1-8)
for i, pos in enumerate(positions):
    solver.add(pos >= 1, pos <= 8)
    # Each composition appears exactly once
    solver.add(Or([pos == i+1 for i in range(8)]))

# Each composition appears exactly once
for c in compositions:
    solver.add(comp_vars[c] >= 1, comp_vars[c] <= 8)
    # All distinct positions
solver.add(Distinct([comp_vars[c] for c in compositions]))

# Helper functions to get position of a composition
def get_pos(comp):
    return comp_vars[comp]

# Condition 1: T is performed either immediately before F or immediately after R
# T before F: pos_T + 1 == pos_F
# T after R: pos_T == pos_R + 1
solver.add(Or(
    get_pos('T') + 1 == get_pos('F'),
    get_pos('T') == get_pos('R') + 1
))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This means |pos_F - pos_R| >= 3 (at least 2 compositions between them)
solver.add(Or(
    get_pos('F') + 3 <= get_pos('R'),
    get_pos('R') + 3 <= get_pos('F')
))

# Condition 3: O is performed either first or fifth
solver.add(Or(
    get_pos('O') == 1,
    get_pos('O') == 5
))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(
    get_pos('L') == 8,
    get_pos('H') == 8
))

# Condition 5: P is performed at some time before S
solver.add(get_pos('P') < get_pos('S'))

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
# This means |pos_O - pos_S| >= 2 (at least 1 composition between them)
solver.add(Or(
    get_pos('O') + 2 <= get_pos('S'),
    get_pos('S') + 2 <= get_pos('O')
))

# Now test each answer choice
found_options = []

# Option A: L, P, S, R, O, T, F, H
opt_a = And(
    get_pos('L') == 1,
    get_pos('P') == 2,
    get_pos('S') == 3,
    get_pos('R') == 4,
    get_pos('O') == 5,
    get_pos('T') == 6,
    get_pos('F') == 7,
    get_pos('H') == 8
)

# Option B: O, T, P, F, S, H, R, L
opt_b = And(
    get_pos('O') == 1,
    get_pos('T') == 2,
    get_pos('P') == 3,
    get_pos('F') == 4,
    get_pos('S') == 5,
    get_pos('H') == 6,
    get_pos('R') == 7,
    get_pos('L') == 8
)

# Option C: P, T, F, S, L, R, O, H
opt_c = And(
    get_pos('P') == 1,
    get_pos('T') == 2,
    get_pos('F') == 3,
    get_pos('S') == 4,
    get_pos('L') == 5,
    get_pos('R') == 6,
    get_pos('O') == 7,
    get_pos('H') == 8
)

# Option D: P, T, F, S, O, R, L, H
opt_d = And(
    get_pos('P') == 1,
    get_pos('T') == 2,
    get_pos('F') == 3,
    get_pos('S') == 4,
    get_pos('O') == 5,
    get_pos('R') == 6,
    get_pos('L') == 7,
    get_pos('H') == 8
)

# Option E: T, F, P, R, O, L, S, H
opt_e = And(
    get_pos('T') == 1,
    get_pos('F') == 2,
    get_pos('P') == 3,
    get_pos('R') == 4,
    get_pos('O') == 5,
    get_pos('L') == 6,
    get_pos('S') == 7,
    get_pos('H') == 8
)

# Test each option
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")