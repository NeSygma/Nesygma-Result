from z3 import *

solver = Solver()

# Declare variables for positions (1..7)
O = Int('O')
P = Int('P')
R1 = Int('R1')
R2 = Int('R2')
S = Int('S')
T = Int('T')
V = Int('V')

# Base constraints
# All positions between 1 and 7
solver.add(O >= 1, O <= 7)
solver.add(P >= 1, P <= 7)
solver.add(R1 >= 1, R1 <= 7)
solver.add(R2 >= 1, R2 <= 7)
solver.add(S >= 1, S <= 7)
solver.add(T >= 1, T <= 7)
solver.add(V >= 1, V <= 7)

# All distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Shoe store is in space 2
solver.add(S == 2)

# Pharmacy at one end, restaurant at the other end
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Two restaurants separated by at least two other businesses
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Pharmacy next to optometrist or veterinarian
solver.add(Or(
    P - O == 1,
    P - O == -1,
    P - V == 1,
    P - V == -1
))

# Toy store not next to veterinarian
solver.add(And(T - V != 1, T - V != -1))

# Define option constraints
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