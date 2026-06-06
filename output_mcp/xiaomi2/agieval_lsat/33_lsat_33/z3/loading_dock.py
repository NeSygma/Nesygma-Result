from z3 import *

solver = Solver()

# Each cargo is assigned a bay number (1-6), all different
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# All bays 1-6, all different
for c in cargos:
    solver.add(And(c >= 1, c <= 6))
solver.add(Distinct(cargos))

# Constraints
solver.add(grain > livestock)       # grain has higher number than livestock
solver.add(livestock > textiles)    # livestock has higher number than textiles
solver.add(produce > fuel)          # produce has higher number than fuel
solver.add(Abs(textiles - produce) == 1)  # textiles is next to produce

# Test each option for livestock
found_options = []
for letter, constr in [("A", livestock == 1), ("B", livestock == 2), ("C", livestock == 3), ("D", livestock == 5), ("E", livestock == 6)]:
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