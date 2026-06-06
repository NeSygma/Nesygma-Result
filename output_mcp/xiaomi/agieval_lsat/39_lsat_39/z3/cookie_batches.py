from z3 import *

solver = Solver()

# Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5
# Variables: batch_k_i = day when batch i (1,2,3) of kind k is made
# Kinds: O=Oatmeal, P=Peanut Butter, S=Sugar

# Create variables for each batch of each kind
O1, O2, O3 = Ints('O1 O2 O3')  # Oatmeal batches 1,2,3
P1, P2, P3 = Ints('P1 P2 P3')  # Peanut Butter batches 1,2,3
S1, S2, S3 = Ints('S1 S2 S3')  # Sugar batches 1,2,3

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain: each batch is made on day 1-5 (Monday-Friday)
for b in all_batches:
    solver.add(b >= 1, b <= 5)

# No two batches of the same kind on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday (day 1)
solver.add(Or([b == 1 for b in all_batches]))

# Second batch of oatmeal = First batch of peanut butter (same day)
solver.add(O2 == P1)

# Second batch of sugar = Thursday (day 4)
solver.add(S2 == 4)

# Given: First batch of peanut butter = Tuesday (day 2)
solver.add(P1 == 2)

# This means O2 = 2 as well (from O2 == P1)

# Now evaluate each option - which CANNOT be true?
# We check if each option is SATISFIABLE. The one that is NOT satisfiable is the answer.

# Option A: Two different kinds have their first batch on Monday
# Means at least two of {O1, P1, S1} equal 1
opt_a = Or(
    And(O1 == 1, P1 == 1),
    And(O1 == 1, S1 == 1),
    And(P1 == 1, S1 == 1)
)

# Option B: Two different kinds have their first batch on Tuesday
# Means at least two of {O1, P1, S1} equal 2
opt_b = Or(
    And(O1 == 2, P1 == 2),
    And(O1 == 2, S1 == 2),
    And(P1 == 2, S1 == 2)
)

# Option C: Two different kinds have their second batch on Wednesday
# Means at least two of {O2, P2, S2} equal 3
opt_c = Or(
    And(O2 == 3, P2 == 3),
    And(O2 == 3, S2 == 3),
    And(P2 == 3, S2 == 3)
)

# Option D: Two different kinds have their second batch on Thursday
# Means at least two of {O2, P2, S2} equal 4
opt_d = Or(
    And(O2 == 4, P2 == 4),
    And(O2 == 4, S2 == 4),
    And(P2 == 4, S2 == 4)
)

# Option E: Two different kinds have their third batch on Friday
# Means at least two of {O3, P3, S3} equal 5
opt_e = Or(
    And(O3 == 5, P3 == 5),
    And(O3 == 5, S3 == 5),
    And(P3 == 5, S3 == 5)
)

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