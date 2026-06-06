from z3 import *

solver = Solver()

# Variables: batch number (1,2,3) for each cookie type (O=Oatmeal, PB=PeanutButter, S=Sugar)
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

# From constraints: O_2 = PB_1 = 2
# So O_2 = 2, PB_1 = 2, S_2 = 4

# Define answer option constraints
# (A) Two different kinds have first batch on Monday
# First batches: O_1, PB_1, S_1. PB_1=2, so need O_1==1 AND S_1==1
opt_a = And(O_1 == 1, S_1 == 1)

# (B) Two different kinds have first batch on Tuesday
# PB_1=2 already. O_2=2 so O_1!=2. Need S_1==2.
opt_b = (S_1 == 2)

# (C) Two different kinds have second batch on Wednesday
# Second batches: O_2=2, S_2=4. Only PB_2 could be 3. Can't have two.
# So this requires at least two of {O_2, PB_2, S_2} == 3
# O_2=2 != 3, S_2=4 != 3, so only PB_2 could be 3 -> at most 1
opt_c = And(PB_2 == 3, Or(O_2 == 3, S_2 == 3))  # impossible given O_2=2, S_2=4

# (D) Two different kinds have second batch on Thursday
# S_2=4 already. O_2=2!=4. Need PB_2==4.
opt_d = (PB_2 == 4)

# (E) Two different kinds have third batch on Friday
# Need at least two of {O_3, PB_3, S_3} == 5
opt_e = Or(
    And(O_3 == 5, PB_3 == 5),
    And(O_3 == 5, S_3 == 5),
    And(PB_3 == 5, S_3 == 5)
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT -> O=({m[O_1]},{m[O_2]},{m[O_3]}), PB=({m[PB_1]},{m[PB_2]},{m[PB_3]}), S=({m[S_1]},{m[S_2]},{m[S_3]})")
    else:
        print(f"Option {letter}: UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")