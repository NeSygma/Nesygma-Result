from z3 import *

solver = Solver()

# We have 3 kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches (first, second, third)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Constraint: No batch on Wednesday (day 2) - this is the "if" condition we add as base

# We'll use integer variables for each batch: day of week (0-4)
# O1, O2, O3 = oatmeal batches 1,2,3
# P1, P2, P3 = peanut butter batches 1,2,3
# S1, S2, S3 = sugar batches 1,2,3

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain: each batch is made on Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
# Oatmeal: O1, O2, O3 all different days
solver.add(Distinct(O1, O2, O3))
# Peanut butter: P1, P2, P3 all different days
solver.add(Distinct(P1, P2, P3))
# Sugar: S1, S2, S3 all different days
solver.add(Distinct(S1, S2, S3))

# At least one batch of cookies is made on Monday
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
solver.add(O2 == P1)

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(S2 == 3)

# IF condition: No batch of cookies is made on Wednesday (day 2)
solver.add(And([b != 2 for b in all_batches]))

# Now evaluate each option

# Option A: Exactly three batches of cookies are made on Tuesday (day 1)
opt_a = Sum([If(b == 1, 1, 0) for b in all_batches]) == 3

# Option B: Exactly three batches of cookies are made on Friday (day 4)
opt_b = Sum([If(b == 4, 1, 0) for b in all_batches]) == 3

# Option C: At least two batches of cookies are made on Monday (day 0)
opt_c = Sum([If(b == 0, 1, 0) for b in all_batches]) >= 2

# Option D: At least two batches of cookies are made on Thursday (day 3)
opt_d = Sum([If(b == 3, 1, 0) for b in all_batches]) >= 2

# Option E: Fewer batches on Monday than on Tuesday
opt_e = Sum([If(b == 0, 1, 0) for b in all_batches]) < Sum([If(b == 1, 1, 0) for b in all_batches])

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