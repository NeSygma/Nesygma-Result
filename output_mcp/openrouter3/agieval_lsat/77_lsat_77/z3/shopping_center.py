from z3 import *

# Create solver
solver = Solver()

# Declare position variables for each business (1-7)
O = Int('optometrist')  # optometrist
P = Int('pharmacy')     # pharmacy
R1 = Int('restaurant1') # restaurant 1
R2 = Int('restaurant2') # restaurant 2
S = Int('shoe_store')   # shoe store
T = Int('toy_store')    # toy store
V = Int('veterinarian') # veterinarian

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

# Constraint 6: Shoe store is in space 2
solver.add(S == 2)

# Constraint 1: Pharmacy at one end (space 1 or 7)
solver.add(Or(P == 1, P == 7))

# Constraint 2: One restaurant at the other end
# If pharmacy is at 1, one restaurant must be at 7
# If pharmacy is at 7, one restaurant must be at 1
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 3: Two restaurants separated by at least two other businesses
# |R1 - R2| >= 3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 4: Pharmacy next to either optometrist or veterinarian
# |P - O| = 1 OR |P - V| = 1
solver.add(Or(
    Or(P - O == 1, O - P == 1),
    Or(P - V == 1, V - P == 1)
))

# Constraint 5: Toy store not next to veterinarian
# |T - V| != 1
solver.add(Or(T - V != 1, V - T != 1))
# Actually, we need to ensure the absolute difference is not 1
# Better: Not(Or(T - V == 1, V - T == 1))
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Now test each answer choice
# Answer choices:
# (A) The optometrist is in space 5
# (B) The pharmacy is in space 1
# (C) A restaurant is in space 3
# (D) The toy store is in space 6
# (E) The veterinarian is in space 4

# Define constraints for each option
opt_a_constr = (O == 5)
opt_b_constr = (P == 1)
opt_c_constr = Or(R1 == 3, R2 == 3)
opt_d_constr = (T == 6)
opt_e_constr = (V == 4)

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