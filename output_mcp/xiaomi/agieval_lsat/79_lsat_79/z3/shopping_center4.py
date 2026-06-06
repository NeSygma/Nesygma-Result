from z3 import *

solver = Solver()

# Define business types
# 0=Optometrist, 1=Pharmacy, 2=Restaurant1, 3=Restaurant2, 4=Shoe, 5=Toy, 6=Vet
businesses = [Int(f'biz_{i}') for i in range(7)]  # biz_i is business in space i+1

# Each space gets exactly one business (0-6)
for i in range(7):
    solver.add(businesses[i] >= 0, businesses[i] <= 6)

# All businesses are distinct
solver.add(Distinct(businesses))

# Constraint 1: Pharmacy at one end, one restaurant at the other
# Pharmacy is 1, restaurants are 2 and 3
solver.add(Or(
    And(businesses[0] == 1, Or(businesses[6] == 2, businesses[6] == 3)),
    And(businesses[6] == 1, Or(businesses[0] == 2, businesses[0] == 3))
))

# Constraint 2: Two restaurants separated by at least 2 other businesses
# Find positions of restaurants (2 and 3)
rest_positions = [Int(f'rest_pos_{i}') for i in range(2)]
for i in range(2):
    # rest_positions[i] is the space index (0-6) where restaurant i+2 is
    solver.add(rest_positions[i] >= 0, rest_positions[i] <= 6)
    # Link to actual positions
    solver.add(Or([And(rest_positions[i] == j, businesses[j] == i+2) for j in range(7)]))

# Restaurants must be distinct
solver.add(rest_positions[0] != rest_positions[1])
# At least 2 apart: |pos1 - pos2| >= 3
solver.add(Or(rest_positions[0] - rest_positions[1] >= 3, rest_positions[1] - rest_positions[0] >= 3))

# Constraint 3: Pharmacy next to either optometrist or veterinarian
# Pharmacy is 1, optometrist is 0, vet is 6
# We need to find pharmacy position without symbolic indexing
pharmacy_pos = Int('pharmacy_pos')
solver.add(pharmacy_pos >= 0, pharmacy_pos <= 6)
solver.add(Or([And(pharmacy_pos == i, businesses[i] == 1) for i in range(7)]))

# Pharmacy must be adjacent to optometrist or vet
# Use Or-loop pattern for adjacency
adjacent_to_pharmacy = []
for i in range(7):
    # If pharmacy is at position i, check neighbors
    if i > 0:
        adjacent_to_pharmacy.append(And(pharmacy_pos == i, Or(businesses[i-1] == 0, businesses[i-1] == 6)))
    if i < 6:
        adjacent_to_pharmacy.append(And(pharmacy_pos == i, Or(businesses[i+1] == 0, businesses[i+1] == 6)))
solver.add(Or(adjacent_to_pharmacy))

# Constraint 4: Toy store not next to veterinarian
# Toy is 5, vet is 6
for i in range(7):
    # If space i is toy, neighbors can't be vet
    if i > 0:
        solver.add(Implies(businesses[i] == 5, businesses[i-1] != 6))
    if i < 6:
        solver.add(Implies(businesses[i] == 5, businesses[i+1] != 6))
    # If space i is vet, neighbors can't be toy
    if i > 0:
        solver.add(Implies(businesses[i] == 6, businesses[i-1] != 5))
    if i < 6:
        solver.add(Implies(businesses[i] == 6, businesses[i+1] != 5))

# Additional condition: Optometrist next to shoe store
# Optometrist is 0, shoe is 4
solver.add(Or(
    And(businesses[0] == 0, businesses[1] == 4),
    And(businesses[0] == 4, businesses[1] == 0),
    And(businesses[1] == 0, businesses[2] == 4),
    And(businesses[1] == 4, businesses[2] == 0),
    And(businesses[2] == 0, businesses[3] == 4),
    And(businesses[2] == 4, businesses[3] == 0),
    And(businesses[3] == 0, businesses[4] == 4),
    And(businesses[3] == 4, businesses[4] == 0),
    And(businesses[4] == 0, businesses[5] == 4),
    And(businesses[4] == 4, businesses[5] == 0),
    And(businesses[5] == 0, businesses[6] == 4),
    And(businesses[5] == 4, businesses[6] == 0)
))

# Now we need to find what must be on either side of the O-S pair
# First, let's find all valid arrangements
# Then check each answer choice

