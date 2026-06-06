from z3 import *

solver = Solver()

# Declare variables for each business's space (1-7)
O = Int('Optometrist')
P = Int('Pharmacy')
R1 = Int('Restaurant1')
R2 = Int('Restaurant2')
S = Int('ShoeStore')
T = Int('ToyStore')
V = Int('Veterinarian')

# Base constraints
# All spaces are distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))
# Veterinarian is in space 5
solver.add(V == 5)

# Pharmacy at one end, restaurant at the other end
solver.add(Or(P == 1, P == 7))
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Two restaurants separated by at least two other businesses
solver.add(Abs(R1 - R2) >= 3)

# Pharmacy next to optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Toy store not next to veterinarian
solver.add(Abs(T - V) != 1)

# Define the options as the negation of each statement
# We want to find which option must be true, i.e., its negation is unsatisfiable
opt_a_constr = Not(O == 2)          # (A) The optometrist is in space 2
opt_b_constr = Not(P == 7)          # (B) The pharmacy is in space 7
opt_c_constr = Not(Or(R1 == 4, R2 == 4))  # (C) A restaurant is in space 4
opt_d_constr = Not(S == 6)          # (D) The shoe store is in space 6
opt_e_constr = Not(T == 3)          # (E) The toy store is in space 3

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:   # If negation is unsatisfiable, the option must be true
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