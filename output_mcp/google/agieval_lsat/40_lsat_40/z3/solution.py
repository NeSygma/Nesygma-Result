from z3 import *

solver = Solver()

# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
# No Wednesday: days are {0, 1, 3, 4}
days = [0, 1, 3, 4]

# Batches: 3 of each kind (O, P, S)
# O1, O2, O3 are the days for the 3 oatmeal batches
# P1, P2, P3 are the days for the 3 peanut butter batches
# S1, S2, S3 are the days for the 3 sugar batches
O = [Int(f'O_{i}') for i in range(3)]
P = [Int(f'P_{i}') for i in range(3)]
S = [Int(f'S_{i}') for i in range(3)]

# Constraints:
# 1. Each batch is on a valid day (not Wednesday)
for day in O + P + S:
    solver.add(Or([day == d for d in days]))

# 2. No two batches of the same kind on the same day (already implied by ordering + distinct)
# Ordering: O1 <= O2 <= O3, P1 <= P2 <= P3, S1 <= S2 <= S3
# Wait, if they are on the same day, they are not distinct.
# The problem says "No two batches of the same kind of cookie are made on the same day."
# This means O1 < O2 < O3, P1 < P2 < P3, S1 < S2 < S3.
solver.add(O[0] < O[1], O[1] < O[2])
solver.add(P[0] < P[1], P[1] < P[2])
solver.add(S[0] < S[1], S[1] < S[2])

# 3. At least one batch on Monday (day 0)
solver.add(Or([d == 0 for d in O + P + S]))

# 4. Second batch of oatmeal (O[1]) is on the same day as first batch of peanut butter (P[0])
solver.add(O[1] == P[0])

# 5. Second batch of sugar (S[1]) is on Thursday (day 3)
solver.add(S[1] == 3)

# Helper to count batches on a day
def count_on_day(day_val):
    return Sum([If(d == day_val, 1, 0) for d in O + P + S])

# Options
# (A) Exactly three batches on Tuesday (day 1)
opt_a = (count_on_day(1) == 3)
# (B) Exactly three batches on Friday (day 4)
opt_b = (count_on_day(4) == 3)
# (C) At least two batches on Monday (day 0)
opt_c = (count_on_day(0) >= 2)
# (D) At least two batches on Thursday (day 3)
opt_d = (count_on_day(3) >= 2)
# (E) Fewer batches on Monday than on Tuesday
opt_e = (count_on_day(0) < count_on_day(1))

# We need to find which one MUST be true.
# This means for all valid models, the option must be true.
# Equivalently, there is no model where the option is false.

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        # If Not(constr) is unsat, then constr must be true in all models
        found_options.append(letter)
    solver.pop()

print(f"Must be true options: {found_options}")