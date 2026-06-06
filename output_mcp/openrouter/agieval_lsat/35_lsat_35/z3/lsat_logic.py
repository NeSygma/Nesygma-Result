from z3 import *

# Base constraints for the loading dock problem
solver = Solver()

# Variables: bay number for each cargo type (1..6)
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

# All different cargo types
solver.add(Distinct(vars))

# Given ordering constraints
solver.add(grains > livestock)          # grain > livestock
solver.add(livestock > textiles)       # livestock > textiles
solver.add(produce > fuel)             # produce > fuel
solver.add(Abs(textiles - produce) == 1)  # textiles adjacent to produce

# Additional condition for the conditional premise
solver.add(Abs(produce - livestock) == 1)  # produce adjacent to livestock

# Define option-specific constraints
opt_a_constr = (fuel == 2)          # Bay 2 holds fuel
opt_b_constr = (produce == 4)       # Bay 4 holds produce
opt_c_constr = (textiles == 4)      # Bay 4 holds textiles
opt_d_constr = (grains == 5)        # Bay 5 holds grain
opt_e_constr = (machinery == 5)     # Bay 5 holds machinery

found_sat = []
options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_sat.append(letter)
    solver.pop()

# Determine which option is NOT satisfiable (the EXCEPT answer)
all_letters = [letter for letter, _ in options]
found_unsat = [l for l in all_letters if l not in found_sat]

if len(found_unsat) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat[0]}")
elif len(found_unsat) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {found_unsat}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")