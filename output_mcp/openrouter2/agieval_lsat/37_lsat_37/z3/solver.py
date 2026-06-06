from z3 import *
solver = Solver()
# Variables for each batch in order
# Oatmeal batches
oatmeal0 = Int('oatmeal0')
oatmeal1 = Int('oatmeal1')
oatmeal2 = Int('oatmeal2')
# Peanut butter batches
peanut0 = Int('peanut0')
peanut1 = Int('peanut1')
peanut2 = Int('peanut2')
# Sugar batches
sugar0 = Int('sugar0')
sugar1 = Int('sugar1')
sugar2 = Int('sugar2')
# Domain constraints: days 0-4 (Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4)
for v in [oatmeal0, oatmeal1, oatmeal2, peanut0, peanut1, peanut2, sugar0, sugar1, sugar2]:
    solver.add(v >= 0, v <= 4)
# Distinctness within each kind
solver.add(Distinct(oatmeal0, oatmeal1, oatmeal2))
solver.add(Distinct(peanut0, peanut1, peanut2))
solver.add(Distinct(sugar0, sugar1, sugar2))
# At least one batch on Monday (day 0)
solver.add(Or(oatmeal0 == 0, oatmeal1 == 0, oatmeal2 == 0,
              peanut0 == 0, peanut1 == 0, peanut2 == 0,
              sugar0 == 0, sugar1 == 0, sugar2 == 0))
# Second oatmeal batch same day as first peanut butter batch
solver.add(oatmeal1 == peanut0)
# Second sugar batch on Thursday (day 3)
solver.add(sugar1 == 3)
# Option constraints
opt_a_constr = [oatmeal0 == 0, oatmeal1 == 2, oatmeal2 == 3,
                peanut0 == 2, peanut1 == 3, peanut2 == 4,
                sugar0 == 0, sugar1 == 3, sugar2 == 4]
opt_b_constr = [oatmeal0 == 0, oatmeal1 == 1, oatmeal2 == 3,
                peanut0 == 1, peanut1 == 2, peanut2 == 3,
                sugar0 == 0, sugar1 == 2, sugar2 == 3]
opt_c_constr = [oatmeal0 == 1, oatmeal1 == 2, oatmeal2 == 3,
                peanut0 == 2, peanut1 == 3, peanut2 == 4,
                sugar0 == 1, sugar1 == 3, sugar2 == 4]
opt_d_constr = [oatmeal0 == 0, oatmeal1 == 1, oatmeal2 == 3,
                peanut0 == 0, peanut1 == 2, peanut2 == 3,
                sugar0 == 0, sugar1 == 3, sugar2 == 4]
opt_e_constr = [oatmeal0 == 0, oatmeal1 == 3, oatmeal2 == 4,
                peanut0 == 1, peanut1 == 2, peanut2 == 3,
                sugar0 == 0, sugar1 == 3, sugar2 == 4]
# Evaluate options
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