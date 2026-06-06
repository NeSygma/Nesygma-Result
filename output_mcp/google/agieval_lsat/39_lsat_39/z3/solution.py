from z3 import *

solver = Solver()

O = [Int('O1'), Int('O2'), Int('O3')]
P = [Int('P1'), Int('P2'), Int('P3')]
S = [Int('S1'), Int('S2'), Int('S3')]

for b in O + P + S:
    solver.add(b >= 0, b <= 4)

solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))

solver.add(Or([b == 0 for b in O + P + S]))
solver.add(O[1] == P[0])
solver.add(S[1] == 3)
solver.add(P[0] == 1)

# Options
opt_a = Or(And(O[0] == 0, P[0] == 0), And(O[0] == 0, S[0] == 0), And(P[0] == 0, S[0] == 0))
opt_b = Or(And(O[1] == 1, P[1] == 1), And(O[1] == 1, S[1] == 1), And(P[1] == 1, S[1] == 1))
opt_c = Or(And(O[1] == 2, P[1] == 2), And(O[1] == 2, S[1] == 2), And(P[1] == 2, S[1] == 2))
opt_d = Or(And(O[1] == 3, P[1] == 3), And(O[1] == 3, S[1] == 3), And(P[1] == 3, S[1] == 3))
opt_e = Or(And(O[2] == 4, P[2] == 4), And(O[2] == 4, S[2] == 4), And(P[2] == 4, S[2] == 4))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for name, constr in options:
    solver.push()
    solver.add(constr)
    res = solver.check()
    print(f"Option {name}: {res}")
    solver.pop()