from z3 import *

# Create solver
solver = Solver()

# Define spaces 1-7 (indices 0-6 for Python)
spaces = [Int(f'space_{i}') for i in range(7)]

# Business types: 0=pharmacy, 1=optometrist, 2=restaurant, 3=shoe store, 4=toy store, 5=veterinarian, 6=restaurant (second)
# Actually, we have two restaurants, so we need to distinguish them. Let's use:
# 0=pharmacy, 1=optometrist, 2=restaurant1, 3=shoe store, 4=toy store, 5=veterinarian, 6=restaurant2

# Each space must contain exactly one business, and each business exactly once
# We'll use a permutation constraint: all spaces have distinct values from 0-6
solver.add(Distinct(spaces))
for i in range(7):
    solver.add(spaces[i] >= 0, spaces[i] <= 6)

# Helper function to get business name from value
def business_name(val):
    names = ["pharmacy", "optometrist", "restaurant1", "shoe store", "toy store", "veterinarian", "restaurant2"]
    return names[val]

# Base constraints from problem statement:

# 1. The pharmacy must be at one end of the row and one of the restaurants at the other.
# Pharmacy (0) at space 0 OR space 6
solver.add(Or(spaces[0] == 0, spaces[6] == 0))
# One restaurant (2 or 6) at the opposite end
solver.add(Or(
    And(spaces[0] == 0, Or(spaces[6] == 2, spaces[6] == 6)),  # pharmacy at 0, restaurant at 6
    And(spaces[6] == 0, Or(spaces[0] == 2, spaces[0] == 6))   # pharmacy at 6, restaurant at 0
))

# 2. The two restaurants must be separated by at least two other businesses.
# If restaurant1 at position i, restaurant2 at position j, then |i - j| >= 3
# We need to find positions of restaurant1 (2) and restaurant2 (6)
r1_pos = Int('r1_pos')
r2_pos = Int('r2_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 2, r1_pos == i))
    solver.add(Implies(spaces[i] == 6, r2_pos == i))
solver.add(Abs(r1_pos - r2_pos) >= 3)

# 3. The pharmacy must be next to either the optometrist or the veterinarian.
# Pharmacy (0) adjacent to optometrist (1) or veterinarian (5)
pharm_pos = Int('pharm_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 0, pharm_pos == i))
# Adjacent means |pos - other_pos| == 1
opt_pos = Int('opt_pos')
vet_pos = Int('vet_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 1, opt_pos == i))
    solver.add(Implies(spaces[i] == 5, vet_pos == i))
solver.add(Or(Abs(pharm_pos - opt_pos) == 1, Abs(pharm_pos - vet_pos) == 1))

# 4. The toy store cannot be next to the veterinarian.
# Toy store (4) and veterinarian (5) cannot be adjacent
toy_pos = Int('toy_pos')
for i in range(7):
    solver.add(Implies(spaces[i] == 4, toy_pos == i))
solver.add(Abs(toy_pos - vet_pos) != 1)

# Now evaluate each answer choice
found_options = []

# Answer A: pharmacy, optometrist, shoe store, restaurant, veterinarian, toy store, restaurant
# This means: space0=pharmacy(0), space1=optometrist(1), space2=shoe store(3), 
# space3=restaurant(2 or 6), space4=veterinarian(5), space5=toy store(4), space6=restaurant(2 or 6)
# We need to assign the two restaurants (2 and 6) to spaces 3 and 6
opt_a_constr = And(
    spaces[0] == 0,  # pharmacy
    spaces[1] == 1,  # optometrist
    spaces[2] == 3,  # shoe store
    spaces[4] == 5,  # veterinarian
    spaces[5] == 4,  # toy store
    # restaurants at spaces 3 and 6 (one is 2, other is 6)
    Or(And(spaces[3] == 2, spaces[6] == 6), And(spaces[3] == 6, spaces[6] == 2))
)

# Answer B: pharmacy, veterinarian, optometrist, shoe store, restaurant, toy store, restaurant
opt_b_constr = And(
    spaces[0] == 0,  # pharmacy
    spaces[1] == 5,  # veterinarian
    spaces[2] == 1,  # optometrist
    spaces[3] == 3,  # shoe store
    spaces[5] == 4,  # toy store
    # restaurants at spaces 4 and 6
    Or(And(spaces[4] == 2, spaces[6] == 6), And(spaces[4] == 6, spaces[6] == 2))
)

# Answer C: restaurant, shoe store, veterinarian, pharmacy, optometrist, toy store, restaurant
opt_c_constr = And(
    spaces[3] == 0,  # pharmacy at space 4 (index 3)
    spaces[0] == 2 or spaces[0] == 6,  # restaurant at space 1
    spaces[1] == 3,  # shoe store
    spaces[2] == 5,  # veterinarian
    spaces[4] == 1,  # optometrist
    spaces[5] == 4,  # toy store
    spaces[6] == 2 or spaces[6] == 6  # restaurant at space 7
)

# Answer D: restaurant, toy store, optometrist, restaurant, veterinarian, shoe store, pharmacy
opt_d_constr = And(
    spaces[6] == 0,  # pharmacy at space 7
    spaces[0] == 2 or spaces[0] == 6,  # restaurant at space 1
    spaces[1] == 4,  # toy store
    spaces[2] == 1,  # optometrist
    spaces[3] == 2 or spaces[3] == 6,  # restaurant at space 4
    spaces[4] == 5,  # veterinarian
    spaces[5] == 3   # shoe store
)

# Answer E: restaurant, optometrist, toy store, restaurant, shoe store, veterinarian, pharmacy
opt_e_constr = And(
    spaces[6] == 0,  # pharmacy at space 7
    spaces[0] == 2 or spaces[0] == 6,  # restaurant at space 1
    spaces[1] == 1,  # optometrist
    spaces[2] == 4,  # toy store
    spaces[3] == 2 or spaces[3] == 6,  # restaurant at space 4
    spaces[4] == 3,  # shoe store
    spaces[5] == 5   # veterinarian
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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