from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# Batches: 1st, 2nd, 3rd for each type

solver = Solver()

# Variables: batch[type][batch_num] = day (0-4)
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

# Total batches = 9, distributed across 5 days
# Each day can have 0-3 batches (max 3 because 3 cookie types, each at most 1 per day)
# Actually, max per day is 3 (one from each type)

# Question: How many days have at most 2 batches?
days_at_most_2 = Int('days_at_most_2')
solver.add(days_at_most_2 == Sum([If(batches_per_day[d] <= 2, 1, 0) for d in range(5)]))

# Let's first find all valid models and see what days_at_most_2 values are possible
possible_values = set()
models = []
while solver.check() == sat:
    m = solver.model()
    val = m[days_at_most_2].as_long()
    possible_values.add(val)
    models.append(m)
    # Block this specific assignment
    solver.add(Or([batch[t][b] != m[batch[t][b]] for t in range(3) for b in range(3)]))

print(f"Possible values for days_at_most_2: {possible_values}")
print(f"Total valid models found: {len(models)}")

# Now test each answer option against ALL possible models
# The answer must be the value that is ALWAYS true (in every valid model)
# Since the question asks "how many days are such that at most two batches COULD be made"
# This means: in every valid arrangement, how many days have at most 2 batches?

# Actually, re-reading: "How many of the days, Monday through Friday, are such that 
# at most two batches of cookies could be made on that day?"
# This is asking: for how many days is it GUARANTEED that at most 2 batches are made?
# i.e., in ALL valid models, that day has <= 2 batches.

# Let's check each day
days_guaranteed_at_most_2 = []
for d in range(5):
    all_have_at_most_2 = True
    for m in models:
        val = m[batches_per_day[d]].as_long()
        if val > 2:
            all_have_at_most_2 = False
            break
    if all_have_at_most_2:
        days_guaranteed_at_most_2.append(d)

print(f"Days guaranteed to have at most 2 batches: {days_guaranteed_at_most_2}")
print(f"Count: {len(days_guaranteed_at_most_2)}")

# Map to answer
count = len(days_guaranteed_at_most_2)
answer_map = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
if count in answer_map:
    print("STATUS: sat")
    print(f"answer:{answer_map[count]}")
else:
    print("STATUS: unsat")
    print(f"Refine: count={count} not in options")