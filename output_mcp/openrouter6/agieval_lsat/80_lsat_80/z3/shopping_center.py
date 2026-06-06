from z3 import *

solver = Solver()

# Declare variables
O = Int('O')
P = Int('P')
R1 = Int('R1')
R2 = Int('R2')
S = Int('S')
T = Int('T')
V = Int('V')

# Shoe store is in space 4
solver.add(S == 4)

# All positions between 1 and 7
solver.add(1 <= O, O <= 7)
solver.add(1 <= P, P <= 7)
solver.add(1 <= R1, R1 <= 7)
solver.add(1 <= R2, R2 <= 7)
solver.add(1 <= S, S <= 7)
solver.add(1 <= T, T <= 7)
solver.add(1 <= V, V <= 7)

# All distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Constraint 1: Pharmacy at one end, restaurant at the other
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: Two restaurants separated by at least two other businesses
solver.add(Abs(R1 - R2) >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 4: Toy store not next to veterinarian
solver.add(Not(Or(
    Abs(T - V) == 1
)))

# Define option constraints
opt_a_constr = Or(
    Abs(O - R1) == 1,
    Abs(O - R2) == 1
)

opt_b_constr = Abs(P - V) == 1

opt_c_constr = Or(
    Abs(R1 - T) == 1,
    Abs(R2 - T) == 1
)

opt_d_constr = Abs(S - T) == 1  # S=4, so T=3 or 5

opt_e_constr = Abs(S - V) == 1  # S=4, so V=3 or 5

# Evaluate each option
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