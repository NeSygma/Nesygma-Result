from z3 import *

solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Three kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches: batch 1, 2, 3

# Variables: day for each batch of each kind
O1, O2, O3 = Ints('O1 O2 O3')  # Oatmeal batches 1,2,3
P1, P2, P3 = Ints('P1 P2 P3')  # Peanut Butter batches 1,2,3
S1, S2, S3 = Ints('S1 S2 S3')  # Sugar batches 1,2, S3)

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Each batch is made on a day 0-4 (Monday-Friday)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday (day 0)
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal is made on the same day as the first batch of peanut butter
solver.add(O2 == P1)

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(S2 == 3)

# The number of batches made on Friday (day 4) is exactly one
solver.add(Sum([If(b == 4, 1, 0) for b in all_batches]) == 1)

# Define option constraints
opt_a_constr = (S1 == 0)  # First batch of sugar on Monday
opt_b_constr = (O1 == 1)  # First batch of oatmeal on Tuesday
opt_c_constr = (O3 == 4)  # Third batch of oatmeal on Friday
opt_d_constr = (P1 == 2)  # First batch of peanut butter on Wednesday
opt_e_constr = (P2 == 1)  # Second batch of peanut butter on Tuesday

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