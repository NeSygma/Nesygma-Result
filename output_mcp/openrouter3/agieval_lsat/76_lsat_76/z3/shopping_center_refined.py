from z3 import *

# Create solver
solver = Solver()

# Define spaces 1-7 (indices 0-6 for Python)
# Each space contains a business type: 0=pharmacy, 1=optometrist, 2=restaurant, 3=shoe store, 4=toy store, 5=veterinarian
# We have two restaurants, so we'll use the same type (2) for both
spaces = [Int(f'space_{i}') for i in range(7)]

# Each space must contain exactly one business from 0-5
# But we have 7 spaces and 6 business types (with 2 restaurants), so we need to handle duplicates
# Actually, we have: pharmacy, optometrist, 2 restaurants, shoe store, toy store, veterinarian = 7 businesses
# So we need 7 distinct business identifiers. Let's use:
# 0=pharmacy, 1=optometrist, 2=restaurant1, 3=shoe store, 4=toy store, 5=veterinarian, 6=restaurant2

# All spaces must have distinct values from 0-6
solver.add(Distinct(spaces))
for i in range(7):
    solver.add(spaces[i] >= 0, spaces[i] <= 6)

# Helper function to check if a space contains a restaurant (either type 2 or 6)
def is_restaurant(space_val):
    return Or(space_val == 2, space_val == 6)

# Constraint 1: Pharmacy at one end, restaurant at the other
# Pharmacy (0) at space 0 OR space 6
pharm_at_start = (spaces[0] == 0)
pharm_at_end = (spaces[6] == 0)
restaurant_at_start = is_restaurant(spaces[0])
restaurant_at_end = is_restaurant(spaces[6])

solver.add(Or(
    And(pharm_at_start, restaurant_at_end),  # pharmacy at start, restaurant at end
    And(pharm_at_end, restaurant_at_start)   # pharmacy at end, restaurant at start
))

# Constraint 2: Two restaurants separated by at least two other businesses
# Find positions of the two restaurants
r1_pos = Int('r1_pos')
r2_pos = Int('r2_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 2, r1_pos == i))
    solver.add(Implies(spaces[i] == 6, r2_pos == i))
# Distance between them must be at least 3 (positions differ by at least 3)
solver.add(Abs(r1_pos - r2_pos) >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
pharm_pos = Int('pharm_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 0, pharm_pos == i))

opt_pos = Int('opt_pos')
vet_pos = Int('vet_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 1, opt_pos == i))
    solver.add(Implies(spaces[i] == 5, vet_pos == i))

solver.add(Or(
    Abs(pharm_pos - opt_pos) == 1,
    Abs(pharm_pos - vet_pos) == 1
))

# Constraint 4: Toy store (4) cannot be next to veterinarian (5)
toy_pos = Int('toy_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 4, toy_pos == i))
solver.add(Abs(toy_pos - vet_pos) != 1)

# Now test each answer choice
# For each choice, we need to map the given sequence to our business types
# A: pharmacy, optometrist, shoe store, restaurant, veterinarian, toy store, restaurant
# B: pharmacy, veterinarian, optometrist, shoe store, restaurant, toy store, restaurant
# C: restaurant, shoe store, veterinarian, pharmacy, optometrist, toy store, restaurant
# D: restaurant, toy store, optometrist, restaurant, veterinarian, shoe store, pharmacy
# E: restaurant, optometrist, toy store, restaurant, shoe store, veterinarian, pharmacy

def make_choice_constraint(seq):
    """Convert a sequence of business names to Z3 constraints"""
    # Map business names to our types
    mapping = {
        "pharmacy": 0,
        "optometrist": 1,
        "restaurant": 2,  # We'll handle restaurants specially
        "shoe store": 3,
        "toy store": 4,
        "veterinarian": 5
    }
    
    constraints = []
    restaurant_positions = []
    
    for i, business in enumerate(seq):
        if business == "restaurant":
            # We'll assign restaurant types later
            restaurant_positions.append(i)
        else:
            constraints.append(spaces[i] == mapping[business])
    
    # For restaurants, we need to assign types 2 and 6 to the two positions
    if len(restaurant_positions) == 2:
        pos1, pos2 = restaurant_positions
        # One restaurant is type 2, the other is type 6
        constraints.append(Or(
            And(spaces[pos1] == 2, spaces[pos2] == 6),
            And(spaces[pos1] == 6, spaces[pos2] == 2)
        ))
    
    return And(constraints)

# Define each answer choice sequence
seq_a = ["pharmacy", "optometrist", "shoe store", "restaurant", "veterinarian", "toy store", "restaurant"]
seq_b = ["pharmacy", "veterinarian", "optometrist", "shoe store", "restaurant", "toy store", "restaurant"]
seq_c = ["restaurant", "shoe store", "veterinarian", "pharmacy", "optometrist", "toy store", "restaurant"]
seq_d = ["restaurant", "toy store", "optometrist", "restaurant", "veterinarian", "shoe store", "pharmacy"]
seq_e = ["restaurant", "optometrist", "toy store", "restaurant", "shoe store", "veterinarian", "pharmacy"]

# Test each option
found_options = []
for letter, seq in [("A", seq_a), ("B", seq_b), ("C", seq_c), ("D", seq_d), ("E", seq_e)]:
    solver.push()
    solver.add(make_choice_constraint(seq))
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")