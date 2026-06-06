from z3 import *
solver = Solver()

# Declare position variables for each business
O = Int('optometrist')  # optometrist
P = Int('pharmacy')     # pharmacy
R1 = Int('restaurant1') # first restaurant
R2 = Int('restaurant2') # second restaurant
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

# Constraint 1: Pharmacy must be at one end (space 1 or 7)
solver.add(Or(P == 1, P == 7))

# Constraint 2: One restaurant must be at the other end (opposite from pharmacy)
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7), And(R1 != 1, R2 != 1)),
    And(P == 7, Or(R1 == 1, R2 == 1), And(R1 != 7, R2 != 7))
))

# Constraint 3: Two restaurants must be separated by at least two other businesses
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 4: Pharmacy must be next to either optometrist or veterinarian
solver.add(Or(
    Or(P - O == 1, O - P == 1),
    Or(P - V == 1, V - P == 1)
))

# Constraint 5: Toy store cannot be next to veterinarian
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Given constraint: Veterinarian is in space 5
solver.add(V == 5)

# Define options
opt_a_constr = (O == 2)
opt_b_constr = (P == 7)
opt_c_constr = Or(R1 == 4, R2 == 4)
opt_d_constr = (S == 6)
opt_e_constr = (T == 3)

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