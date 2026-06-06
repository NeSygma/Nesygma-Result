from z3 import *

# Define business constants
PHARMACY = 0
OPTOMETRIST = 1
RESTAURANT = 2
SHOE_STORE = 3
TOY_STORE = 4
VETERINARIAN = 5

# Helper function to check constraints for a given assignment of spaces

def check_constraints(spaces):
    solver = Solver()
    
    # Constraint 1: Pharmacy at one end, restaurant at the other end
    solver.add(Or(
        And(spaces[0] == PHARMACY, spaces[6] == RESTAURANT),
        And(spaces[0] == RESTAURANT, spaces[6] == PHARMACY)
    ))
    
    # Constraint 2: Two restaurants separated by at least two other businesses
    restaurant_indices = [i for i in range(7) if spaces[i] == RESTAURANT]
    solver.add(And(
        restaurant_indices[0] < restaurant_indices[1],
        restaurant_indices[1] - restaurant_indices[0] - 1 >= 2
    ))
    
    # Constraint 3: Pharmacy must be next to either optometrist or veterinarian
    if spaces[0] == PHARMACY:
        solver.add(Or(spaces[1] == OPTOMETRIST, spaces[1] == VETERINARIAN))
    if spaces[6] == PHARMACY:
        solver.add(Or(spaces[5] == OPTOMETRIST, spaces[5] == VETERINARIAN))
    
    # Constraint 4: Toy store cannot be next to veterinarian
    for i in range(6):
        solver.add(Not(And(spaces[i] == TOY_STORE, spaces[i+1] == VETERINARIAN)))
        solver.add(Not(And(spaces[i] == VETERINARIAN, spaces[i+1] == TOY_STORE)))
    
    return solver.check()

# Define the options as lists of business constants
options = {
    "A": [PHARMACY, OPTOMETRIST, SHOE_STORE, RESTAURANT, VETERINARIAN, TOY_STORE, RESTAURANT],
    "B": [PHARMACY, VETERINARIAN, OPTOMETRIST, SHOE_STORE, RESTAURANT, TOY_STORE, RESTAURANT],
    "C": [RESTAURANT, SHOE_STORE, VETERINARIAN, PHARMACY, OPTOMETRIST, TOY_STORE, RESTAURANT],
    "D": [RESTAURANT, TOY_STORE, OPTOMETRIST, RESTAURANT, VETERINARIAN, SHOE_STORE, PHARMACY],
    "E": [RESTAURANT, OPTOMETRIST, TOY_STORE, RESTAURANT, SHOE_STORE, VETERINARIAN, PHARMACY]
}

# Evaluate each option
found_options = []
for letter, assignment in options.items():
    solver = Solver()
    spaces = [Int(f"space_{i}") for i in range(7)]
    
    # Assign the option's businesses to spaces
    for i in range(7):
        solver.add(spaces[i] == assignment[i])
    
    # Check constraints
    if solver.check() == sat:
        found_options.append(letter)

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")