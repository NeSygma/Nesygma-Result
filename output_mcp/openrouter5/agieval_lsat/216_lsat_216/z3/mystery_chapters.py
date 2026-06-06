from z3 import *

solver = Solver()

# Seven chapters (1-7), seven clues (R, S, T, U, W, X, Z)
# Each clue is assigned a chapter number (1-7)
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
chapter = {c: Int(f'chapter_{c}') for c in clues}

# Domain: each chapter is between 1 and 7
for c in clues:
    solver.add(chapter[c] >= 1, chapter[c] <= 7)

# All different: each clue gets a unique chapter
solver.add(Distinct([chapter[c] for c in clues]))

# Constraint 1: T cannot be mentioned in chapter 1
solver.add(chapter['T'] != 1)

# Constraint 2: T must be mentioned before W, and exactly two chapters separate them
# So W = T + 3 (since exactly two chapters between means difference of 3)
solver.add(chapter['W'] == chapter['T'] + 3)

# Constraint 3: S and Z cannot be adjacent
solver.add(Abs(chapter['S'] - chapter['Z']) != 1)

# Constraint 4: W and X cannot be adjacent
solver.add(Abs(chapter['W'] - chapter['X']) != 1)

# Constraint 5: U and X must be adjacent
solver.add(Abs(chapter['U'] - chapter['X']) == 1)

# Given: Z is mentioned in chapter 7
solver.add(chapter['Z'] == 7)

# Now evaluate each option
options = {
    "A": chapter['R'] == 3,
    "B": chapter['S'] == 3,
    "C": chapter['T'] == 4,
    "D": chapter['U'] == 1,
    "E": chapter['X'] == 5
}

found_options = []
for letter, constr in options.items():
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