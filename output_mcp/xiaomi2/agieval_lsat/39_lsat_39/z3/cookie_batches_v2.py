from z3 import *

solver = Solver()

# Variables: batch number (1,2,3) for each cookie type
# Day encoding: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
O_1, O_2, O_3 = Ints('O_1 O_2 O_3')
PB_1, PB_2, PB_3 = Ints('PB_1 PB_2 PB_3')
S_1, S_2, S_3 = Ints('S_1 S_2 S_3')

all_vars = [O_1, O_2, O_3, PB_1, PB_2, PB_3, S_1, S_2, S_3]

# Domain: each batch on a day 1-5
for v in all_vars:
    solver.add(v >= 1, v <= 5)

# No two batches of the same kind on the same day
solver.add(Distinct(O_1, O_2, O_3))
solver.add(Distinct(PB_1, PB_2, PB_3))
solver.add(Distinct(S_1, S_2, S_3))

# At least one batch on Monday
solver.add(Or([v == 1 for v in all_vars]))

# Second batch of oatmeal = first batch of peanut butter
solver.add(O_2 == PB_1)

# Second batch of sugar on Thursday
solver.add(S_2 == 4)

# Given: first batch of peanut butter on Tuesday
solver.add(PB_1 == 2)

# Define answer option constraints (what "could be true")
# (A) Two different kinds have first batch on Monday
opt_a = And(O_1 == 1, S_1 == 1)

# (B) Two different kinds have first batch on Tuesday
opt_b = (S_1 == 2)

# (C) Two different kinds have second batch on Wednesday
opt_c = And(PB_2 == 3, Or(O_2 == 3, S_2 == 3))

# (D) Two different kinds have second batch on Thursday
opt_d = (PB_2 == 4)

# (E) Two different kinds have third batch on Friday
opt_e = Or(
    And(O_3 == 5, PB_3 == 5),
    And(O_3 == 5, S_3 == 5),
    And(PB_3 == 5, S_3 == 5)
)

# For "EXCEPT" question: find which CANNOT be true (UNSAT)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
        print(f"Option {letter}: UNSAT (CANNOT be true)")
    else:
        print(f"Option {letter}: SAT (COULD be true)")
    solver.pop()

print()
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")