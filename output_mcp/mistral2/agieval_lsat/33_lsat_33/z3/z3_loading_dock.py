from z3 import *

solver = Solver()

# Declare symbolic variables for each bay and cargo type
# Bays are numbered 1 through 6
bays = [Int(f'bay_{i}') for i in range(1, 7)]

# Cargo types
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
cargo = {c: Int(f'cargo_{c}') for c in cargo_types}

# Each bay holds a different cargo type
solver.add(Distinct(list(cargo.values())))

# Each cargo type is assigned to exactly one bay
for c in cargo_types:
    solver.add(Or([bays[i] == cargo[c] for i in range(6)]))

# The bay holding grain has a higher number than the bay holding livestock
solver.add(cargo['grain'] > cargo['livestock'])

# The bay holding livestock has a higher number than the bay holding textiles
solver.add(cargo['livestock'] > cargo['textiles'])

# The bay holding produce has a higher number than the bay holding fuel
solver.add(cargo['produce'] > cargo['fuel'])

# The bay holding textiles is next to the bay holding produce
# This means the absolute difference between their bay numbers is 1
solver.add(Or(
    cargo['textiles'] == cargo['produce'] + 1,
    cargo['textiles'] == cargo['produce'] - 1
))

# Base constraints for bays: they are numbered 1 through 6
for i in range(6):
    solver.add(bays[i] >= 1, bays[i] <= 6)

# Now evaluate the multiple choice options
found_options = []

# Option A: bay 1 holds livestock
solver.push()
solver.add(cargo['livestock'] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: bay 2 holds livestock
solver.push()
solver.add(cargo['livestock'] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: bay 3 holds livestock
solver.push()
solver.add(cargo['livestock'] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: bay 5 holds livestock
solver.push()
solver.add(cargo['livestock'] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: bay 6 holds livestock
solver.push()
solver.add(cargo['livestock'] == 6)
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