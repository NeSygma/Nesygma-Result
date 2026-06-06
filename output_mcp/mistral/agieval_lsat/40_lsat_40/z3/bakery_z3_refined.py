from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# Batches: 0,1,2 for each type

# Declare variables: batch_day[type][batch] = day
batch_day = [[Int(f"batch_day_{t}_{b}") for b in range(3)] for t in range(3)]

solver = Solver()

# Helper: All batches of the same type must be on distinct days
for t in range(3):
    for b1 in range(3):
        for b2 in range(b1+1, 3):
            solver.add(batch_day[t][b1] != batch_day[t][b2])

# At least one batch on Monday (day 0)
solver.add(Or([batch_day[t][b] == 0 for t in range(3) for b in range(3)]))

# Second batch of oatmeal (type 0, batch 1) is on the same day as first batch of peanut butter (type 1, batch 0)
solver.add(batch_day[0][1] == batch_day[1][0])

# Second batch of sugar (type 2, batch 1) is on Thursday (day 3)
solver.add(batch_day[2][1] == 3)

# No batch is made on Wednesday (day 2) — all batch days must not be 2
for t in range(3):
    for b in range(3):
        solver.add(batch_day[t][b] != 2)

# Additional constraint: Each kind has exactly three batches, each on a distinct day
# This is already enforced by the distinctness constraint above.

# Base constraints are now set. Now evaluate each option.

# Option A: Exactly three batches of cookies are made on Tuesday (day 1)
# Count batches on Tuesday
count_tue_A = Sum([If(batch_day[t][b] == 1, 1, 0) for t in range(3) for b in range(3)])
opt_a_constr = (count_tue_A == 3)

# Option B: Exactly three batches of cookies are made on Friday (day 4)
count_fri_B = Sum([If(batch_day[t][b] == 4, 1, 0) for t in range(3) for b in range(3)])
opt_b_constr = (count_fri_B == 3)

# Option C: At least two batches of cookies are made on Monday (day 0)
count_mon_C = Sum([If(batch_day[t][b] == 0, 1, 0) for t in range(3) for b in range(3)])
opt_c_constr = (count_mon_C >= 2)

# Option D: At least two batches of cookies are made on Thursday (day 3)
count_thu_D = Sum([If(batch_day[t][b] == 3, 1, 0) for t in range(3) for b in range(3)])
opt_d_constr = (count_thu_D >= 2)

# Option E: Fewer batches of cookies are made on Monday than on Tuesday
count_mon_E = Sum([If(batch_day[t][b] == 0, 1, 0) for t in range(3) for b in range(3)])
count_tue_E = Sum([If(batch_day[t][b] == 1, 1, 0) for t in range(3) for b in range(3)])
opt_e_constr = (count_mon_E < count_tue_E)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        model = solver.model()
        print(f"Option {letter} is SAT with model:")
        for t in range(3):
            for b in range(3):
                print(f"  batch_day[{t}][{b}] = {model[batch_day[t][b]]}")
        print(f"  Count Monday: {model.eval(count_mon_C)}")
        print(f"  Count Tuesday: {model.eval(count_tue_A)}")
        print(f"  Count Thursday: {model.eval(count_thu_D)}")
        print(f"  Count Friday: {model.eval(count_fri_B)}")
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