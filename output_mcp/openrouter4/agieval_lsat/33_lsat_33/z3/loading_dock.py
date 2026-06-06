from z3 import *

solver = Solver()

# Create variables for each cargo type: the bay number (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargo_vars = [fuel, grain, livestock, machinery, produce, textiles]

# Domain constraints: each bay is 1-6
for v in cargo_vars:
    solver.add(v >= 1, v <= 6)

# All different
solver.add(Distinct(cargo_vars))

# Constraint 1: grain > livestock
solver.add(grain > livestock)

# Constraint 2: livestock > textiles
solver.add(livestock > textiles)

# Constraint 3: produce > fuel
solver.add(produce > fuel)

# Constraint 4: textiles is next to produce
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Now test each option for livestock
found_options = []
for letter, value in [("A", 1), ("B", 2), ("C", 3), ("D", 5), ("E", 6)]:
    solver.push()
    solver.add(livestock == value)
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