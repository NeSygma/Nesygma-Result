from z3 import *

# Problem analysis:
# - 3 kinds: oatmeal (O), peanut butter (P), sugar (S)
# - 3 batches of each kind: 1st, 2nd, 3rd
# - Days: Monday (1), Tuesday (2), Wednesday (3), Thursday (4), Friday (5)
# - Each batch is made on a single day
# - No two batches of same kind on same day
# - At least one batch on Monday
# - 2nd oatmeal = 1st peanut butter (same day)
# - 2nd sugar = Thursday (day 4)
# - Exactly one batch on Friday

# Variables: For each batch, which day it's made
# Format: batch_kind_batchnum = day (1-5)
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

# At least one batch on Monday (day 1)
solver.add(Or([var == 1 for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))

# 2nd oatmeal = 1st peanut butter
solver.add(O2 == P1)

# 2nd sugar = Thursday (day 4)
solver.add(S2 == 4)

# Exactly one batch on Friday (day 5)
# Count how many variables equal 5
friday_count = Sum([If(var == 5, 1, 0) for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])
solver.add(friday_count == 1)

# Now test each answer choice
# (A) The first batch of sugar cookies is made on Monday.
opt_a = (S1 == 1)

# (B) The first batch of oatmeal cookies is made on Tuesday.
opt_b = (O1 == 2)

# (C) The third batch of oatmeal cookies is made on Friday.
opt_c = (O3 == 5)

# (D) The first batch of peanut butter cookies is made on Wednesday.
opt_d = (P1 == 3)

# (E) The second batch of peanut butter cookies is made on Tuesday.
opt_e = (P2 == 2)

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