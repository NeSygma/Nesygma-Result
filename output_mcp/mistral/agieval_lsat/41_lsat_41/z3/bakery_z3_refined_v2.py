from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=Oatmeal, 1=PeanutButter, 2=Sugar
# Batches: 0=Batch1, 1=Batch2, 2=Batch3

solver = Solver()

# Decision variables: day for each batch of each kind
# batches[type][batch] = day
batches = [[Int(f"batch_{t}_{b}") for b in range(3)] for t in range(3)]

# Helper: Extract days for each type
O1, O2, O3 = batches[0]
P1, P2, P3 = batches[1]
S1, S2, S3 = batches[2]

# Domain: days are 0-4 (Monday-Friday)
days = range(5)
for t in range(3):
    for b in range(3):
        solver.add(batches[t][b] >= 0, batches[t][b] <= 4)

# No two batches of the same kind on the same day
for t in range(3):
    solver.add(Distinct(batches[t]))

# At least one batch is made on Monday (day 0)
solver.add(Or([batches[t][b] == 0 for t in range(3) for b in range(3)]))

# The second batch of oatmeal (O2) is made on the same day as the first batch of peanut butter (P1)
solver.add(O2 == P1)

# The second batch of sugar (S2) is made on Thursday (day 3)
solver.add(S2 == 3)

# The number of batches made on Friday (day 4) is exactly one
friday_batches = Sum([If(batches[t][b] == 4, 1, 0) for t in range(3) for b in range(3)])
solver.add(friday_batches == 1)

# Ensure that the Friday batch is the only one on that day
# This is already implied by the uniqueness constraints, but we can add it explicitly
# We will enforce that only one batch is on Friday by ensuring that all other batches are not on Friday
for t in range(3):
    for b in range(3):
        if not (t == 0 and b == 2):  # Allow O3 to be on Friday if needed
            solver.add(Implies(batches[t][b] == 4, And([batches[tt][bb] != 4 for tt in range(3) for bb in range(3) if not (tt == t and bb == b)])))

# Base constraints are set. Now evaluate each option.

# Option A: The first batch of sugar cookies is made on Monday (S1 == 0)
opt_a_constr = (S1 == 0)

# Option B: The first batch of oatmeal cookies is made on Tuesday (O1 == 1)
opt_b_constr = (O1 == 1)

# Option C: The third batch of oatmeal cookies is made on Friday (O3 == 4)
opt_c_constr = (O3 == 4)

# Option D: The first batch of peanut butter cookies is made on Wednesday (P1 == 2)
opt_d_constr = (P1 == 2)

# Option E: The second batch of peanut butter cookies is made on Tuesday (P2 == 1)
opt_e_constr = (P2 == 1)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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