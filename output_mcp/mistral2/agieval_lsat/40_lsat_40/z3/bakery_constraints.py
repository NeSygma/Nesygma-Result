from z3 import *

# Initialize solver
solver = Solver()

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Batches: O1, O2, O3 (oatmeal), P1, P2, P3 (peanut butter), S1, S2, S3 (sugar)

# Declare variables for the day each batch is made
days = [Int(f'day_{cookie}') for cookie in ['O1', 'O2', 'O3', 'P1', 'P2', 'P3', 'S1', 'S2', 'S3']]

# Constraints:
# 1. No two batches of the same kind are made on the same day
solver.add(Distinct([days[0], days[1], days[2]]))  # O1, O2, O3
solver.add(Distinct([days[3], days[4], days[5]]))  # P1, P2, P3
solver.add(Distinct([days[6], days[7], days[8]]))  # S1, S2, S3

# 2. At least one batch is made on Monday (day=0)
solver.add(Or([d == 0 for d in days]))

# 3. O2 and P1 are on the same day
solver.add(days[1] == days[3])

# 4. S2 is on Thursday (day=3)
solver.add(days[7] == 3)

# 5. No batches on Wednesday (day=2)
solver.add(And([d != 2 for d in days]))

# Additional constraint: All batches must be on valid days (0-4)
for d in days:
    solver.add(d >= 0, d <= 4)

# Now, evaluate each answer choice
found_options = []

# (A) Exactly three batches of cookies are made on Tuesday (day=1)
solver.push()
solver.add(Sum([If(d == 1, 1, 0) for d in days]) == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Exactly three batches of cookies are made on Friday (day=4)
solver.push()
solver.add(Sum([If(d == 4, 1, 0) for d in days]) == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) At least two batches of cookies are made on Monday (day=0)
solver.push()
solver.add(Sum([If(d == 0, 1, 0) for d in days]) >= 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) At least two batches of cookies are made on Thursday (day=3)
solver.push()
solver.add(Sum([If(d == 3, 1, 0) for d in days]) >= 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Fewer batches of cookies are made on Monday than on Tuesday
solver.push()
solver.add(Sum([If(d == 0, 1, 0) for d in days]) < Sum([If(d == 1, 1, 0) for d in days]))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")