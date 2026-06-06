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

# 6. All batches must be on valid days (0-4)
for d in days:
    solver.add(d >= 0, d <= 4)

# 7. Ensure that the total number of batches per day does not exceed 3
for day in range(5):
    solver.add(Sum([If(d == day, 1, 0) for d in days]) <= 3)

# Now, evaluate each answer choice with stricter constraints
found_options = []

# (A) Exactly three batches of cookies are made on Tuesday (day=1)
# and no other day has three batches
solver.push()
count_tue = Sum([If(d == 1, 1, 0) for d in days])
solver.add(count_tue == 3)
for day in [0, 3, 4]:  # Exclude Wednesday (day=2) as it has no batches
    solver.add(Sum([If(d == day, 1, 0) for d in days]) != 3)
if solver.check() == sat:
    found_options.append("A")
    model_A = solver.model()
solver.pop()

# (B) Exactly three batches of cookies are made on Friday (day=4)
# and no other day has three batches
solver.push()
count_fri = Sum([If(d == 4, 1, 0) for d in days])
solver.add(count_fri == 3)
for day in [0, 1, 3]:  # Exclude Wednesday (day=2) as it has no batches
    solver.add(Sum([If(d == day, 1, 0) for d in days]) != 3)
if solver.check() == sat:
    found_options.append("B")
    model_B = solver.model()
solver.pop()

# (C) At least two batches of cookies are made on Monday (day=0)
# and no other constraint is enforced (since it's not an exact count)
solver.push()
count_mon = Sum([If(d == 0, 1, 0) for d in days])
solver.add(count_mon >= 2)
if solver.check() == sat:
    found_options.append("C")
    model_C = solver.model()
solver.pop()

# (D) At least two batches of cookies are made on Thursday (day=3)
# and no other constraint is enforced
solver.push()
count_thu = Sum([If(d == 3, 1, 0) for d in days])
solver.add(count_thu >= 2)
if solver.check() == sat:
    found_options.append("D")
    model_D = solver.model()
solver.pop()

# (E) Fewer batches of cookies are made on Monday than on Tuesday
solver.push()
count_mon = Sum([If(d == 0, 1, 0) for d in days])
count_tue = Sum([If(d == 1, 1, 0) for d in days])
solver.add(count_mon < count_tue)
if solver.check() == sat:
    found_options.append("E")
    model_E = solver.model()
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
    # Print models for debugging
    print("\nModel for A:")
    for d in days:
        print(f"{d} = {model_A[d]}")
    print("\nModel for B:")
    for d in days:
        print(f"{d} = {model_B[d]}")
    print("\nModel for C:")
    for d in days:
        print(f"{d} = {model_C[d]}")
    print("\nModel for D:")
    for d in days:
        print(f"{d} = {model_D[d]}")
    print("\nModel for E:")
    for d in days:
        print(f"{d} = {model_E[d]}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")