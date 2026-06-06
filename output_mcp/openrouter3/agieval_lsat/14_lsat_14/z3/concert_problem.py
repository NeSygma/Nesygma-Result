from z3 import *

# Create solver
solver = Solver()

# Define positions for each composition
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# Domain constraints: each position is between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions must be distinct (exactly one composition per position)
solver.add(Distinct([pos[c] for c in compositions]))

# Additional constraints from the problem
# 1. T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# 2. At least two compositions between F and R
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# 3. O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# 4. Eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# 5. P before S
solver.add(pos['P'] < pos['S'])

# 6. At least one composition between O and S
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Question-specific constraints
solver.add(pos['T'] == 5)  # T is fifth
solver.add(pos['F'] == 6)  # F is sixth

# Now test each answer choice
# Answer choices:
# (A) fourth or seventh
# (B) third or sixth
# (C) third or fourth
# (D) second or seventh
# (E) first or fourth

# Define constraints for each option
opt_a = Or(pos['S'] == 4, pos['S'] == 7)
opt_b = Or(pos['S'] == 3, pos['S'] == 6)
opt_c = Or(pos['S'] == 3, pos['S'] == 4)
opt_d = Or(pos['S'] == 2, pos['S'] == 7)
opt_e = Or(pos['S'] == 1, pos['S'] == 4)

# Use the exact skeleton for multiple choice evaluation
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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