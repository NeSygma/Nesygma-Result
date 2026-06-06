from z3 import *

solver = Solver()

# Riders: R=0, S=1, T=2, Y=3
# Bicycles: F=0, G=1, H=2, J=3

# Day 1 assignments (rider -> bicycle)
R1, S1, T1, Y1 = Ints('R1 S1 T1 Y1')
# Day 2 assignments (rider -> bicycle)
R2, S2, T2, Y2 = Ints('R2 S2 T2 Y2')

F, G, H, J = 0, 1, 2, 3

# All assignments are in {0,1,2,3} (i.e., F, G, H, J)
for v in [R1, S1, T1, Y1, R2, S2, T2, Y2]:
    solver.add(And(v >= 0, v <= 3))

# Each day is a permutation (all bicycles tested, each by exactly one rider)
solver.add(Distinct(R1, S1, T1, Y1))
solver.add(Distinct(R2, S2, T2, Y2))

# Each rider tests a different bicycle on day 2 than day 1
solver.add(R1 != R2)
solver.add(S1 != S2)
solver.add(T1 != T2)
solver.add(Y1 != Y2)

# Constraint 1: Reynaldo cannot test F
solver.add(R1 != F)
solver.add(R2 != F)

# Constraint 2: Yuki cannot test J
solver.add(Y1 != J)
solver.add(Y2 != J)

# Constraint 3: Theresa must test H on at least one day
solver.add(Or(T1 == H, T2 == H))

# Constraint 4: Bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(S2 == Y1)

# Now evaluate each option to see which CANNOT be true
# (A) Reynaldo tests G on the second day: R2 == G
# (B) Seamus tests F on the first day: S1 == F
# (C) Theresa tests F on the second day: T2 == F
# (D) Reynaldo tests H on the first day: R1 == H
# (E) Yuki tests F on the second day: Y2 == F

options = [
    ("A", R2 == G),
    ("B", S1 == F),
    ("C", T2 == F),
    ("D", R1 == H),
    ("E", Y2 == F),
]

found_options = []
for letter, constr in options:
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

# Also print which options are possible and which are not for debugging
print(f"\nPossible options: {found_options}")
impossible = [l for l, _ in options if l not in found_options]
print(f"Impossible options (CANNOT be true): {impossible}")