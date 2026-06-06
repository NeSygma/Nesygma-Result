from z3 import *
solver = Solver()
# Variables for each business
O = Int('O')  # optometrist
P = Int('P')  # pharmacy
R1 = Int('R1')  # restaurant 1
R2 = Int('R2')  # restaurant 2
S = Int('S')  # shoe store
T = Int('T')  # toy store
V = Int('V')  # veterinarian

# Domain constraints: each space 1..7
for var in [O,P,R1,R2,S,T,V]:
    solver.add(var >= 1, var <= 7)

# All distinct
solver.add(Distinct([O,P,R1,R2,S,T,V]))

# Veterinarian is in space 5
solver.add(V == 5)

# Pharmacy at one end
solver.add(Or(P == 1, P == 7))

# One of the restaurants at the other end
solver.add(Or(And(P == 1, Or(R1 == 7, R2 == 7)),
              And(P == 7, Or(R1 == 1, R2 == 1))))

# Two restaurants separated by at least two other businesses
solver.add(Abs(R1 - R2) >= 3)

# Pharmacy next to either optometrist or veterinarian
solver.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))

# Toy store cannot be next to veterinarian
solver.add(Abs(T - V) != 1)

# Option constraints
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