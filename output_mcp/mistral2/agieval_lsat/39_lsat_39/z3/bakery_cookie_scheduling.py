from z3 import *

# Initialize solver
solver = Solver()

# Days: M=0, T=1, W=2, Th=3, F=4
days = [0, 1, 2, 3, 4]

# Batch variables: O1, O2, O3, P1, P2, P3, S1, S2, S3
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# All batch variables in a list for convenience
batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Constraints:
# 1. No two batches of the same kind are on the same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# 2. At least one batch is on Monday (day 0)
solver.add(Or([b == 0 for b in batches]))

# 3. O2 = P1 (same day)
solver.add(O2 == P1)

# 4. S2 = Thursday (day 3)
solver.add(S2 == 3)

# 5. P1 = Tuesday (day 1)
solver.add(P1 == 1)

# 6. All batches are within the 5 days
for b in batches:
    solver.add(Or([b == d for d in days]))

# Now, evaluate each option (A-E) to see if it is possible
found_options = []

# Option A: Two different kinds of cookie have their first batch made on Monday.
# This means: (O1 == 0) or (P1 == 0) or (S1 == 0) is true, and at least two of O1, P1, S1 are 0.
# But P1 is fixed to 1 (Tuesday), so only O1 or S1 can be 0.
# To satisfy "two different kinds", both O1 and S1 must be 0.
solver.push()
solver.add(Or(O1 == 0, S1 == 0))
solver.add(And(O1 == 0, S1 == 0))  # Both O1 and S1 are Monday
result_A = solver.check()
solver.pop()

if result_A == sat:
    found_options.append("A")

# Option B: Two different kinds of cookie have their first batch made on Tuesday.
# P1 is already Tuesday (day 1), so we need either O1 or S1 to also be Tuesday.
solver.push()
solver.add(Or(O1 == 1, S1 == 1))
result_B = solver.check()
solver.pop()

if result_B == sat:
    found_options.append("B")

# Option C: Two different kinds of cookie have their second batch made on Wednesday.
# This means two of O2, P2, S2 are Wednesday (day 2).
# S2 is fixed to Thursday (day 3), so only O2 and P2 can be Wednesday.
solver.push()
solver.add(Or(And(O2 == 2, P2 == 2), And(O2 == 2, S2 == 2), And(P2 == 2, S2 == 2)))
# Since S2 is fixed to 3, only O2 and P2 can be 2.
solver.add(Or(O2 == 2, P2 == 2))
solver.add(And(O2 == 2, P2 == 2))  # Both O2 and P2 are Wednesday
result_C = solver.check()
solver.pop()

if result_C == sat:
    found_options.append("C")

# Option D: Two different kinds of cookie have their second batch made on Thursday.
# S2 is fixed to Thursday (day 3), so we need either O2 or P2 to also be Thursday.
solver.push()
solver.add(Or(O2 == 3, P2 == 3))
result_D = solver.check()
solver.pop()

if result_D == sat:
    found_options.append("D")

# Option E: Two different kinds of cookie have their third batch made on Friday.
# This means two of O3, P3, S3 are Friday (day 4).
solver.push()
solver.add(Or(And(O3 == 4, P3 == 4), And(O3 == 4, S3 == 4), And(P3 == 4, S3 == 4)))
solver.add(And(O3 == 4, P3 == 4))  # Both O3 and P3 are Friday
result_E = solver.check()
solver.pop()

if result_E == sat:
    found_options.append("E")

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")