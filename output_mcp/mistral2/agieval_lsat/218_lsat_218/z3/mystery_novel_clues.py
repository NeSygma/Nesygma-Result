from z3 import *

# Base constraints for the mystery novel clues problem
solver = Solver()

# Declare symbolic variables for the chapters (1 to 7)
chapters = [Int(f'chapter_{i}') for i in range(1, 8)]

# Declare symbolic variables for the clues
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
clue_vars = {clue: Int(f'clue_{clue}') for clue in clues}

# Each chapter must have exactly one clue
for i in range(7):
    solver.add(And(clue_vars['R'] <= 7, clue_vars['R'] >= 1))
    solver.add(And(clue_vars['S'] <= 7, clue_vars['S'] >= 1))
    solver.add(And(clue_vars['T'] <= 7, clue_vars['T'] >= 1))
    solver.add(And(clue_vars['U'] <= 7, clue_vars['U'] >= 1))
    solver.add(And(clue_vars['W'] <= 7, clue_vars['W'] >= 1))
    solver.add(And(clue_vars['X'] <= 7, clue_vars['X'] >= 1))
    solver.add(And(clue_vars['Z'] <= 7, clue_vars['Z'] >= 1))

# Each clue must appear exactly once
solver.add(Distinct(list(clue_vars.values())))

# T cannot be mentioned in chapter 1 (original constraint)
solver.add(clue_vars['T'] != 1)

# T must be mentioned before W, with exactly two chapters separating T and W
# This means W = T + 3
solver.add(clue_vars['W'] == clue_vars['T'] + 3)

# S and Z cannot be mentioned in adjacent chapters
for c1, c2 in [(clue_vars['S'], clue_vars['Z']), (clue_vars['Z'], clue_vars['S'])]:
    for i in range(1, 7):
        solver.add(Or(c1 != i, c2 != i + 1))
        solver.add(Or(c1 != i + 1, c2 != i))

# W and X cannot be mentioned in adjacent chapters
for i in range(1, 7):
    solver.add(Or(clue_vars['W'] != i, clue_vars['X'] != i + 1))
    solver.add(Or(clue_vars['W'] != i + 1, clue_vars['X'] != i))

# U and X must be mentioned in adjacent chapters
solver.add(Or(
    clue_vars['U'] == clue_vars['X'] - 1,
    clue_vars['U'] == clue_vars['X'] + 1,
    clue_vars['X'] == clue_vars['U'] - 1,
    clue_vars['X'] == clue_vars['U'] + 1
))

# Base constraints for the chapters (ordering)
for i in range(7):
    solver.add(chapters[i] == i + 1)

# Now, evaluate each option to see if it can replace the original constraint (T cannot be in chapter 1)
# We will check if the option alone can enforce the same ordering as the original constraint.

# Option A: U cannot be mentioned in chapter 2
opt_a_constr = (clue_vars['U'] != 2)

# Option B: W cannot be mentioned in chapter 4
opt_b_constr = (clue_vars['W'] != 4)

# Option C: X cannot be mentioned in chapter 6
opt_c_constr = (clue_vars['X'] != 6)

# Option D: U must be mentioned in an earlier chapter than T
opt_d_constr = (clue_vars['U'] < clue_vars['T'])

# Option E: X must be mentioned in an earlier chapter than W
opt_e_constr = (clue_vars['X'] < clue_vars['W'])

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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