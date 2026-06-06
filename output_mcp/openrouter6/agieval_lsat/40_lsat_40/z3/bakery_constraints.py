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

# Additional condition: no batch on Wednesday (already enforced by domain)

# Now define option constraints
# Count functions
def count_day(day):
    return Sum([If(v == day, 1, 0) for v in all_vars])

count_mon = count_day(Mon)
count_tue = count_day(Tue)
count_thu = count_day(Thu)
count_fri = count_day(Fri)

# Option A: Exactly three batches on Tuesday
opt_a = (count_tue == 3)
# Option B: Exactly three batches on Friday
opt_b = (count_fri == 3)
# Option C: At least two batches on Monday
opt_c = (count_mon >= 2)
# Option D: At least two batches on Thursday
opt_d = (count_thu >= 2)
# Option E: Fewer batches on Monday than on Tuesday
opt_e = (count_mon < count_tue)

# Now check which options must be true (i.e., negation unsatisfiable)
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

# Output according to skeleton logic (but for necessity)
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")