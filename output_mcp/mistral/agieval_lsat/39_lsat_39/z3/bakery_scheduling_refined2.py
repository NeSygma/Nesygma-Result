from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare cookie types and batch numbers
cookie_types = [0, 1, 2]  # 0: oatmeal, 1: peanut butter, 2: sugar
batch_numbers = [0, 1, 2]  # 0: first batch, 1: second batch, 2: third batch

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday

# batch_day[c][b] = day when batch b of cookie type c is made
batch_day = [[Int(f"batch_day_{c}_{b}") for b in batch_numbers] for c in cookie_types]

solver = Solver()

# 1. No two batches of the same kind on the same day
for c in cookie_types:
    for b1 in batch_numbers:
        for b2 in batch_numbers:
            if b1 != b2:
                solver.add(batch_day[c][b1] != batch_day[c][b2])

# 2. Each batch is made on a single day (0-4)
for c in cookie_types:
    for b in batch_numbers:
        solver.add(batch_day[c][b] >= 0, batch_day[c][b] <= 4)

# 3. At least one batch is made on Monday (day 0)
solver.add(Or([batch_day[c][b] == 0 for c in cookie_types for b in batch_numbers]))

# 4. Second batch of oatmeal (c=0, b=1) is on the same day as first batch of peanut butter (c=1, b=0)
solver.add(batch_day[0][1] == batch_day[1][0])

# 5. Second batch of sugar (c=2, b=1) is on Thursday (day 3)
solver.add(batch_day[2][1] == 3)

# 6. First batch of peanut butter (c=1, b=0) is on Tuesday (day 1)
solver.add(batch_day[1][0] == 1)

# Base constraints are set. Now evaluate the multiple-choice options.

# Option A: Two different kinds of cookie have their first batch made on Monday.
# This means oatmeal and sugar have their first batch on Monday.
opt_a_constr = And(
    batch_day[0][0] == 0,
    batch_day[2][0] == 0,
    batch_day[1][0] == 1  # peanut butter first batch is Tuesday
)

# Option B: Two different kinds of cookie have their first batch made on Tuesday.
# This means peanut butter and sugar have their first batch on Tuesday.
opt_b_constr = And(
    batch_day[1][0] == 1,  # peanut butter first batch is Tuesday
    batch_day[2][0] == 1,  # sugar first batch is Tuesday
    batch_day[0][0] != 1   # oatmeal first batch is not Tuesday
)

# Option C: Two different kinds of cookie have their second batch made on Wednesday.
# This means two cookie types have their second batch on Wednesday.
# But oatmeal's second batch is on Tuesday (from constraint 4), sugar's second batch is on Thursday (fixed).
# So only peanut butter's second batch could be on Wednesday, which does not satisfy "two different kinds".
opt_c_constr = And(
    Sum([If(batch_day[c][1] == 2, 1, 0) for c in cookie_types]) == 2
)

# Option D: Two different kinds of cookie have their second batch made on Thursday.
# This means sugar and peanut butter have their second batch on Thursday.
opt_d_constr = And(
    batch_day[2][1] == 3,  # sugar second batch is Thursday
    batch_day[1][1] == 3,  # peanut butter second batch is Thursday
    batch_day[0][1] != 3   # oatmeal second batch is not Thursday
)

# Option E: Two different kinds of cookie have their third batch made on Friday.
# This means any two cookie types have their third batch on Friday.
opt_e_constr = And(
    Sum([If(batch_day[c][2] == 4, 1, 0) for c in cookie_types]) == 2
)

# Evaluate each option
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