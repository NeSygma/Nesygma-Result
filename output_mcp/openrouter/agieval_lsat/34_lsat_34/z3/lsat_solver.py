from z3 import *

# Base solver and constraints
solver = Solver()
# Variables for positions of each cargo type (1..6)
fuel = Int('fuel')
grains = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')
vars = [fuel, grains, livestock, machinery, produce, textiles]
# Domain constraints
for v in vars:
    solver.add(v >= 1, v <= 6)
# All distinct
solver.add(Distinct(vars))
# Given constraints
solver.add(grains > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Option constraints definitions
opt_a_constr = Or(fuel == machinery + 1, fuel == machinery - 1)  # A: fuel next to machinery
opt_b_constr = Or(grains == machinery + 1, grains == machinery - 1)  # B: grain next to machinery
opt_c_constr = Or(livestock == fuel + 1, livestock == fuel - 1)  # C: livestock next to fuel
opt_d_constr = Or(produce == livestock + 1, produce == livestock - 1)  # D: produce next to livestock
opt_e_constr = Or(textiles == fuel + 1, textiles == fuel - 1)  # E: textiles next to fuel

found_options = []
options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option must be false (i.e., unsat when added)
unsat_options = [letter for letter, _ in options if letter not in found_options]
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(found_options) == 1:
    # fallback: if exactly one option is possible, output it
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options possible {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options possible")