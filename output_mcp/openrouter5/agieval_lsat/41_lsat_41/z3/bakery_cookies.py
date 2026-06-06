from z3 import *

# We have 3 kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches (1st, 2nd, 3rd)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

solver = Solver()

# Variables: day each batch is made
# O1, O2, O3 = day of 1st, 2nd, 3rd oatmeal batch
# P1, P2, P3 = day of 1st, 2nd, 3rd peanut butter batch
# S1, S2, S3 = day of 1st, 2nd, 3rd sugar batch

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain: each batch is made on Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Exactly three batches of each kind are made each week (already encoded by having 3 vars per kind)

# No two batches of the same kind are made on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch of cookies is made on Monday
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
solver.add(O2 == P1)

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(S2 == 3)

# Additional condition: The number of batches made on Friday is exactly one
# Count how many batches are on Friday (day 4)
solver.add(Sum([If(b == 4, 1, 0) for b in all_batches]) == 1)

# Now evaluate each option

# Option A: The first batch of sugar cookies is made on Monday.
opt_a = (S1 == 0)

# Option B: The first batch of oatmeal cookies is made on Tuesday.
opt_b = (O1 == 1)

# Option C: The third batch of oatmeal cookies is made on Friday.
opt_c = (O3 == 4)

# Option D: The first batch of peanut butter cookies is made on Wednesday.
opt_d = (P1 == 2)

# Option E: The second batch of peanut butter cookies is made on Tuesday.
opt_e = (P2 == 1)

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