from z3 import *

# Define business type codes
OPT = 0
PHARM = 1
REST = 2
SHOE = 3
TOY = 4
VET = 5

# Create solver
solver = Solver()

# Declare position variables
pos = [Int(f'pos_{i}') for i in range(7)]

# Add base constraints

# 1. Exactly one of each type except restaurants (two)
# Count constraints
solver.add(Sum([If(pos[i] == OPT, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == PHARM, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == REST, 1, 0) for i in range(7)]) == 2)
solver.add(Sum([If(pos[i] == SHOE, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == TOY, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(pos[i] == VET, 1, 0) for i in range(7)]) == 1)

# 2. Pharmacy at one end and restaurant at the other
solver.add(Or(pos[0] == PHARM, pos[0] == REST))
solver.add(Or(pos[6] == PHARM, pos[6] == REST))
solver.add((pos[0] == PHARM) == (pos[6] == REST))
solver.add((pos[0] == REST) == (pos[6] == PHARM))

# 3. Two restaurants separated by at least two other businesses
for i in range(7):
    for j in range(i+1, 7):
        solver.add(Implies(And(pos[i] == REST, pos[j] == REST), j - i >= 3))

# 4. Pharmacy next to optometrist or veterinarian
for i in range(7):
    neighbor_left = And(i > 0, Or(pos[i-1] == OPT, pos[i-1] == VET))
    neighbor_right = And(i < 6, Or(pos[i+1] == OPT, pos[i+1] == VET))
    solver.add(Implies(pos[i] == PHARM, Or(neighbor_left, neighbor_right)))

# 5. Toy store cannot be next to veterinarian
for i in range(7):
    if i > 0:
        solver.add(Implies(pos[i] == TOY, pos[i-1] != VET))
    if i < 6:
        solver.add(Implies(pos[i] == TOY, pos[i+1] != VET))

# Define the options
options = [
    ("A", [PHARM, OPT, SHOE, REST, VET, TOY, REST]),
    ("B", [PHARM, VET, OPT, SHOE, REST, TOY, REST]),
    ("C", [REST, SHOE, VET, PHARM, OPT, TOY, REST]),
    ("D", [REST, TOY, OPT, REST, VET, SHOE, PHARM]),
    ("E", [REST, OPT, TOY, REST, SHOE, VET, PHARM])
]

found_options = []
for letter, ordering in options:
    solver.push()
    # Add ordering constraints
    for i in range(7):
        solver.add(pos[i] == ordering[i])
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