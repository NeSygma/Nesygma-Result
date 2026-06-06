from z3 import *

# Base constraints for the concert scheduling problem
solver = Solver()

# Compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
comp_consts = {c: Int(c) for c in compositions}

# Positions: 0 to 7 (0 = first, 7 = eighth)
positions = [Int(f'pos_{i}') for i in range(8)]

# Each position must be assigned a unique composition
solver.add(Distinct(positions))

# Helper: Map compositions to positions
for c in compositions:
    solver.add(Or([positions[i] == comp_consts[c] for i in range(8)]))

# Constraint 1: T is performed either immediately before F or immediately after R
# Case 1: T immediately before F (T at i, F at i+1)
# Case 2: T immediately after R (R at i, T at i+1)
solver.add(Or(
    # Case 1: T immediately before F
    Or([And(positions[i] == comp_consts['T'], positions[i+1] == comp_consts['F']) for i in range(7)]),
    # Case 2: T immediately after R
    Or([And(positions[i] == comp_consts['R'], positions[i+1] == comp_consts['T']) for i in range(7)])
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the number of compositions between F and R (in either order) is at least 2
# We need to ensure that the distance between F and R is at least 3 (since at least two compositions are between them)
# So, |position(F) - position(R)| >= 3
solver.add(Or(
    # F before R, at least two compositions between them
    And(
        comp_consts['F'] < comp_consts['R'],
        comp_consts['R'] - comp_consts['F'] >= 3
    ),
    # R before F, at least two compositions between them
    And(
        comp_consts['R'] < comp_consts['F'],
        comp_consts['F'] - comp_consts['R'] >= 3
    )
))

# Constraint 3: O is performed either first or fifth
solver.add(Or(
    positions[0] == comp_consts['O'],
    positions[4] == comp_consts['O']
))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(
    positions[7] == comp_consts['L'],
    positions[7] == comp_consts['H']
))

# Constraint 5: P is performed at some time before S
solver.add(comp_consts['P'] < comp_consts['S'])

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means that O and S are not adjacent, and there is at least one composition between them in either order
# So, |position(O) - position(S)| >= 2
solver.add(Or(
    # O before S, at least one composition between them
    And(
        comp_consts['O'] < comp_consts['S'],
        comp_consts['S'] - comp_consts['O'] >= 2
    ),
    # S before O, at least one composition between them
    And(
        comp_consts['S'] < comp_consts['O'],
        comp_consts['O'] - comp_consts['S'] >= 2
    )
))

# Now, test each option for P's position
found_options = []

# Option A: P is second (position 1)
opt_a_constr = (positions[1] == comp_consts['P'])
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: P is third (position 2)
opt_b_constr = (positions[2] == comp_consts['P'])
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: P is fourth (position 3)
opt_c_constr = (positions[3] == comp_consts['P'])
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: P is sixth (position 5)
opt_d_constr = (positions[5] == comp_consts['P'])
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P is seventh (position 6)
opt_e_constr = (positions[6] == comp_consts['P'])
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")