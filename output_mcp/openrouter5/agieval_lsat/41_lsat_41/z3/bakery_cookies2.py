from z3 import *

# We have 3 kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches (1st, 2nd, 3rd)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

solver = Solver()

# Variables: day each batch is made
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain: each batch is made on Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

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
solver.add(Sum([If(b == 4, 1, 0) for b in all_batches]) == 1)

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    print(f"O1={m[O1]}, O2={m[O2]}, O3={m[O3]}")
    print(f"P1={m[P1]}, P2={m[P2]}, P3={m[P3]}")
    print(f"S1={m[S1]}, S2={m[S2]}, S3={m[S3]}")
else:
    print("Base constraints are UNSAT!")
    exit()

# Now evaluate each option more carefully
# The issue might be that "first batch" means the earliest day, not batch #1
# Let me re-read: "The first batch of sugar cookies" - this means batch #1 (the first one made that week)
# But we need to ensure ordering: O1 < O2 < O3, P1 < P2 < P3, S1 < S2 < S3
# Because "first batch" means the earliest in the week

solver2 = Solver()
for b in all_batches:
    solver2.add(b >= 0, b <= 4)

solver2.add(Distinct(O1, O2, O3))
solver2.add(Distinct(P1, P2, P3))
solver2.add(Distinct(S1, S2, S3))

# Ordering: batch 1 < batch 2 < batch 3 (chronological order)
solver2.add(O1 < O2)
solver2.add(O2 < O3)
solver2.add(P1 < P2)
solver2.add(P2 < P3)
solver2.add(S1 < S2)
solver2.add(S2 < S3)

solver2.add(Or([b == 0 for b in all_batches]))
solver2.add(O2 == P1)
solver2.add(S2 == 3)
solver2.add(Sum([If(b == 4, 1, 0) for b in all_batches]) == 1)

print("\nWith ordering constraints:")
if solver2.check() == sat:
    m = solver2.model()
    print(f"O1={m[O1]}, O2={m[O2]}, O3={m[O3]}")
    print(f"P1={m[P1]}, P2={m[P2]}, P3={m[P3]}")
    print(f"S1={m[S1]}, S2={m[S2]}, S3={m[S3]}")
else:
    print("UNSAT with ordering constraints")

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
    solver2.push()
    solver2.add(constr)
    if solver2.check() == sat:
        found_options.append(letter)
    solver2.pop()

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")