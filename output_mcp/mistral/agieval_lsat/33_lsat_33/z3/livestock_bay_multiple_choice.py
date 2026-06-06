from z3 import *

# Define cargo types as constants for clarity
fuel = 0
grain = 1
livestock = 2
machinery = 3
produce = 4
textiles = 5

# Create a solver
solver = Solver()

# bay_of[cargo] = bay number (1-6) for that cargo
bay_of = [Int(f"bay_of_{cargo}") for cargo in [fuel, grain, livestock, machinery, produce, textiles]]

# Each bay number is between 1 and 6
for b in bay_of:
    solver.add(b >= 1, b <= 6)

# All bays are distinct (each bay holds exactly one cargo type)
solver.add(Distinct(bay_of))

# Constraints from the problem
# 1. The bay holding grain has a higher number than the bay holding livestock
solver.add(bay_of[grain] > bay_of[livestock])

# 2. The bay holding livestock has a higher number than the bay holding textiles
solver.add(bay_of[livestock] > bay_of[textiles])

# 3. The bay holding produce has a higher number than the bay holding fuel
solver.add(bay_of[produce] > bay_of[fuel])

# 4. The bay holding textiles is next to the bay holding produce
solver.add(Or(bay_of[textiles] == bay_of[produce] - 1, bay_of[textiles] == bay_of[produce] + 1))

# Multiple-choice options: check which option for livestock bay is possible
found_options = []

# Option A: bay 1
solver.push()
solver.add(bay_of[livestock] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: bay 2
solver.push()
solver.add(bay_of[livestock] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: bay 3
solver.push()
solver.add(bay_of[livestock] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: bay 5
solver.push()
solver.add(bay_of[livestock] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: bay 6
solver.push()
solver.add(bay_of[livestock] == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")