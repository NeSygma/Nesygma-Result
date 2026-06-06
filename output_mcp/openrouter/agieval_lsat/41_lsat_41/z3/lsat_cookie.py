from z3 import *

solver = Solver()
# Variables for batch days (1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri)
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain constraints
for v in all_vars:
    solver.add(v >= 1, v <= 5)

# No two batches of same kind on same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday (day 1)
solver.add(Or([v == 1 for v in all_vars]))

# O2 same day as P1
solver.add(O2 == P1)

# S2 is Thursday (day 4)
solver.add(S2 == 4)

# Exactly one batch on Friday (day 5)
friday_count = Sum([If(v == 5, 1, 0) for v in all_vars])
solver.add(friday_count == 1)

# Define option constraints
opt_a_constr = S1 == 1          # A: first sugar batch on Monday
opt_b_constr = O1 == 2          # B: first oatmeal batch on Tuesday
opt_c_constr = O3 == 5          # C: third oatmeal batch on Friday
opt_d_constr = P1 == 3          # D: first peanut butter batch on Wednesday
opt_e_constr = P2 == 2          # E: second peanut butter batch on Tuesday

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