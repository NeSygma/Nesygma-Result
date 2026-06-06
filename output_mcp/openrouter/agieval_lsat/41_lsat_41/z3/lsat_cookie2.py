from z3 import *

solver = Solver()
# Days 1..5 Mon..Fri
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
for v in all_vars:
    solver.add(v >= 1, v <= 5)
# distinct per kind
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))
# ordering within each kind
solver.add(O1 < O2, O2 < O3)
solver.add(P1 < P2, P2 < P3)
solver.add(S1 < S2, S2 < S3)
# at least one batch Monday
solver.add(Or([v == 1 for v in all_vars]))
# O2 same day as P1
solver.add(O2 == P1)
# S2 Thursday
solver.add(S2 == 4)
# exactly one batch on Friday
friday_count = Sum([If(v == 5, 1, 0) for v in all_vars])
solver.add(friday_count == 1)

# options
opt_a_constr = S1 == 1
opt_b_constr = O1 == 2
opt_c_constr = O3 == 5
opt_d_constr = P1 == 3
opt_e_constr = P2 == 2

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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