from z3 import *

solver = Solver()

# Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
# Kinds: Oatmeal=0, Peanut Butter=1, Sugar=2

# batch[kind][batch_num] = day, where batch_num: 0=1st, 1=2nd, 2=3rd
batch = [[Int(f"b_{k}_{b}") for b in range(3)] for k in range(3)]

for k in range(3):
    for b in range(3):
        solver.add(batch[k][b] >= 0, batch[k][b] <= 4)

# Constraint 1: No two batches of the same kind on the same day
for k in range(3):
    solver.add(Distinct(batch[k]))

# CRITICAL: chronological ordering - 1st before 2nd before 3rd
for k in range(3):
    solver.add(batch[k][0] < batch[k][1])
    solver.add(batch[k][1] < batch[k][2])

# Constraint 2: At least one batch on Monday (day 0)
solver.add(Or([batch[k][b] == 0 for k in range(3) for b in range(3)]))

# Constraint 3: Second oatmeal batch = first peanut butter batch
solver.add(batch[0][1] == batch[1][0])

# Constraint 4: Second sugar batch is on Thursday (day 3)
solver.add(batch[2][1] == 3)

# CONDITION: one kind's first batch = another kind's third batch (distinct kinds)
cond = Or([And(k1 != k2, batch[k1][0] == batch[k2][2]) for k1 in range(3) for k2 in range(3)])
solver.add(cond)

# Helper: count batches on a given day
def count_day(day):
    return Sum([If(batch[k][b] == day, 1, 0) for k in range(3) for b in range(3)])

# For each option, check if it COULD BE FALSE under the constraints.
# That is: does there exist a model where the option's statement is false?

# Option A false: some day has 0 batches
opt_a_false = Or([count_day(d) == 0 for d in range(5)])

# Option B false: less than 2 batches on Wednesday (day 2)
opt_b_false = count_day(2) < 2

# Option C false: not exactly 1 batch on Monday (day 0)
opt_c_false = count_day(0) != 1

# Option D false: not exactly 2 batches on Tuesday (day 1)
opt_d_false = count_day(1) != 2

# Option E false: not exactly 1 batch on Friday (day 4)
opt_e_false = count_day(4) != 1

found_options = []

for letter, constr in [("A", opt_a_false), ("B", opt_b_false), ("C", opt_c_false), ("D", opt_d_false), ("E", opt_e_false)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} CAN be false. Model:")
        kind_names = ["Oatmeal", "PeanutButter", "Sugar"]
        for k in range(3):
            for b in range(3):
                print(f"  {kind_names[k]} batch #{b+1} -> day {m[batch[k][b]]}")
        # Count per day
        for d in range(5):
            cnt = sum(1 for k in range(3) for b in range(3) if m[batch[k][b]].as_long() == d)
            print(f"  Day {d}: {cnt} batches")
    else:
        print(f"Option {letter} CANNOT be false (must be true)")
    solver.pop()

print(f"\nFound options that could be false: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")