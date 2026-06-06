from z3 import *

# Solver and base constraints
solver = Solver()

# Days: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri
# Variables for batches
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain constraints: each batch day in 0..4
for v in all_vars:
    solver.add(v >= 0, v <= 4)

# No two batches of same kind on same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday (day 0)
solver.add(Or([v == 0 for v in all_vars]))

# Second batch of oatmeal same day as first batch of peanut butter
solver.add(O2 == P1)

# Second batch of sugar is Thursday (day 3)
solver.add(S2 == 3)

# Compute number of batches per day
counts = []
for d in range(5):
    cnt = Sum([If(v == d, 1, 0) for v in all_vars])
    counts.append(cnt)

# Number of days with at most two batches
days_at_most_two = Sum([If(cnt <= 2, 1, 0) for cnt in counts])

# Define option constraints for each answer choice
opt_a_constr = (days_at_most_two == 1)
opt_b_constr = (days_at_most_two == 2)
opt_c_constr = (days_at_most_two == 3)
opt_d_constr = (days_at_most_two == 4)
opt_e_constr = (days_at_most_two == 5)

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