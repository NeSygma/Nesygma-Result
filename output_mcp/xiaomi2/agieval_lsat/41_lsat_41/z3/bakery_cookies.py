from z3 import *

solver = Solver()

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Variables for each batch of each cookie type
O1, O2, O3 = Ints('O1 O2 O3')  # Oatmeal batches 1,2,3
P1, P2, P3 = Ints('P1 P2 P3')  # Peanut butter batches 1,2,3
S1, S2, S3 = Ints('S1 S2 S3')  # Sugar batches 1,2,3

all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Each batch is on a day 1-5
for v in all_vars:
    solver.add(And(v >= 1, v <= 5))

# No two batches of the same kind on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday
solver.add(Or([v == 1 for v in all_vars]))

# O2 == P1 (second oatmeal same day as first peanut butter)
solver.add(O2 == P1)

# S2 == 4 (second sugar on Thursday)
solver.add(S2 == 4)

# Exactly one batch on Friday
solver.add(Sum([If(v == 5, 1, 0) for v in all_vars]) == 1)

# Define option constraints
opt_a = (S1 == 1)  # First batch of sugar on Monday
opt_b = (O1 == 2)  # First batch of oatmeal on Tuesday
opt_c = (O3 == 5)  # Third batch of oatmeal on Friday
opt_d = (P1 == 3)  # First batch of peanut butter on Wednesday
opt_e = (P2 == 2)  # Second batch of peanut butter on Tuesday

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: O1={m[O1]},O2={m[O2]},O3={m[O3]},P1={m[P1]},P2={m[P2]},P3={m[P3]},S1={m[S1]},S2={m[S2]},S3={m[S3]}")
    else:
        print(f"Option {letter} is UNSAT")
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