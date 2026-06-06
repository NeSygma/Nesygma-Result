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

# Re-reading the question more carefully:
# "How many of the days, Monday through Friday, are such that at most two batches 
# of cookies COULD be made on that day?"
# 
# "COULD be made" means: there EXISTS a valid arrangement where that day has at most 2 batches.
# So we need to count days where it's POSSIBLE to have <= 2 batches.
# 
# But wait - every day COULD have 0 batches (if we arrange things right), so that would give 5.
# That doesn't seem right either.
#
# Let me re-read: "at most two batches of cookies could be made on that day"
# This likely means: in the valid arrangement(s), which days are GUARANTEED to have at most 2?
# OR: which days MUST have at most 2 batches?
#
# Actually, I think the question is asking: considering all valid schedules,
# for how many days is it true that in EVERY valid schedule, that day has at most 2 batches?
# i.e., which days can NEVER have 3 batches?

days_cannot_have_3 = []
for d in range(5):
    # Check if there exists a model where day d has 3 batches
    s = Solver()
    # Add all base constraints
    for t in range(3):
        for b in range(3):
            s.add(batch[t][b] >= 0, batch[t][b] <= 4)
    for t in range(3):
        s.add(Distinct(batch[t][0], batch[t][1], batch[t][2]))
    s.add(Or([batch[t][b] == 0 for t in range(3) for b in range(3)]))
    s.add(batch[0][1] == batch[1][0])
    s.add(batch[2][1] == 3)
    
    # Add constraint that day d has exactly 3 batches
    s.add(Sum([If(batch[t][b] == d, 1, 0) for t in range(3) for b in range(3)]) == 3)
    
    if s.check() == unsat:
        days_cannot_have_3.append(d)
        print(f"Day {d}: CANNOT have 3 batches")
    else:
        print(f"Day {d}: CAN have 3 batches")

print(f"\nDays that cannot have 3 batches: {days_cannot_have_3}")
print(f"Count: {len(days_cannot_have_3)}")

count = len(days_cannot_have_3)
answer_map = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
if count in answer_map:
    print("STATUS: sat")
    print(f"answer:{answer_map[count]}")
else:
    print("STATUS: unsat")
    print(f"Refine: count={count} not in options")