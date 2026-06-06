from z3 import *

# Define business types as integers
PHARMACY = 0
OPTOMETRIST = 1
RESTAURANT = 2
SHOE_STORE = 3
TOY_STORE = 4
VETERINARIAN = 5

# Map option letters to their space assignments (spaces 1-7)
options = {
    "A": [PHARMACY, OPTOMETRIST, SHOE_STORE, RESTAURANT, VETERINARIAN, TOY_STORE, RESTAURANT],
    "B": [PHARMACY, VETERINARIAN, OPTOMETRIST, SHOE_STORE, RESTAURANT, TOY_STORE, RESTAURANT],
    "C": [RESTAURANT, SHOE_STORE, VETERINARIAN, PHARMACY, OPTOMETRIST, TOY_STORE, RESTAURANT],
    "D": [RESTAURANT, TOY_STORE, OPTOMETRIST, RESTAURANT, VETERINARIAN, SHOE_STORE, PHARMACY],
    "E": [RESTAURANT, OPTOMETRIST, TOY_STORE, RESTAURANT, SHOE_STORE, VETERINARIAN, PHARMACY],
}

solver = Solver()

# Create space variables
spaces = [Int(f'space_{i}') for i in range(7)]

# Each space gets one of 6 business types (0-5)
for i in range(7):
    solver.add(spaces[i] >= 0, spaces[i] <= 5)

# Exactly one pharmacy, one optometrist, two restaurants, one shoe store, one toy store, one vet
solver.add(Sum([If(spaces[i] == PHARMACY, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(spaces[i] == OPTOMETRIST, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(spaces[i] == RESTAURANT, 1, 0) for i in range(7)]) == 2)
solver.add(Sum([If(spaces[i] == SHOE_STORE, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(spaces[i] == TOY_STORE, 1, 0) for i in range(7)]) == 1)
solver.add(Sum([If(spaces[i] == VETERINARIAN, 1, 0) for i in range(7)]) == 1)

# Constraint 1: Pharmacy at one end, restaurant at the other
solver.add(Or(
    And(spaces[0] == PHARMACY, spaces[6] == RESTAURANT),
    And(spaces[0] == RESTAURANT, spaces[6] == PHARMACY)
))

# Constraint 2: Two restaurants separated by at least 2 others (distance >= 3)
for i in range(7):
    for j in range(i+1, 7):
        solver.add(Implies(And(spaces[i] == RESTAURANT, spaces[j] == RESTAURANT), j - i >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian
# For each space, if it's pharmacy, at least one neighbor must be opt or vet
for i in range(7):
    neighbor_conditions = []
    if i > 0:
        neighbor_conditions.append(Or(spaces[i-1] == OPTOMETRIST, spaces[i-1] == VETERINARIAN))
    if i < 6:
        neighbor_conditions.append(Or(spaces[i+1] == OPTOMETRIST, spaces[i+1] == VETERINARIAN))
    solver.add(Implies(spaces[i] == PHARMACY, Or(neighbor_conditions)))

# Constraint 4: Toy store not next to veterinarian
for i in range(7):
    for j in range(i+1, 7):
        if j - i == 1:
            solver.add(Not(And(spaces[i] == TOY_STORE, spaces[j] == VETERINARIAN)))
            solver.add(Not(And(spaces[i] == VETERINARIAN, spaces[j] == TOY_STORE)))

# Now check each option
found_options = []
for letter, assignment in options.items():
    solver.push()
    for i in range(7):
        solver.add(spaces[i] == assignment[i])
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