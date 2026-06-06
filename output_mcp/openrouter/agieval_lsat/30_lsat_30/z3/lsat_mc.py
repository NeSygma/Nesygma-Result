from z3 import *

# Define solver and base constraints
solver = Solver()
# Position variables for each cargo type
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')
positions = [fuel, grain, livestock, machinery, produce, textiles]
# Domain 1..6
for p in positions:
    solver.add(p >= 1, p <= 6)
# All distinct
solver.add(Distinct(positions))
# Given constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(produce == textiles + 1, textiles == produce + 1))

# Option constraints
opt_a_constr = [fuel == 1, machinery == 2, textiles == 3]
opt_b_constr = [grain == 1, machinery == 2, fuel == 3]
opt_c_constr = [machinery == 1, livestock == 2, fuel == 3]
opt_d_constr = [machinery == 1, textiles == 2, fuel == 3]
opt_e_constr = [machinery == 1, textiles == 2, produce == 3]

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