from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Days: Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4)
# Cookie types: Oatmeal(0), PeanutButter(1), Sugar(2)
# Batches: 0 (first), 1 (second), 2 (third)

solver = Solver()

# Declare variables
# batch_day[type][batch] = day (0-4)
batch_day = [[Int(f"batch_day_{t}_{b}") for b in range(3)] for t in range(3)]

# day_batch_count[day] = number of batches on that day
day_batch_count = [Int(f"day_batch_count_{d}") for d in range(5)]

# day_has_batch[day] = whether at least one batch is made on that day
day_has_batch = [Bool(f"day_has_batch_{d}") for d in range(5)]

# Helper: All batches of a type are on distinct days
for t in range(3):
    for b1 in range(3):
        for b2 in range(b1+1, 3):
            solver.add(batch_day[t][b1] != batch_day[t][b2])

# All batches are on days 0-4 (Monday-Friday)
for t in range(3):
    for b in range(3):
        solver.add(batch_day[t][b] >= 0, batch_day[t][b] <= 4)

# At least one batch is made on Monday (day 0)
solver.add(Or([batch_day[t][b] == 0 for t in range(3) for b in range(3)]))

# The second batch of oatmeal (batch 1) is made on the same day as the first batch of peanut butter (batch 0)
solver.add(batch_day[0][1] == batch_day[1][0])

# The second batch of sugar (batch 1) is made on Thursday (day 3)
solver.add(batch_day[2][1] == 3)

# Additional condition: one kind's first batch is made on the same day as another kind's third batch
# There exist types t1, t2 such that batch_day[t1][0] == batch_day[t2][2]
solver.add(Or(
    batch_day[0][0] == batch_day[0][2],  # Oatmeal first = Oatmeal third (but batches must be distinct days, so this is impossible)
    batch_day[0][0] == batch_day[1][2],  # Oatmeal first = PeanutButter third
    batch_day[0][0] == batch_day[2][2],  # Oatmeal first = Sugar third
    batch_day[1][0] == batch_day[0][2],  # PeanutButter first = Oatmeal third
    batch_day[1][0] == batch_day[1][2],  # PeanutButter first = PeanutButter third (impossible)
    batch_day[1][0] == batch_day[2][2],  # PeanutButter first = Sugar third
    batch_day[2][0] == batch_day[0][2],  # Sugar first = Oatmeal third
    batch_day[2][0] == batch_day[1][2],  # Sugar first = PeanutButter third
    batch_day[2][0] == batch_day[2][2]   # Sugar first = Sugar third (impossible)
))

# Define day_batch_count and day_has_batch
for d in range(5):
    # day_batch_count[d] = number of batches on day d
    solver.add(day_batch_count[d] == Sum([If(batch_day[t][b] == d, 1, 0) for t in range(3) for b in range(3)]))
    # day_has_batch[d] = (day_batch_count[d] >= 1)
    solver.add(day_has_batch[d] == (day_batch_count[d] >= 1))

# Base constraints are now fully encoded

# Now evaluate each option to see if it could be false (i.e., its negation is satisfiable)

# Option A: At least one batch on each day
opt_a = And(day_has_batch[0], day_has_batch[1], day_has_batch[2], day_has_batch[3], day_has_batch[4])
# Negation: Not all days have at least one batch
neg_opt_a = Or(Not(day_has_batch[0]), Not(day_has_batch[1]), Not(day_has_batch[2]), Not(day_has_batch[3]), Not(day_has_batch[4]))

# Option B: At least two batches on Wednesday (day 2)
opt_b = (day_batch_count[2] >= 2)
# Negation: Less than two batches on Wednesday
neg_opt_b = (day_batch_count[2] < 2)

# Option C: Exactly one batch on Monday (day 0)
opt_c = (day_batch_count[0] == 1)
# Negation: Not exactly one batch on Monday
neg_opt_c = Not(opt_c)

# Option D: Exactly two batches on Tuesday (day 1)
opt_d = (day_batch_count[1] == 2)
# Negation: Not exactly two batches on Tuesday
neg_opt_d = Not(opt_d)

# Option E: Exactly one batch on Friday (day 4)
opt_e = (day_batch_count[4] == 1)
# Negation: Not exactly one batch on Friday
neg_opt_e = Not(opt_e)

# Now check which options could be false (i.e., their negations are satisfiable)
found_options = []

# Check option A
solver.push()
solver.add(neg_opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Check option B
solver.push()
solver.add(neg_opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Check option C
solver.push()
solver.add(neg_opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Check option D
solver.push()
solver.add(neg_opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Check option E
solver.push()
solver.add(neg_opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")