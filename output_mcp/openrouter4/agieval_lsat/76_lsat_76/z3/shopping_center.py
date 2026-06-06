from z3 import *

# Define the businesses
# P = Pharmacy, O = Optometrist, R = Restaurant (two of them), S = Shoe store, T = Toy store, V = Veterinarian
# We have two restaurants: R1 and R2

solver = Solver()

# Positions 1-7
positions = list(range(7))  # 0-indexed internally, but we'll map 0 to space 1, etc.

# Variables for each business's position
P = Int('Pharmacy')
O = Int('Optometrist')
R1 = Int('Restaurant1')
R2 = Int('Restaurant2')
S = Int('ShoeStore')
T = Int('ToyStore')
V = Int('Veterinarian')

all_businesses = [P, O, R1, R2, S, T, V]

# Domain: each business is in one of positions 1-7 (we'll use 1-7)
for b in all_businesses:
    solver.add(b >= 1, b <= 7)

# All different positions
solver.add(Distinct(all_businesses))

# Constraint 1: Pharmacy at one end and one of the restaurants at the other
solver.add(Or(P == 1, P == 7))
solver.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
# Make sure they're at opposite ends
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: The two restaurants must be separated by at least two other businesses
# That means |R1 - R2| >= 3 (since if they're at positions 1 and 4, that's 2 businesses between them)
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: The pharmacy must be next to either the optometrist or the veterinarian
# Next to means absolute difference of 1
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 4: The toy store cannot be next to the veterinarian
solver.add(Not(Abs(T - V) == 1))

# Now define each option as a complete assignment
# Option A: pharmacy, optometrist, shoe store, restaurant, veterinarian, toy store, restaurant
opt_a_constr = And(
    P == 1, O == 2, S == 3,
    Or(And(R1 == 4, R2 == 7), And(R1 == 7, R2 == 4)),
    V == 5, T == 6
)

# Option B: pharmacy, veterinarian, optometrist, shoe store, restaurant, toy store, restaurant
opt_b_constr = And(
    P == 1, V == 2, O == 3, S == 4,
    Or(And(R1 == 5, R2 == 7), And(R1 == 7, R2 == 5)),
    T == 6
)

# Option C: restaurant, shoe store, veterinarian, pharmacy, optometrist, toy store, restaurant
opt_c_constr = And(
    Or(And(R1 == 1, R2 == 7), And(R1 == 7, R2 == 1)),
    S == 2, V == 3, P == 4, O == 5, T == 6
)

# Option D: restaurant, toy store, optometrist, restaurant, veterinarian, shoe store, pharmacy
opt_d_constr = And(
    Or(And(R1 == 1, R2 == 4), And(R1 == 4, R2 == 1)),
    T == 2, O == 3, V == 5, S == 6, P == 7
)

# Option E: restaurant, optometrist, toy store, restaurant, shoe store, veterinarian, pharmacy
opt_e_constr = And(
    Or(And(R1 == 1, R2 == 4), And(R1 == 4, R2 == 1)),
    O == 2, T == 3, S == 5, V == 6, P == 7
)

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