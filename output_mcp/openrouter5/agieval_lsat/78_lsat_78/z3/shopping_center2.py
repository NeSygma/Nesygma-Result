from z3 import *

solver = Solver()

# 7 spaces, numbered 1 to 7
O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')

businesses = [O, P, R1, R2, S, T, V]
solver.add(Distinct(businesses))
for b in businesses:
    solver.add(b >= 1, b <= 7)

# Constraint 1: Pharmacy at one end, one of the restaurants at the other.
solver.add(Or(P == 1, P == 7))
solver.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
solver.add(Implies(P == 1, Or(R1 == 7, R2 == 7)))
solver.add(Implies(P == 7, Or(R1 == 1, R2 == 1)))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian.
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 4: Toy store cannot be next to veterinarian.
solver.add(Not(Abs(T - V) == 1))

# Veterinarian is in space 5.
solver.add(V == 5)

# Let's first check if the base constraints are satisfiable
print("Base constraints check:")
if solver.check() == sat:
    m = solver.model()
    print("SAT - example model:")
    for b in businesses:
        print(f"  {b} = {m[b]}")
else:
    print("UNSAT - base constraints inconsistent")
    exit()

# Now evaluate each option as "must be true" - meaning it holds in ALL models.
# We test if the negation of the option is satisfiable. If not, it must be true.

found_options = []
for letter, constr in [("A", O == 2), ("B", P == 7), ("C", Or(R1 == 4, R2 == 4)), ("D", S == 6), ("E", T == 3)]:
    solver.push()
    # Check if the negation is unsatisfiable -> the option must be true
    solver.add(Not(constr))
    if solver.check() == unsat:
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