from z3 import *

solver = Solver()

# Compositions
comps = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in comps}

for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct([pos[c] for c in comps]))

# Constraints
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))
solver.add(Or(pos['O'] == 1, pos['O'] == 5))
solver.add(Or(pos['L'] == 8, pos['H'] == 8))
solver.add(pos['P'] < pos['S'])
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Question constraints
solver.add(pos['P'] == 3)
solver.add(pos['S'] == 6)

# Define options
# (A) F or H
# (B) F or O
# (C) F or T
# (D) H or L
# (E) O or R

def check_option(c1, c2):
    # The composition at 5 MUST be c1 or c2.
    # This means:
    # 1. It is possible for pos[5] to be c1 or c2.
    # 2. It is NOT possible for pos[5] to be anything else.
    
    # Let's check if there exists a valid model where pos[5] is NOT c1 AND pos[5] is NOT c2.
    solver.push()
    solver.add(pos['F'] != 5, pos['H'] != 5, pos['L'] != 5, pos['O'] != 5, pos['P'] != 5, pos['R'] != 5, pos['S'] != 5, pos['T'] != 5)
    # Wait, this is wrong. pos[5] must be one of the compositions.
    # Let's say pos[X] = 5. We want to check if X is in {c1, c2}.
    
    # Correct logic:
    # For all valid models, pos[5] must be c1 or c2.
    # This is equivalent to: There is NO valid model where pos[5] is NOT c1 AND pos[5] is NOT c2.
    
    solver.push()
    # Find a model where pos[5] is not c1 and pos[5] is not c2
    # pos[5] is not c1 means pos[c1] != 5
    # pos[5] is not c2 means pos[c2] != 5
    # Actually, we need to find a model where the composition at 5 is some X, and X is not c1 and X is not c2.
    
    # Let X be the composition at 5.
    X = Int('X')
    solver.add(Or([pos[c] == 5 for c in comps]))
    solver.add(Or([And(pos[c] == 5, c != c1, c != c2) for c in comps]))
    
    res = solver.check()
    solver.pop()
    return res == unsat

# Check each option
options = [
    ("A", "F", "H"),
    ("B", "F", "O"),
    ("C", "F", "T"),
    ("D", "H", "L"),
    ("E", "O", "R")
]

found_options = []
for letter, c1, c2 in options:
    if check_option(c1, c2):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")