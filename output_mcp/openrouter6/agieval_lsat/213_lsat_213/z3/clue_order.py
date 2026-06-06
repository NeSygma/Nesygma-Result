from z3 import *

solver = Solver()

# Define position variables for each clue
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
pos = {c: Int(f'pos_{c}') for c in clues}

# Base constraints: each position between 1 and 7, all distinct
for c in clues:
    solver.add(pos[c] >= 1, pos[c] <= 7)
solver.add(Distinct([pos[c] for c in clues]))

# Constraint 1: T cannot be in chapter 1
solver.add(pos['T'] != 1)

# Constraint 2: T before W, exactly two chapters separating => W = T + 3
solver.add(pos['W'] == pos['T'] + 3)

# Helper for absolute difference
def abs_diff(a, b):
    return If(a > b, a - b, b - a)

# Constraint 3: S and Z not adjacent
solver.add(abs_diff(pos['S'], pos['Z']) != 1)

# Constraint 4: W and X not adjacent
solver.add(abs_diff(pos['W'], pos['X']) != 1)

# Constraint 5: U and X adjacent
solver.add(abs_diff(pos['U'], pos['X']) == 1)

# Now evaluate each answer choice
found_options = []

# Option A: S, T, Z, X, U, W, R
opt_a_constr = And(
    pos['S'] == 1,
    pos['T'] == 2,
    pos['Z'] == 3,
    pos['X'] == 4,
    pos['U'] == 5,
    pos['W'] == 6,
    pos['R'] == 7
)

# Option B: T, X, U, W, S, R, Z
opt_b_constr = And(
    pos['T'] == 1,
    pos['X'] == 2,
    pos['U'] == 3,
    pos['W'] == 4,
    pos['S'] == 5,
    pos['R'] == 6,
    pos['Z'] == 7
)

# Option C: U, S, X, T, Z, R, W
opt_c_constr = And(
    pos['U'] == 1,
    pos['S'] == 2,
    pos['X'] == 3,
    pos['T'] == 4,
    pos['Z'] == 5,
    pos['R'] == 6,
    pos['W'] == 7
)

# Option D: X, U, T, Z, R, W, S
opt_d_constr = And(
    pos['X'] == 1,
    pos['U'] == 2,
    pos['T'] == 3,
    pos['Z'] == 4,
    pos['R'] == 5,
    pos['W'] == 6,
    pos['S'] == 7
)

# Option E: Z, R, T, U, X, W, S
opt_e_constr = And(
    pos['Z'] == 1,
    pos['R'] == 2,
    pos['T'] == 3,
    pos['U'] == 4,
    pos['X'] == 5,
    pos['W'] == 6,
    pos['S'] == 7
)

options = [
    ("A", opt_a_constr),
    ("B", opt_b_constr),
    ("C", opt_c_constr),
    ("D", opt_d_constr),
    ("E", opt_e_constr)
]

for letter, constr in options:
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