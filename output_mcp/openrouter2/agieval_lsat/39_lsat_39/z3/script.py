from z3 import *

solver = Solver()

# Variables
day_O1, day_O2, day_O3 = Ints('day_O1 day_O2 day_O3')
day_P1, day_P2, day_P3 = Ints('day_P1 day_P2 day_P3')
day_S1, day_S2, day_S3 = Ints('day_S1 day_S2 day_S3')

# Domain constraints
for d in [day_O1, day_O2, day_O3, day_P1, day_P2, day_P3, day_S1, day_S2, day_S3]:
    solver.add(d >= 0, d <= 4)

# Distinctness per kind
solver.add(Distinct(day_O1, day_O2, day_O3))
solver.add(Distinct(day_P1, day_P2, day_P3))
solver.add(Distinct(day_S1, day_S2, day_S3))

# At least one batch on Monday
solver.add(Or(day_O1 == 0, day_O2 == 0, day_O3 == 0,
              day_P1 == 0, day_P2 == 0, day_P3 == 0,
              day_S1 == 0, day_S2 == 0, day_S3 == 0))

# Second batch of oatmeal same day as first batch of peanut butter
solver.add(day_O2 == day_P1)

# Second batch of sugar on Thursday
solver.add(day_S2 == 3)

# First batch of peanut butter on Tuesday
solver.add(day_P1 == 1)

# Option constraints
opt_a_constr = Sum([If(day_O1 == 0, 1, 0),
                    If(day_P1 == 0, 1, 0),
                    If(day_S1 == 0, 1, 0)]) >= 2

opt_b_constr = Sum([If(day_O1 == 1, 1, 0),
                    If(day_P1 == 1, 1, 0),
                    If(day_S1 == 1, 1, 0)]) >= 2

opt_c_constr = Sum([If(day_O2 == 2, 1, 0),
                    If(day_P2 == 2, 1, 0),
                    If(day_S2 == 2, 1, 0)]) >= 2

opt_d_constr = Sum([If(day_O2 == 3, 1, 0),
                    If(day_P2 == 3, 1, 0),
                    If(day_S2 == 3, 1, 0)]) >= 2

opt_e_constr = Sum([If(day_O3 == 4, 1, 0),
                    If(day_P3 == 4, 1, 0),
                    If(day_S3 == 4, 1, 0)]) >= 2

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