from z3 import *

solver = Solver()

# Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
# Kinds: Oatmeal=0, Peanut Butter=1, Sugar=2
NUM_DAYS = 5
NUM_KINDS = 3
NUM_BATCHES = 3

# batch[kind][batch_num] = day (0-4)
batch = [[Int(f"b_{k}_{b}") for b in range(NUM_BATCHES)] for k in range(NUM_KINDS)]

for k in range(NUM_KINDS):
    for b in range(NUM_BATCHES):
        solver.add(batch[k][b] >= 0, batch[k][b] < NUM_DAYS)

# 1. No two batches of the same kind on the same day
for k in range(NUM_KINDS):
    solver.add(Distinct(batch[k]))

# 2. Chronological order: 1st batch before 2nd before 3rd
for k in range(NUM_KINDS):
    solver.add(batch[k][0] < batch[k][1])
    solver.add(batch[k][1] < batch[k][2])

# 3. At least one batch on Monday
solver.add(Or([batch[k][b] == 0 for k in range(NUM_KINDS) for b in range(NUM_BATCHES)]))

# 4. Second oatmeal = first peanut butter
solver.add(batch[0][1] == batch[1][0])

# 5. Second sugar on Thursday (day 3)
solver.add(batch[2][1] == 3)

# CONDITION: one kind's first batch is made on the same day as another kind's third batch
cond = Or([And(k1 != k2, batch[k1][0] == batch[k2][2]) for k1 in range(NUM_KINDS) for k2 in range(NUM_KINDS)])
solver.add(cond)

def count_day(day):
    return Sum([If(batch[k][b] == day, 1, 0) for k in range(NUM_KINDS) for b in range(NUM_BATCHES)])

# Option A: At least one batch on each of the five days
opt_a = And([count_day(d) >= 1 for d in range(NUM_DAYS)])

# Option B: At least two batches on Wednesday (day 2)
opt_b = count_day(2) >= 2

# Option C: Exactly one batch on Monday (day 0)
opt_c = count_day(0) == 1

# Option D: Exactly two batches on Tuesday (day 1)
opt_d = count_day(1) == 2

# Option E: Exactly one batch on Friday (day 4)
opt_e = count_day(4) == 1

# The question asks: "which one could be false?"
# We need to find the option that CAN be false (i.e., there exists a model where the option's statement is false)
# And the other options CANNOT be false (they must be true).

# So we test each option's NEGATION for satisfiability.
# If negation is SAT, the option COULD be false.
# If negation is UNSAT, the option must be true (CANNOT be false).

found = []
for letter, opt in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(opt))  # can this option be false?
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")