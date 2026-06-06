from z3 import *

solver = Solver()

# Declare integer variables for each cargo
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

# All different
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce + 1, textiles + 1 == produce))

# Option constraints
opt_a_constr = livestock == 1
opt_b_constr = livestock == 2
opt_c_constr = livestock == 3
opt_d_constr = livestock == 5
opt_e_constr = livestock == 6

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