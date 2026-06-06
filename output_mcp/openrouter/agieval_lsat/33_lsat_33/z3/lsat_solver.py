from z3 import *

# Declare variables for each cargo type, representing the bay number (1..6)
grain = Int('grain')
livestock = Int('livestock')
textiles = Int('textiles')
produce = Int('produce')
fuel = Int('fuel')
machinery = Int('machinery')

solver = Solver()
# Domain constraints: each bay number between 1 and 6
vars = [grain, livestock, textiles, produce, fuel, machinery]
for v in vars:
    solver.add(v >= 1, v <= 6)
# All different cargo types occupy distinct bays
solver.add(Distinct(vars))
# Given relational constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Define option constraints for each answer choice
opt_a_constr = (livestock == 1)
opt_b_constr = (livestock == 2)
opt_c_constr = (livestock == 3)
opt_d_constr = (livestock == 5)
opt_e_constr = (livestock == 6)

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