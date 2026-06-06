from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# Batches: 1st, 2nd, 3rd for each type

solver = Solver()

# Variables: batch[type][batch_num] = day (0-4)
# type 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# batch_num 0=1st, 1=2nd, 2=3rd
batch = [[Int(f'batch_{t}_{b}') for b in range(3)] for t in range(3)]

# Each batch is made on a day 0-4
for t in range(3):
    for b in range(3):
        solver.add(batch[t][b] >= 0, batch[t][b] <= 4)

# No two batches of the same kind on the same day
for t in range(3):
    solver.add(Distinct(batch[t][0], batch[t][1], batch[t][2]))

# At least one batch on Monday (day 0)
all_batches = [batch[t][b] for t in range(3) for b in range(3)]
solver.add(Or([b == 0 for b in all_batches]))

# The 2nd batch of oatmeal (type 0, batch 1) is made on the same day as 
# the 1st batch of peanut butter (type 1, batch 0)
solver.add(batch[0][1] == batch[1][0])

# The 2nd batch of sugar cookies (type 2, batch 1) is made on Thursday (day 3)
solver.add(batch[2][1] == 3)

# Count batches per day
batches_per_day = [Int(f'batches_day_{d}') for d in range(5)]
for d in range(5):
    solver.add(batches_per_day[d] == Sum([If(batch[t][b] == d, 1, 0) for t in range(3) for b in range(3)]))

# Question: How many days have at most 2 batches?
# "at most two batches" means batches_per_day[d] <= 2
days_at_most_2 = Int('days_at_most_2')
solver.add(days_at_most_2 == Sum([If(batches_per_day[d] <= 2, 1, 0) for d in range(5)]))

# Now test each answer option
# (A) one day has at most 2 batches -> days_at_most_2 == 1
# (B) two days -> days_at_most_2 == 2
# (C) three days -> days_at_most_2 == 3
# (D) four days -> days_at_most_2 == 4
# (E) five days -> days_at_most_2 == 5

found_options = []
for letter, val in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver.push()
    solver.add(days_at_most_2 == val)
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