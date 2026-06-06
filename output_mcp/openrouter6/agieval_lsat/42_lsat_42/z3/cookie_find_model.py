from z3 import *

solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Variables for batches: O1,O2,O3 for oatmeal; P1,P2,P3 for peanut butter; S1,S2,S3 for sugar
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain constraints: each batch on a day 0..4
for v in all_vars:
    solver.add(v >= 0, v <= 4)

# Constraint 1: No two batches of the same kind on the same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# Constraint 2: At least one batch on Monday (day 0)
solver.add(Or([v == 0 for v in all_vars]))

# Constraint 3: Second oatmeal batch same day as first peanut butter batch
solver.add(O2 == P1)

# Constraint 4: Second sugar batch on Thursday (day 3)
solver.add(S2 == 3)

# Additional condition: One kind's first batch same day as another kind's third batch
solver.add(Or(
    O1 == P3,
    O1 == S3,
    P1 == O3,
    P1 == S3,
    S1 == O3,
    S1 == P3
))

# Find a model
if solver.check() == sat:
    m = solver.model()
    print("Found a model:")
    for v in all_vars:
        print(f"{v} = {m[v]}")
    # Compute counts per day
    counts = [0]*5
    for v in all_vars:
        day = m[v].as_long()
        counts[day] += 1
    print("Counts per day:", counts)
    # Check options
    print("Option A (at least one batch each day):", all(c > 0 for c in counts))
    print("Option B (at least two on Wednesday):", counts[2] >= 2)
    print("Option C (exactly one on Monday):", counts[0] == 1)
    print("Option D (exactly two on Tuesday):", counts[1] == 2)
    print("Option E (exactly one on Friday):", counts[4] == 1)
else:
    print("No model found")