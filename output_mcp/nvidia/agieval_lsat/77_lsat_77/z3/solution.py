from z3 import *

solver = Solver()

# Variables
O = Int('O')
P = Int('P')
R1 = Int('R1')
R2 = Int('R2')
S = Int('S')
T = Int('T')
V = Int('V')

# Shoe store in space 2
solver.add(S == 2)

# All different
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Base constraints
# Pharmacy at end and a restaurant at other end
solver.add(Or(And(P == 1, Or(R1 == 7, R2 == 7)),
              And(P == 7, Or(R1 == 1, R2 == 1))))

# Restaurants separated by at least two other businesses
solver.add(Or(R1 >= R2 + 3, R2 >= R1 + 3))

# Pharmacy next to optometrist or veterinarian
solver.add(Or(P == O+1, P == O-1, P == V+1, P == V-1))

# Toy store not next to veterinarian
solver.add(Not(Or(T == V+1, T == V-1)))

# Test each answer choice
found_options = []

# Option A: optometrist in space 5
opt_a_constr = (O == 5)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: pharmacy in space 1
opt_b_constr = (P == 1)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: a restaurant in space 3
opt_c_constr = Or(R1 == 3, R2 == 3)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: toy store in space 6
opt_d_constr = (T == 6)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: veterinarian in space 4
opt_e_constr = (V == 4)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")