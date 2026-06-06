from z3 import *

# BENCHMARK_MODE: ON (as per instructions)
BENCHMARK_MODE = True

# Create a solver
solver = Solver()

# Define business types as integers for easier handling
OPT = 0  # Optometrist
PHAR = 1  # Pharmacy
REST = 2  # Restaurant
SHOE = 3  # Shoe Store
TOY = 4   # Toy Store
VET = 5   # Veterinarian

# Create a list of variables for each space (1-7)
spaces = [Int(f'space_{i}') for i in range(1, 8)]

# Each space must be assigned exactly one business
for i in range(1, 8):
    solver.add(Or([spaces[i-1] == b for b in [OPT, PHAR, REST, SHOE, TOY, VET]]))

# Constraint 1: Pharmacy (PHAR) must be at one end (space 1 or 7), and a restaurant (REST) must be at the other end.
solver.add(Or(spaces[0] == PHAR, spaces[0] == REST))
solver.add(Or(spaces[6] == PHAR, spaces[6] == REST))
solver.add(Or(And(spaces[0] == PHAR, spaces[6] == REST), And(spaces[0] == REST, spaces[6] == PHAR)))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# First, ensure there are exactly two restaurants.
restaurant_positions = [i for i in range(7) if spaces[i] == REST]
solver.add(Sum([If(spaces[i] == REST, 1, 0) for i in range(7)]) == 2)

# Ensure the two restaurants are separated by at least two businesses.
solver.add(Or(
    restaurant_positions[1] - restaurant_positions[0] >= 3,
    restaurant_positions[0] - restaurant_positions[1] >= 3
))

# Constraint 3: Pharmacy (PHAR) must be next to either the optometrist (OPT) or the veterinarian (VET).
pharmacy_pos = [i for i in range(7) if spaces[i] == PHAR]
solver.add(Or(
    And(pharmacy_pos[0] > 0, Or(spaces[pharmacy_pos[0]-1] == OPT, spaces[pharmacy_pos[0]-1] == VET)),
    And(pharmacy_pos[0] < 6, Or(spaces[pharmacy_pos[0]+1] == OPT, spaces[pharmacy_pos[0]+1] == VET))
))

# Constraint 4: Toy store (TOY) cannot be next to the veterinarian (VET).
toy_pos = [i for i in range(7) if spaces[i] == TOY]
vet_pos = [i for i in range(7) if spaces[i] == VET]
for t in toy_pos:
    for v in vet_pos:
        solver.add(And(t != v, t != v+1, t != v-1))

# Given: Shoe store (SHOE) is in space 4.
solver.add(spaces[3] == SHOE)

# Now, check each option (A-E) to see if it must be true.
# We will push the base constraints, then add each option's constraint, and check for satisfiability.

# Define the options as constraints:
# (A) The optometrist is next to a restaurant.
opt_a_constr = Exists([i], And(
    spaces[i] == OPT,
    Or(
        (i > 0 and spaces[i-1] == REST),
        (i < 6 and spaces[i+1] == REST)
    )
))

# (B) The pharmacy is next to the veterinarian.
opt_b_constr = Exists([i], And(
    spaces[i] == PHAR,
    Or(
        (i > 0 and spaces[i-1] == VET),
        (i < 6 and spaces[i+1] == VET)
    )
))

# (C) A restaurant is next to the toy store.
opt_c_constr = Exists([i], And(
    spaces[i] == REST,
    Or(
        (i > 0 and spaces[i-1] == TOY),
        (i < 6 and spaces[i+1] == TOY)
    )
))

# (D) The shoe store is next to the toy store.
opt_d_constr = And(
    spaces[3] == SHOE,
    Or(
        (3 > 0 and spaces[2] == TOY),
        (3 < 6 and spaces[4] == TOY)
    )
)

# (E) The shoe store is next to the veterinarian.
opt_e_constr = And(
    spaces[3] == SHOE,
    Or(
        (3 > 0 and spaces[2] == VET),
        (3 < 6 and spaces[4] == VET)
    )
)

# Now, test each option
found_options = []
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