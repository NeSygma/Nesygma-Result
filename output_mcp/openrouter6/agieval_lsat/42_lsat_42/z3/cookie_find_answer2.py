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

# Helper to compute count of batches on a given day
def count_on_day(day):
    return Sum([If(v == day, 1, 0) for v in all_vars])

# Define negations of each option (corrected)
opt_a_neg = Or([count_on_day(d) == 0 for d in range(5)])
opt_b_neg = count_on_day(2) <= 1
opt_c_neg = count_on_day(0) >= 2  # since at least one already, negation is >=2
opt_d_neg = count_on_day(1) != 2
opt_e_neg = count_on_day(4) != 1

# Evaluate each option's negation
found_options = []
for letter, constr in [("A", opt_a_neg), ("B", opt_b_neg), ("C", opt_c_neg), ("D", opt_d_neg), ("E", opt_e_neg)]:
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