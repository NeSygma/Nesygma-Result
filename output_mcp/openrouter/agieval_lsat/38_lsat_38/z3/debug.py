from z3 import *
solver = Solver()
O1,O2,O3 = Ints('O1 O2 O3')
P1,P2,P3 = Ints('P1 P2 P3')
S1,S2,S3 = Ints('S1 S2 S3')
vars = [O1,O2,O3,P1,P2,P3,S1,S2,S3]
for v in vars:
    solver.add(v >= 0, v <= 4)
solver.add(Distinct(O1,O2,O3))
solver.add(Distinct(P1,P2,P3))
solver.add(Distinct(S1,S2,S3))
solver.add(Or([v == 0 for v in vars]))
solver.add(O2 == P1)
solver.add(S2 == 3)
limited = []
for d in range(5):
    s = Solver()
    s.add(solver.assertions())
    cnt = Sum([If(v == d, 1, 0) for v in vars])
    s.add(cnt >= 3)
    if s.check() == unsat:
        limited.append(d)
print('limited days', limited)
print('num_limited', len(limited))