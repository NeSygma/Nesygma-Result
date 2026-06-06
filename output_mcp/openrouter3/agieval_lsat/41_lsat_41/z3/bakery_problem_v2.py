from z3 import *

# Variables
O1, O2, O3 = Ints('O1 O2 O3')  # oatmeal batches 1,2,3
P1, P2, P3 = Ints('P1 P2 P3')  # peanut butter batches 1,2,3
S1, S2, S3 = Ints('S1 S2 S3')  # sugar batches 1,2,3

solver = Solver()

# Domain constraints: days 1-5
for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]:
    solver.add(var >= 1, var <= 5)

# No two batches of same kind on same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# Ordering constraints: batches happen in order
solver.add(O1 < O2)
solver.add(O2 < O3)
solver.add(P1 < P2)
solver.add(P2 < P3)
solver.add(S1 < S2)
solver.add(S2 < S3)

# At least one batch on Monday (day 1)
solver.add(Or([var == 1 for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))

# 2nd oatmeal = 1st peanut butter
solver.add(O2 == P1)

# 2nd sugar = Thursday (day 4)
solver.add(S2 == 4)

# Exactly one batch on Friday (day 5)
friday_count = Sum([If(var == 5, 1, 0) for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])
solver.add(friday_count == 1)

# Answer choices
opt_a = (S1 == 1)  # first sugar on Monday
opt_b = (O1 == 2)  # first oatmeal on Tuesday
opt_c = (O3 == 5)  # third oatmeal on Friday
opt_d = (P1 == 3)  # first peanut butter on Wednesday
opt_e = (P2 == 2)  # second peanut butter on Tuesday

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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