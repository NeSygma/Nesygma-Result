from z3 import *

solver = Solver()

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Batches: O1, O2, O3 for oatmeal; P1, P2, P3 for peanut butter; S1, S2, S3 for sugar
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# Domain constraints: each batch day between 0 and 4 inclusive
solver.add([And(0 <= d, d <= 4) for d in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])

# No two batches of the same kind on the same day
solver.add(O1 != O2, O1 != O3, O2 != O3)
solver.add(P1 != P2, P1 != P3, P2 != P3)
solver.add(S1 != S2, S1 != S3, S2 != S3)

# At least one batch on Monday
solver.add(Or([d == 0 for d in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))

# Second batch of oatmeal on same day as first batch of peanut butter
solver.add(O2 == P1)

# Second batch of sugar on Thursday (day 3)
solver.add(S2 == 3)

# Number of batches made on Friday is exactly one
solver.add(Sum([If(d == 4, 1, 0) for d in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]) == 1)

# Base constraints are now added

# Define options as constraints
opt_a = (S1 == 0)   # first batch of sugar on Monday
opt_b = (O1 == 1)   # first batch of oatmeal on Tuesday
opt_c = (O3 == 4)   # third batch of oatmeal on Friday
opt_d = (P1 == 2)   # first batch of peanut butter on Wednesday
opt_e = (P2 == 1)   # second batch of peanut butter on Tuesday

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