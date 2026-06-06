from z3 import *

# Define the compositions as symbolic constants
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]

# Define the solver
solver = Solver()

# Create a list of 8 integer variables representing the order of compositions
# Each variable represents the composition at a given position (0-7)
order = [Int(f'order_{i}') for i in range(8)]

# Each position must be assigned a unique composition
solver.add(Distinct(order))

# Helper function to get the position of a given composition
comp_pos = {}
for comp in compositions:
    comp_pos[comp] = Int(f'pos_{comp}')
    solver.add(comp_pos[comp] >= 0, comp_pos[comp] < 8)

# Link the order list to the positions
for i in range(8):
    solver.add(Or([order[i] == comp for comp in compositions]))

for comp in compositions:
    solver.add(Or([And(order[i] == comp, comp_pos[comp] == i) for i in range(8)]))

# Constraint 1: T is immediately before F or immediately after R
# Case 1: T is immediately before F
# Case 2: T is immediately after R
solver.add(Or(
    And(comp_pos[T] + 1 == comp_pos[F]),
    And(comp_pos[R] + 1 == comp_pos[T])
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the number of compositions between F and R (in either order) must be at least 2
solver.add(Or(
    And(comp_pos[F] < comp_pos[R], comp_pos[R] - comp_pos[F] >= 3),
    And(comp_pos[R] < comp_pos[F], comp_pos[F] - comp_pos[R] >= 3)
))

# Constraint 3: O is performed either first or fifth
solver.add(Or(comp_pos[O] == 0, comp_pos[O] == 4))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(order[7] == L, order[7] == H))

# Constraint 5: P is performed at some time before S
solver.add(comp_pos[P] < comp_pos[S])

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means there is at least one composition between O and S (in either order)
solver.add(Or(
    And(comp_pos[O] < comp_pos[S], comp_pos[S] - comp_pos[O] >= 2),
    And(comp_pos[S] < comp_pos[O], comp_pos[O] - comp_pos[S] >= 2)
))

# Now, evaluate each answer choice
found_options = []

# Helper function to check an option
def check_option(name, assignments):
    solver.push()
    for pos, comp in enumerate(assignments):
        solver.add(order[pos] == comp)
    if solver.check() == sat:
        found_options.append(name)
    solver.pop()

# Option A: L, P, S, R, O, T, F, H
check_option("A", [L, P, S, R, O, T, F, H])

# Option B: O, T, P, F, S, H, R, L
check_option("B", [O, T, P, F, S, H, R, L])

# Option C: P, T, F, S, L, R, O, H
check_option("C", [P, T, F, S, L, R, O, H])

# Option D: P, T, F, S, O, R, L, H
check_option("D", [P, T, F, S, O, R, L, H])

# Option E: T, F, P, R, O, L, S, H
check_option("E", [T, F, P, R, O, L, S, H])

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