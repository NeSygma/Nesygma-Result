from z3 import *

solver = Solver()

# Slots 1-6, each band gets one slot
slots = [1, 2, 3, 4, 5, 6]

# Variables for each band's slot
Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon = Ints('Uneasy Vegemite Wellspring Xpert Yardsign Zircon')
bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]

# Each band gets a slot from 1 to 6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All slots are distinct
solver.add(Distinct(bands))

# Constraints:
# Vegemite performs in an earlier slot than Zircon.
solver.add(Vegemite < Zircon)

# Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)

# Uneasy performs in one of the last three slots (4, 5, or 6).
solver.add(Or([Uneasy == i for i in [4, 5, 6]]))

# Yardsign performs in one of the first three slots (1, 2, or 3).
solver.add(Or([Yardsign == i for i in [1, 2, 3]]))

# Additional condition: Zircon performs immediately before Wellspring.
solver.add(Zircon + 1 == Wellspring)

# Let's first see what models exist to understand the constraints better
print("All solutions:")
solver_copy = Solver()
for c in solver.assertions():
    solver_copy.add(c)

solutions = []
while solver_copy.check() == sat:
    m = solver_copy.model()
    sol = {str(b): m.eval(b, model_completion=True).as_long() for b in bands}
    solutions.append(sol)
    solver_copy.add(Or([b != m.eval(b, model_completion=True) for b in bands]))

print(f"Total solutions: {len(solutions)}")
for s in solutions:
    print(s)

# Now evaluate each option as "must be true" - meaning it holds in ALL solutions
# So we check if the negation is unsatisfiable
print("\nChecking which options MUST be true (hold in all solutions):")
for letter, constr in [("A", Uneasy == 5), ("B", Vegemite == 1), ("C", Xpert == 5), ("D", Yardsign == 2), ("E", Zircon == 3)]:
    s2 = Solver()
    for c in solver.assertions():
        s2.add(c)
    s2.add(Not(constr))
    res = s2.check()
    if res == unsat:
        print(f"Option {letter} MUST be true (negation unsat)")
    else:
        print(f"Option {letter} is NOT necessarily true (negation sat)")