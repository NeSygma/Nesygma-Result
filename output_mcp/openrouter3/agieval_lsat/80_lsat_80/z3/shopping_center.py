from z3 import *

# Create solver
solver = Solver()

# Define positions for each business (1-7)
O = Int('optometrist')
P = Int('pharmacy')
R1 = Int('restaurant1')
R2 = Int('restaurant2')
S = Int('shoe_store')
T = Int('toy_store')
V = Int('veterinarian')

# All positions must be between 1 and 7
solver.add(O >= 1, O <= 7)
solver.add(P >= 1, P <= 7)
solver.add(R1 >= 1, R1 <= 7)
solver.add(R2 >= 1, R2 <= 7)
solver.add(S >= 1, S <= 7)
solver.add(T >= 1, T <= 7)
solver.add(V >= 1, V <= 7)

# All positions must be distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Given: Shoe store is in space 4
solver.add(S == 4)

# Constraint 1: Pharmacy at one end (space 1 or 7)
solver.add(Or(P == 1, P == 7))

# Constraint 2: One restaurant at the other end
# If pharmacy is at 1, then one restaurant must be at 7
# If pharmacy is at 7, then one restaurant must be at 1
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 3: Two restaurants separated by at least two other businesses
# |R1 - R2| >= 3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 4: Pharmacy next to either optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 5: Toy store not next to veterinarian
solver.add(Abs(T - V) != 1)

# Now evaluate each answer choice
# Answer choices:
# (A) The optometrist is next to a restaurant.
# (B) The pharmacy is next to the veterinarian.
# (C) A restaurant is next to the toy store.
# (D) The shoe store is next to the toy store.
# (E) The shoe store is next to the veterinarian.

# Define constraints for each option
opt_a = Or(Abs(O - R1) == 1, Abs(O - R2) == 1)
opt_b = Abs(P - V) == 1
opt_c = Or(Abs(R1 - T) == 1, Abs(R2 - T) == 1)
opt_d = Abs(S - T) == 1
opt_e = Abs(S - V) == 1

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