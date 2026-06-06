from z3 import *

solver = Solver()

# Variables: each cargo type maps to a bay number (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Each cargo is in a bay 1-6
for c in cargos:
    solver.add(And(c >= 1, c <= 6))

# All different bays
solver.add(Distinct(cargos))

# Constraint 1: grain > livestock
solver.add(grain > livestock)

# Constraint 2: livestock > textiles
solver.add(livestock > textiles)

# Constraint 3: produce > fuel
solver.add(produce > fuel)

# Constraint 4: textiles is next to produce (difference of 1)
solver.add(Abs(textiles - produce) == 1)

# Now test each option for livestock
found_options = []

# Option A: livestock == 1
solver.push()
solver.add(livestock == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: livestock == 2
solver.push()
solver.add(livestock == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: livestock == 3
solver.push()
solver.add(livestock == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: livestock == 5
solver.push()
solver.add(livestock == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: livestock == 6
solver.push()
solver.add(livestock == 6)
if solver.check() == sat:
    found_options.append("E")
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