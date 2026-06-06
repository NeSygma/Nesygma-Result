from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare symbolic variables for each space (1 through 7)
spaces = [Int(f'space_{i}') for i in range(1, 8)]

# Business types (encoded as integers for simplicity)
OPT = 0    # optometrist
PHAR = 1   # pharmacy
REST = 2   # restaurant
SHOE = 3   # shoe store
TOY = 4    # toy store
VET = 5    # veterinarian

# Base constraints
solver = Solver()

# Each space must be one of the business types
business_types = [OPT, PHAR, REST, SHOE, TOY, VET]
for s in spaces:
    solver.add(Or([s == b for b in business_types]))

# There are exactly two restaurants (two spaces must be REST)
solver.add(Sum([If(s == REST, 1, 0) for s in spaces]) == 2)

# Pharmacy must be at one end (space 1 or 7), and one restaurant at the other end
solver.add(Or(spaces[0] == PHAR, spaces[6] == PHAR))  # pharmacy at space 1 or 7
solver.add(Or(spaces[0] == REST, spaces[6] == REST))  # restaurant at the other end

# If pharmacy is at space 1, restaurant must be at space 7, and vice versa
solver.add(Implies(spaces[0] == PHAR, spaces[6] == REST))
solver.add(Implies(spaces[6] == PHAR, spaces[0] == REST))

# The two restaurants must be separated by at least two other businesses
# Enforce separation: at least two spaces between the two restaurants
# We will enforce this by ensuring the distance between the two restaurants is at least 3
# First, collect the indices of the restaurants
restaurant_indices = [i for i in range(7) if spaces[i] == REST]
# Ensure there are exactly two restaurants
solver.add(And(
    Sum([If(s == REST, 1, 0) for s in spaces]) == 2,
    restaurant_indices[0] < restaurant_indices[1],
    restaurant_indices[1] >= restaurant_indices[0] + 3
))

# Pharmacy must be next to either optometrist or veterinarian
pharmacy_pos = If(spaces[0] == PHAR, 0, 6)
solver.add(Or(
    And(pharmacy_pos == 0, spaces[1] == OPT),
    And(pharmacy_pos == 0, spaces[1] == VET),
    And(pharmacy_pos == 6, spaces[5] == OPT),
    And(pharmacy_pos == 6, spaces[5] == VET)
))

# Toy store cannot be next to veterinarian
for i in range(6):
    solver.add(Not(And(spaces[i] == TOY, spaces[i+1] == VET)))
    solver.add(Not(And(spaces[i] == VET, spaces[i+1] == TOY)))

# Shoe store is in space 4
solver.add(spaces[3] == SHOE)

# Evaluate each option
found_options = []

# Option A: The optometrist is next to a restaurant
opt_a_constr = Or([
    And(spaces[i] == OPT, Or([spaces[j] == REST for j in range(7) if abs(i - j) == 1]))
    for i in range(7)
])

# Option B: The pharmacy is next to the veterinarian
opt_b_constr = Or([
    And(spaces[i] == PHAR, spaces[j] == VET, abs(i - j) == 1)
    for i in range(7) for j in range(7)
])

# Option C: A restaurant is next to the toy store
opt_c_constr = Or([
    And(spaces[i] == REST, spaces[j] == TOY, abs(i - j) == 1)
    for i in range(7) for j in range(7)
])

# Option D: The shoe store is next to the toy store
opt_d_constr = Or([
    And(spaces[3] == SHOE, spaces[i] == TOY, abs(3 - i) == 1)
])

# Option E: The shoe store is next to the veterinarian
opt_e_constr = Or([
    And(spaces[3] == SHOE, spaces[i] == VET, abs(3 - i) == 1)
])

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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