from z3 import *

# Define days
Mon, Tue, Wed, Thu, Fri = 0, 1, 2, 3, 4

# Variables for each batch
O1, O2, O3, P1, P2, P3, S1, S2, S3 = Ints('O1 O2 O3 P1 P2 P3 S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Base constraints
# 1. Domain: days 0,1,3,4 (no Wednesday)
for v in all_vars:
    solver.add(Or(v == Mon, v == Tue, v == Thu, v == Fri))

# 2. No two batches of same kind on same day
solver.add(O1 != O2)
solver.add(O1 != O3)
solver.add(O2 != O3)
solver.add(P1 != P2)
solver.add(P1 != P3)
solver.add(P2 != P3)
solver.add(S1 != S2)
solver.add(S1 != S3)
solver.add(S2 != S3)

# 3. At least one batch on Monday
solver.add(Or([v == Mon for v in all_vars]))

# 4. Second batch of oatmeal same day as first batch of peanut butter
solver.add(O2 == P1)

# 5. Second batch of sugar on Thursday
solver.add(S2 == Thu)

# Find a model
if solver.check() == sat:
    m = solver.model()
    print("Model found:")
    for v in all_vars:
        print(f"{v} = {m[v]}")
    # Count per day
    counts = {Mon:0, Tue:0, Thu:0, Fri:0}
    for v in all_vars:
        day = m[v].as_long()
        counts[day] += 1
    print("\nCounts per day:")
    print(f"Monday: {counts[Mon]}")
    print(f"Tuesday: {counts[Tue]}")
    print(f"Thursday: {counts[Thu]}")
    print(f"Friday: {counts[Fri]}")
else:
    print("No model found")