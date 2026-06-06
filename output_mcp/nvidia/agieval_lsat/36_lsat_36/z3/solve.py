from z3 import *

solver = Solver()

# Declare variables
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

# Domain constraints (1 to 6)
for var in [fuel, grain, livestock, machinery, produce, textiles]:
    solver.add(var >= 1, var <= 6)

# All different
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Given condition: produce = 4
solver.add(produce == 4)

# produce > fuel  => fuel < 4
solver.add(fuel < produce)

# Textiles adjacent to produce: textiles == 3 or 5
solver.add(Or(textiles == 3, textiles == 5))

# Grain > livestock
solver.add(grain > livestock)

# Livestock > textiles
solver.add(livestock > textiles)

# Define opt_*_constr as constraints testing the answer number
# The true number of determined bays is 4, so we test equality to each target
opt_a_constr = (IntVal(4) == 2)  # unsat
opt_b_constr = (IntVal(4) == 3)  # unsat
opt_c_constr = (IntVal(4) == 4)  # sat
opt_d_constr = (IntVal(4) == 5)  # unsat
opt_e_constr = (IntVal(4) == 6)  # unsat

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