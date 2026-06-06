from z3 import *

solver = Solver()

# Declare variables for each cargo type's bay number
grain = Int('grain')
livestock = Int('livestock')
textiles = Int('textiles')
produce = Int('produce')
fuel = Int('fuel')
machinery = Int('machinery')

# Base constraints: each bay number between 1 and 6
solver.add(1 <= grain, grain <= 6)
solver.add(1 <= livestock, livestock <= 6)
solver.add(1 <= textiles, textiles <= 6)
solver.add(1 <= produce, produce <= 6)
solver.add(1 <= fuel, fuel <= 6)
solver.add(1 <= machinery, machinery <= 6)

# All cargo types are in distinct bays
solver.add(Distinct([grain, livestock, textiles, produce, fuel, machinery]))

# Given ordering constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Abs(textiles - produce) == 1)  # next to each other

# Define options as constraints for bays 1,2,3
# Option A: fuel, machinery, textiles
opt_a = And(fuel == 1, machinery == 2, textiles == 3)
# Option B: grain, machinery, fuel
opt_b = And(grain == 1, machinery == 2, fuel == 3)
# Option C: machinery, livestock, fuel
opt_c = And(machinery == 1, livestock == 2, fuel == 3)
# Option D: machinery, textiles, fuel
opt_d = And(machinery == 1, textiles == 2, fuel == 3)
# Option E: machinery, textiles, produce
opt_e = And(machinery == 1, textiles == 2, produce == 3)

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