# We'll test each answer choice
# A: pharmacy and a restaurant
# B: pharmacy and the toy store  
# C: the two restaurants
# D: a restaurant and the toy store
# E: a restaurant and the veterinarian

# We need to check: for ALL valid arrangements, what's on either side of O-S pair?
# This is a "must be" question, so we need to check if the answer is necessarily true.

# Approach: For each answer choice, check if it's possible to have a valid arrangement
# where the O-S pair does NOT have that answer on either side.
# If it's impossible (unsat), then that answer must be true.

# Let's define helper: O-S pair is at positions (p, p+1)
# Left neighbor is at p-1 (if exists), right neighbor is at p+2 (if exists)

# We'll check each answer choice by trying to find a counterexample
# where the answer is NOT satisfied

def check_answer_choice(choice_name, choice_constraint):
    """Check if choice_constraint must be true for all valid arrangements."""
    s = Solver()
    # Add all base constraints
    s.add(solver.assertions())
    
    # Add negation of the choice constraint
    s.add(Not(choice_constraint))
    
    result = s.check()
    return result == unsat  # If unsat, then choice must be true

# Define the answer choices more precisely
# We need to find the O-S pair position first
os_pair_left = Int('os_pair_left')  # left position of O-S pair (0-5)
os_pair_right = Int('os_pair_right')  # right position (os_pair_left + 1)

# Link to actual positions
solver.add(os_pair_right == os_pair_left + 1)
solver.add(os_pair_left >= 0, os_pair_left <= 5)

# O-S pair constraint using Or-loop pattern
os_pair_constraints = []
for i in range(6):  # i from 0 to 5
    os_pair_constraints.append(And(os_pair_left == i, 
                                   Or(And(businesses[i] == 0, businesses[i+1] == 4),
                                      And(businesses[i] == 4, businesses[i+1] == 0))))
solver.add(Or(os_pair_constraints))

# Now define what's on either side
# We need to check if the pair is not at the ends
has_left = os_pair_left > 0
has_right = os_pair_right < 6

# Define neighbor values using Or-loop pattern
# Left neighbor is at os_pair_left - 1
left_neighbor = Int('left_neighbor')
left_neighbor_constraints = []
for i in range(1, 7):  # i from 1 to 6
    left_neighbor_constraints.append(And(os_pair_left == i, left_neighbor == businesses[i-1]))
solver.add(Implies(has_left, Or(left_neighbor_constraints)))

# Right neighbor is at os_pair_right + 1
right_neighbor = Int('right_neighbor')
right_neighbor_constraints = []
for i in range(0, 6):  # i from 0 to 5
    right_neighbor_constraints.append(And(os_pair_left == i, right_neighbor == businesses[i+2]))
solver.add(Implies(has_right, Or(right_neighbor_constraints)))

# Now check each answer choice
# We need to check if the pair has both neighbors (not at ends)
# If at an end, the question might not apply, but let's assume it's not at an end

# Define answer constraints
# A: pharmacy (1) and a restaurant (2 or 3)
opt_a = And(has_left, has_right, Or(
    And(left_neighbor == 1, Or(right_neighbor == 2, right_neighbor == 3)),
    And(right_neighbor == 1, Or(left_neighbor == 2, left_neighbor == 3))
))

# B: pharmacy (1) and toy store (5)
opt_b = And(has_left, has_right, Or(
    And(left_neighbor == 1, right_neighbor == 5),
    And(right_neighbor == 1, left_neighbor == 5)
))

# C: two restaurants (2 and 3)
opt_c = And(has_left, has_right, Or(
    And(left_neighbor == 2, right_neighbor == 3),
    And(left_neighbor == 3, right_neighbor == 2)
))

# D: a restaurant (2 or 3) and toy store (5)
opt_d = And(has_left, has_right, Or(
    And(Or(left_neighbor == 2, left_neighbor == 3), right_neighbor == 5),
    And(Or(right_neighbor == 2, right_neighbor == 3), left_neighbor == 5)
))

# E: a restaurant (2 or 3) and veterinarian (6)
opt_e = And(has_left, has_right, Or(
    And(Or(left_neighbor == 2, left_neighbor == 3), right_neighbor == 6),
    And(Or(right_neighbor == 2, right_neighbor == 3), left_neighbor == 6)
))

# Check each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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