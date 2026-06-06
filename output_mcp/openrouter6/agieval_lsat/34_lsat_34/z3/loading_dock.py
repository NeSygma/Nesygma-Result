from z3 import *

solver = Solver()

# Declare variables for each cargo's bay number (1 to 6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

# All bays are distinct and within 1..6
all_cargos = [fuel, grain, livestock, machinery, produce, textiles]
solver.add([And(1 <= c, c <= 6) for c in all_cargos])
solver.add(Distinct(all_cargos))

# Base constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce - 1, textiles == produce + 1))

# Define options as constraints
opt_a = Or(fuel == machinery - 1, fuel == machinery + 1)
opt_b = Or(grain == machinery - 1, grain == machinery + 1)
opt_c = Or(livestock == fuel - 1, livestock == fuel + 1)
opt_d = Or(produce == livestock - 1, produce == livestock + 1)
opt_e = Or(textiles == fuel - 1, textiles == fuel + 1)

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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