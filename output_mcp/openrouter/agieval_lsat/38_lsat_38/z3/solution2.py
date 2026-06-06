from z3 import *

solver = Solver()
# Days 0-4
O1,O2,O3 = Ints('O1 O2 O3')
P1,P2,P3 = Ints('P1 P2 P3')
S1,S2,S3 = Ints('S1 S2 S3')
vars = [O1,O2,O3,P1,P2,P3,S1,S2,S3]
for v in vars:
    solver.add(v >= 0, v <= 4)
# distinct per kind
solver.add(Distinct(O1,O2,O3))
solver.add(Distinct(P1,P2,P3))
solver.add(Distinct(S1,S2,S3))
# at least one batch Monday
solver.add(Or([v == 0 for v in vars]))
# constraints
solver.add(O2 == P1)
solver.add(S2 == 3)

# Determine for each day if >=3 possible
limited = []  # days where cannot have >=3
for d in range(5):
    s = Solver()
    s.add(solver.assertions())
    cnt = Sum([If(v == d, 1, 0) for v in vars])
    s.add(cnt >= 3)
    if s.check() == unsat:
        limited.append(d)
# number of limited days
num_limited = len(limited)
# Options
opt_a = (num_limited == 1)
opt_b = (num_limited == 2)
opt_c = (num_limited == 3)
opt_d = (num_limited == 4)
opt_e = (num_limited == 5)

found = []
for letter, constr in [("A",opt_a),("B",opt_b),("C",opt_c),("D",opt_d),("E",opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")