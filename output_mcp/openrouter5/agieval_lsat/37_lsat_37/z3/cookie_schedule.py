from z3 import *

# We have 3 kinds: oatmeal (O), peanut butter (P), sugar (S)
# Each kind has 3 batches (first, second, third)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

# We'll encode each batch's day as an integer 0-4
# Variables: O1, O2, O3, P1, P2, P3, S1, S2, S3

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Domain: each batch day is Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Exactly three batches of each kind, each on a single day (already encoded)

# Condition 1: No two batches of the same kind are made on the same day.
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# Condition 2: At least one batch of cookies is made on Monday.
solver.add(Or([b == 0 for b in all_batches]))

# Condition 3: The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies.
solver.add(O2 == P1)

# Condition 4: The second batch of sugar cookies is made on Thursday.
solver.add(S2 == 3)  # Thursday = 3

# Now define each option as a constraint that the schedule matches exactly.
# Each option gives a list of days for oatmeal, peanut butter, sugar.

# Option A: oatmeal: Monday(0), Wednesday(2), Thursday(3) | peanut butter: Wednesday(2), Thursday(3), Friday(4) | sugar: Monday(0), Thursday(3), Friday(4)
opt_a = And(
    Or([And(O1==0, O2==2, O3==3), And(O1==0, O2==3, O3==2), And(O1==2, O2==0, O3==3), And(O1==2, O2==3, O3==0), And(O1==3, O2==0, O3==2), And(O1==3, O2==2, O3==0)]),
    Or([And(P1==2, P2==3, P3==4), And(P1==2, P2==4, P3==3), And(P1==3, P2==2, P3==4), And(P1==3, P2==4, P3==2), And(P1==4, P2==2, P3==3), And(P1==4, P2==3, P3==2)]),
    Or([And(S1==0, S2==3, S3==4), And(S1==0, S2==4, S3==3), And(S1==3, S2==0, S3==4), And(S1==3, S2==4, S3==0), And(S1==4, S2==0, S3==3), And(S1==4, S2==3, S3==0)])
)

# Option B: oatmeal: Monday(0), Tuesday(1), Thursday(3) | peanut butter: Tuesday(1), Wednesday(2), Thursday(3) | sugar: Monday(0), Wednesday(2), Thursday(3)
opt_b = And(
    Or([And(O1==0, O2==1, O3==3), And(O1==0, O2==3, O3==1), And(O1==1, O2==0, O3==3), And(O1==1, O2==3, O3==0), And(O1==3, O2==0, O3==1), And(O1==3, O2==1, O3==0)]),
    Or([And(P1==1, P2==2, P3==3), And(P1==1, P2==3, P3==2), And(P1==2, P2==1, P3==3), And(P1==2, P2==3, P3==1), And(P1==3, P2==1, P3==2), And(P1==3, P2==2, P3==1)]),
    Or([And(S1==0, S2==2, S3==3), And(S1==0, S2==3, S3==2), And(S1==2, S2==0, S3==3), And(S1==2, S2==3, S3==0), And(S1==3, S2==0, S3==2), And(S1==3, S2==2, S3==0)])
)

# Option C: oatmeal: Tuesday(1), Wednesday(2), Thursday(3) | peanut butter: Wednesday(2), Thursday(3), Friday(4) | sugar: Tuesday(1), Thursday(3), Friday(4)
opt_c = And(
    Or([And(O1==1, O2==2, O3==3), And(O1==1, O2==3, O3==2), And(O1==2, O2==1, O3==3), And(O1==2, O2==3, O3==1), And(O1==3, O2==1, O3==2), And(O1==3, O2==2, O3==1)]),
    Or([And(P1==2, P2==3, P3==4), And(P1==2, P2==4, P3==3), And(P1==3, P2==2, P3==4), And(P1==3, P2==4, P3==2), And(P1==4, P2==2, P3==3), And(P1==4, P2==3, P3==2)]),
    Or([And(S1==1, S2==3, S3==4), And(S1==1, S2==4, S3==3), And(S1==3, S2==1, S3==4), And(S1==3, S2==4, S3==1), And(S1==4, S2==1, S3==3), And(S1==4, S2==3, S3==1)])
)

# Option D: oatmeal: Monday(0), Tuesday(1), Thursday(3) | peanut butter: Monday(0), Wednesday(2), Thursday(3) | sugar: Monday(0), Thursday(3), Friday(4)
opt_d = And(
    Or([And(O1==0, O2==1, O3==3), And(O1==0, O2==3, O3==1), And(O1==1, O2==0, O3==3), And(O1==1, O2==3, O3==0), And(O1==3, O2==0, O3==1), And(O1==3, O2==1, O3==0)]),
    Or([And(P1==0, P2==2, P3==3), And(P1==0, P2==3, P3==2), And(P1==2, P2==0, P3==3), And(P1==2, P2==3, P3==0), And(P1==3, P2==0, P3==2), And(P1==3, P2==2, P3==0)]),
    Or([And(S1==0, S2==3, S3==4), And(S1==0, S2==4, S3==3), And(S1==3, S2==0, S3==4), And(S1==3, S2==4, S3==0), And(S1==4, S2==0, S3==3), And(S1==4, S2==3, S3==0)])
)

# Option E: oatmeal: Monday(0), Thursday(3), Friday(4) | peanut butter: Tuesday(1), Wednesday(2), Thursday(3) | sugar: Monday(0), Thursday(3), Friday(4)
opt_e = And(
    Or([And(O1==0, O2==3, O3==4), And(O1==0, O2==4, O3==3), And(O1==3, O2==0, O3==4), And(O1==3, O2==4, O3==0), And(O1==4, O2==0, O3==3), And(O1==4, O2==3, O3==0)]),
    Or([And(P1==1, P2==2, P3==3), And(P1==1, P2==3, P3==2), And(P1==2, P2==1, P3==3), And(P1==2, P2==3, P3==1), And(P1==3, P2==1, P3==2), And(P1==3, P2==2, P3==1)]),
    Or([And(S1==0, S2==3, S3==4), And(S1==0, S2==4, S3==3), And(S1==3, S2==0, S3==4), And(S1==3, S2==4, S3==0), And(S1==4, S2==0, S3==3), And(S1==4, S2==3, S3==0)])
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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