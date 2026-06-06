from z3 import *

solver = Solver()

# Variables for positions (1-7)
P = Int('Pharmacy')
R1 = Int('Restaurant1')
R2 = Int('Restaurant2')
O = Int('Optometrist')
S = Int('Shoe')
T = Int('Toy')
V = Int('Veterinarian')

businesses = [P, R1, R2, O, S, T, V]

# Domain constraints: each position from 1 to 7
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All different positions
solver.add(Distinct(businesses))

# Constraint 1: Pharmacy at one end, a restaurant at the other end.
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: The two restaurants separated by at least two other businesses.
# |R1 - R2| >= 3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: Pharmacy next to either optometrist or veterinarian.
# If P is at 1, space 2 is O or V. If P is at 7, space 6 is O or V.
solver.add(Implies(P == 1, Or(O == 2, V == 2)))
solver.add(Implies(P == 7, Or(O == 6, V == 6)))

# Constraint 4: Toy store cannot be next to veterinarian.
# |T - V| != 1, so |T - V| >= 2
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Given: Shoe store is in space 4.
solver.add(S == 4)

# Now evaluate each option to see which MUST be true.
# An option "must be true" if it is entailed by the premises.
# That means: when we add the negation of the option to the solver, it becomes unsatisfiable.

found_options = []

# Option A: The optometrist is next to a restaurant.
# O is next to R1 or O is next to R2
opt_a_constr = Or(
    Or(O - R1 == 1, R1 - O == 1),
    Or(O - R2 == 1, R2 - O == 1)
)

solver.push()
solver.add(Not(opt_a_constr))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: The pharmacy is next to the veterinarian.
opt_b_constr = Or(P - V == 1, V - P == 1)

solver.push()
solver.add(Not(opt_b_constr))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: A restaurant is next to the toy store.
opt_c_constr = Or(
    Or(R1 - T == 1, T - R1 == 1),
    Or(R2 - T == 1, T - R2 == 1)
)

solver.push()
solver.add(Not(opt_c_constr))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: The shoe store is next to the toy store.
# Shoe is at space 4. So T must be 3 or 5.
opt_d_constr = Or(T == 3, T == 5)

solver.push()
solver.add(Not(opt_d_constr))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: The shoe store is next to the veterinarian.
# Shoe is at space 4. So V must be 3 or 5.
opt_e_constr = Or(V == 3, V == 5)

solver.push()
solver.add(Not(opt_e_constr))
if solver.check() == unsat:
    found_options.append("E")
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