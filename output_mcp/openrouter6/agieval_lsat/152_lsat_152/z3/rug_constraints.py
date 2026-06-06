from z3 import *

# Color indices
forest = 0
olive = 1
peach = 2
turquoise = 3
white = 4
yellow = 5
colors = [forest, olive, peach, turquoise, white, yellow]
color_names = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Variables
used = [Bool(f"used_{i}") for i in colors]
solid = [Bool(f"solid_{i}") for i in colors]

solver = Solver()

# Base constraints
# Exactly two solids
solver.add(Sum([If(solid[i], 1, 0) for i in colors]) == 2)
# Exactly five used
solver.add(Sum([If(used[i], 1, 0) for i in colors]) == 5)
# If solid then used
for i in colors:
    solver.add(Implies(solid[i], used[i]))
# White cannot be solid
solver.add(Not(solid[white]))
# Olive cannot be solid
solver.add(Not(solid[olive]))
# If olive is used, then peach is used and not solid
solver.add(Implies(used[olive], And(used[peach], Not(solid[peach]))))
# Forest and turquoise not together in multicolored rug
solver.add(Not(And(used[forest], Not(solid[forest]), used[turquoise], Not(solid[turquoise]))))
# Peach and turquoise not together
solver.add(Not(And(used[peach], Not(solid[peach]), used[turquoise], Not(solid[turquoise]))))
# Peach and yellow not together
solver.add(Not(And(used[peach], Not(solid[peach]), used[yellow], Not(solid[yellow]))))

# Option constraints
options = [
    ("A", [(forest, True), (peach, True)]),  # forest and peach solid
    ("B", [(forest, True), (yellow, True)]), # forest and yellow solid
    ("C", [(peach, True), (turquoise, True)]), # peach and turquoise solid
    ("D", [(peach, True), (yellow, True)]),   # peach and yellow solid
    ("E", [(turquoise, True), (yellow, True)]), # turquoise and yellow solid
]

found_unsat = []
for letter, solid_pairs in options:
    solver.push()
    # Add solid constraints for the pair
    for color_idx, val in solid_pairs:
        solver.add(solid[color_idx] == val)
        solver.add(used[color_idx] == True)  # solid implies used
    # For the other colors, we don't explicitly set solid to false, but the exactly two solids constraint will enforce that.
    # Check satisfiability
    result = solver.check()
    if result == unsat:
        found_unsat.append(letter)
    solver.pop()

if len(found_unsat) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat[0]}")
elif len(found_unsat) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found unsat: {found_unsat}")
else:
    print("STATUS: unsat")
    print("Refine: No options found unsat")