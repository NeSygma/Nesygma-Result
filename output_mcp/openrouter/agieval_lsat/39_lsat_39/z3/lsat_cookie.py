from z3 import *

# Base constraints
# Days: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

solver = Solver()
# domain constraints
for v in [O1,O2,O3,P1,P2,P3,S1,S2,S3]:
    solver.add(v >= 0, v <= 4)
# distinct per kind
solver.add(Distinct(O1,O2,O3))
solver.add(Distinct(P1,P2,P3))
solver.add(Distinct(S1,S2,S3))
# at least one batch on Monday (day 0)
solver.add(Or(O1==0, O2==0, O3==0, P1==0, P2==0, P3==0, S1==0, S2==0, S3==0))
# given conditions
solver.add(P1 == 1)   # Tuesday
solver.add(O2 == P1)   # O2 same day as P1
solver.add(S2 == 3)    # Thursday

# Option constraints definitions
# A: O1 and S1 both Monday
opt_a = And(O1 == 0, S1 == 0)
# B: P1 Tuesday and another first batch Tuesday (O1 or S1)
opt_b = Or(O1 == 1, S1 == 1)
# C: two different kinds have second batch Wednesday -> need P2==2 and (O2==2 or S2==2)
opt_c = And(P2 == 2, Or(O2 == 2, S2 == 2))
# D: two different kinds have second batch Thursday -> need P2==3 (since S2 already Thursday)
opt_d = P2 == 3
# E: at least two third batches on Friday (day 4)
cnt_friday = Sum([If(O3 == 4, 1, 0), If(P3 == 4, 1, 0), If(S3 == 4, 1, 0)])
opt_e = cnt_friday >= 2

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

unsat_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

# Determine the single impossible option
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")