from z3 import *

# Define the compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Define the solver
solver = Solver()

# Create a list of 8 integer variables representing the order of compositions
# Each variable represents the position (1-8) of a composition
order = [Int(f'order_{i}') for i in range(8)]

# Each position must be assigned a unique composition
solver.add(Distinct(order))

# Helper function to get the composition at a given position
def get_comp(pos):
    return order[pos]

# Helper function to get the position of a given composition
# We need to define the inverse mapping: for each composition, its position
comp_pos = {comp: Int(f'pos_{comp}') for comp in compositions}
for comp in compositions:
    solver.add(comp_pos[comp] >= 0, comp_pos[comp] < 8)
    # Ensure that the position of comp is the index where order[i] == comp
    solver.add(Or([And(order[i] == comp, comp_pos[comp] == i) for i in range(8)]))

# Constraint 1: T is immediately before F or immediately after R
# Case 1: T is immediately before F
solver.add(Or(
    And(comp_pos['T'] + 1 == comp_pos['F']),
    And(comp_pos['R'] + 1 == comp_pos['T'])
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the number of compositions between F and R (in either order) must be at least 2
# We need to ensure that the absolute difference in positions is at least 3 (since positions are 0-based)
solver.add(Or(
    And(comp_pos['F'] < comp_pos['R'], comp_pos['R'] - comp_pos['F'] >= 3),
    And(comp_pos['R'] < comp_pos['F'], comp_pos['F'] - comp_pos['R'] >= 3)
))

# Constraint 3: O is performed either first or fifth
solver.add(Or(comp_pos['O'] == 0, comp_pos['O'] == 4))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(order[7] == 'L', order[7] == 'H'))

# Constraint 5: P is performed at some time before S
solver.add(comp_pos['P'] < comp_pos['S'])

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means there is at least one composition between O and S (in either order)
solver.add(Or(
    And(comp_pos['O'] < comp_pos['S'], comp_pos['S'] - comp_pos['O'] >= 2),
    And(comp_pos['S'] < comp_pos['O'], comp_pos['O'] - comp_pos['S'] >= 2)
))

# Now, evaluate each answer choice
found_options = []

# Option A: L, P, S, R, O, T, F, H
solver.push()
solver.add(order[0] == 'L')
solver.add(order[1] == 'P')
solver.add(order[2] == 'S')
solver.add(order[3] == 'R')
solver.add(order[4] == 'O')
solver.add(order[5] == 'T')
solver.add(order[6] == 'F')
solver.add(order[7] == 'H')
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: O, T, P, F, S, H, R, L
solver.push()
solver.add(order[0] == 'O')
solver.add(order[1] == 'T')
solver.add(order[2] == 'P')
solver.add(order[3] == 'F')
solver.add(order[4] == 'S')
solver.add(order[5] == 'H')
solver.add(order[6] == 'R')
solver.add(order[7] == 'L')
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: P, T, F, S, L, R, O, H
solver.push()
solver.add(order[0] == 'P')
solver.add(order[1] == 'T')
solver.add(order[2] == 'F')
solver.add(order[3] == 'S')
solver.add(order[4] == 'L')
solver.add(order[5] == 'R')
solver.add(order[6] == 'O')
solver.add(order[7] == 'H')
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: P, T, F, S, O, R, L, H
solver.push()
solver.add(order[0] == 'P')
solver.add(order[1] == 'T')
solver.add(order[2] == 'F')
solver.add(order[3] == 'S')
solver.add(order[4] == 'O')
solver.add(order[5] == 'R')
solver.add(order[6] == 'L')
solver.add(order[7] == 'H')
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: T, F, P, R, O, L, S, H
solver.push()
solver.add(order[0] == 'T')
solver.add(order[1] == 'F')
solver.add(order[2] == 'P')
solver.add(order[3] == 'R')
solver.add(order[4] == 'O')
solver.add(order[5] == 'L')
solver.add(order[6] == 'S')
solver.add(order[7] == 'H')
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