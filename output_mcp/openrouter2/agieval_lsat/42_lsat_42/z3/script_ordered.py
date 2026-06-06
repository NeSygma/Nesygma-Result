from z3 import *

solver = Solver()
# Variables for each batch day
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
# Domain constraints: days 0-4
for v in all_vars:
    solver.add(v >= 0, v <= 4)
# Distinct batches of same kind on same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))
# Ordering constraints: first < second < third for each kind
solver.add(O1 < O2, O2 < O3)
solver.add(P1 < P2, P2 < P3)
solver.add(S1 < S2, S2 < S3)
# At least one batch on Monday
solver.add(Or([v == 0 for v in all_vars]))
# Second batch of oatmeal same day as first batch of peanut butter
solver.add(O2 == P1)
# Second batch of sugar on Thursday
solver.add(S2 == 3)
# Assumption: one kind's first batch same day as another kind's third batch
assumption = Or(
    O1 == P3,
    O1 == S3,
    P1 == O3,
    P1 == S3,
    S1 == O3,
    S1 == P3
)
solver.add(assumption)

# Helper to count batches on a given day

def count_day(d):
    return Sum([If(v == d, 1, 0) for v in all_vars])

# Define negations of each answer choice
opt_a_constr = Not(And([Or([v == d for v in all_vars]) for d in range(5)]))  # some day has no batch
opt_b_constr = count_day(2) <= 1  # Wednesday has <=1 batch
opt_c_constr = count_day(0) != 1  # Monday not exactly one batch
opt_d_constr = count_day(1) != 2  # Tuesday not exactly two batches
opt_e_constr = count_day(4) != 1  # Friday not exactly one batch

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