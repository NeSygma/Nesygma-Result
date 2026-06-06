from z3 import *

solver = Solver()

# Define the businesses
# 0=pharmacy, 1=optometrist, 2=restaurant1, 3=restaurant2, 4=shoe_store, 5=toy_store, 6=veterinarian
businesses = [Int(f'space_{i}') for i in range(7)]

# Each space has a business (0-6)
for b in businesses:
    solver.add(b >= 0, b <= 6)

# All different
solver.add(Distinct(businesses))

# Define helper: is_pharmacy, is_optometrist, etc.
def is_pharmacy(x): return x == 0
def is_optometrist(x): return x == 1
def is_restaurant(x): return Or(x == 2, x == 3)
def is_shoe_store(x): return x == 4
def is_toy_store(x): return x == 5
def is_veterinarian(x): return x == 6

# Constraint 1: Pharmacy at one end, one restaurant at the other
# Pharmacy at space 1 (index 0) or space 7 (index 6)
solver.add(Or(is_pharmacy(businesses[0]), is_pharmacy(businesses[6])))
# One restaurant at the other end
solver.add(Or(
    And(is_pharmacy(businesses[0]), is_restaurant(businesses[6])),
    And(is_pharmacy(businesses[6]), is_restaurant(businesses[0]))
))

# Constraint 2: Two restaurants must be separated by at least two other businesses
# Find positions of the two restaurants
rest_positions = [Int(f'rest_pos_{i}') for i in range(2)]
# Map each restaurant to its position
for r_idx in range(2):
    # restaurant r_idx is business value (2 or 3)
    for pos in range(7):
        solver.add(Implies(businesses[pos] == r_idx + 2, rest_positions[r_idx] == pos))

# The two restaurants must be at least 3 apart (separated by at least 2 others)
solver.add(Abs(rest_positions[0] - rest_positions[1]) >= 3)

# Constraint 3: Pharmacy must be next to either optometrist or veterinarian
# Find pharmacy position
pharmacy_pos = Int('pharmacy_pos')
for pos in range(7):
    solver.add(Implies(is_pharmacy(businesses[pos]), pharmacy_pos == pos))

# Pharmacy must be adjacent to optometrist or veterinarian
adjacent_to_pharmacy = []
for pos in range(7):
    # Check if this position is adjacent to pharmacy
    for other in range(7):
        if abs(pos - other) == 1:
            adjacent_to_pharmacy.append(And(
                pharmacy_pos == pos,
                Or(is_optometrist(businesses[other]), is_veterinarian(businesses[other]))
            ))
solver.add(Or(adjacent_to_pharmacy))

# Constraint 4: Toy store cannot be next to veterinarian
for pos in range(7):
    for other in range(7):
        if abs(pos - other) == 1:
            solver.add(Not(And(is_toy_store(businesses[pos]), is_veterinarian(businesses[other]))))

# Now test each option
def option_constraint(opt_list):
    """opt_list is a list of 7 strings representing the businesses in order"""
    constraints = []
    mapping = {
        'pharmacy': 0,
        'optometrist': 1,
        'restaurant': 2,  # We'll handle two restaurants specially
        'shoe store': 4,
        'toy store': 5,
        'veterinarian': 6
    }
    
    # Track which restaurant (2 or 3) we've assigned
    restaurant_count = 0
    for i, name in enumerate(opt_list):
        if name == 'restaurant':
            if restaurant_count == 0:
                constraints.append(businesses[i] == 2)
                restaurant_count += 1
            else:
                constraints.append(businesses[i] == 3)
        else:
            constraints.append(businesses[i] == mapping[name])
    
    return And(constraints)

options = {
    "A": ["pharmacy", "optometrist", "shoe store", "restaurant", "veterinarian", "toy store", "restaurant"],
    "B": ["pharmacy", "veterinarian", "optometrist", "shoe store", "restaurant", "toy store", "restaurant"],
    "C": ["restaurant", "shoe store", "veterinarian", "pharmacy", "optometrist", "toy store", "restaurant"],
    "D": ["restaurant", "toy store", "optometrist", "restaurant", "veterinarian", "shoe store", "pharmacy"],
    "E": ["restaurant", "optometrist", "toy store", "restaurant", "shoe store", "veterinarian", "pharmacy"]
}

found_options = []
for letter, opt_list in options.items():
    solver.push()
    solver.add(option_constraint(opt_list))
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