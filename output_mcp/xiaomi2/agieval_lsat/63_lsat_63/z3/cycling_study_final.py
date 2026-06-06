from z3 import *

solver = Solver()

# Riders: R=0, S=1, T=2, Y=3
# Bicycles: F=0, G=1, H=2, J=3

R1, S1, T1, Y1 = Ints('R1 S1 T1 Y1')
R2, S2, T2, Y2 = Ints('R2 S2 T2 Y2')

F, G, H, J = 0, 1, 2, 3

for v in [R1, S1, T1, Y1, R2, S2, T2, Y2]:
    solver.add(And(v >= 0, v <= 3))

solver.add(Distinct(R1, S1, T1, Y1))
solver.add(Distinct(R2, S2, T2, Y2))

solver.add(R1 != R2)
solver.add(S1 != S2)
solver.add(T1 != T2)
solver.add(Y1 != Y2)

solver.add(R1 != F)
solver.add(R2 != F)

solver.add(Y1 != J)
solver.add(Y2 != J)

solver.add(Or(T1 == H, T2 == H))

solver.add(S2 == Y1)

# Question: Which CANNOT be true?
# Test each option; the one that returns UNSAT is the answer
options = [
    ("A", R2 == G),
    ("B", S1 == F),
    ("C", T2 == F),
    ("D", R1 == H),
    ("E", Y2 == F),
]

impossible_options = []
for letter, constr in options:
    s = Solver()
    # Copy base constraints
    for c in solver.assertions():
        s.add(c)
    s.add(constr)
    if s.check() == unsat:
        impossible_options.append(letter)

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")