from z3 import *

solver = Solver()

# Bays are numbered 1 through 6
bays = [1, 2, 3, 4, 5, 6]

# Cargo types
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']

# Assign each cargo type to a unique bay
cargo_to_bay = {cargo: Int(f'cargo_to_bay_{cargo}') for cargo in cargo_types}

# Each bay must have exactly one cargo type
for bay in bays:
    solver.add(Or([cargo_to_bay[cargo] == bay for cargo in cargo_types]))

# Each cargo type must be assigned to exactly one bay
for cargo in cargo_types:
    solver.add(Or([cargo_to_bay[cargo] == bay for bay in bays]))

# Ensure all cargo types are assigned to distinct bays
solver.add(Distinct([cargo_to_bay[cargo] for cargo in cargo_types]))

# Constraints:
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(cargo_to_bay['grain'] > cargo_to_bay['livestock'])

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(cargo_to_bay['livestock'] > cargo_to_bay['textiles'])

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(cargo_to_bay['produce'] > cargo_to_bay['fuel'])

# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or(
    cargo_to_bay['textiles'] == cargo_to_bay['produce'] + 1,
    cargo_to_bay['textiles'] == cargo_to_bay['produce'] - 1
))

# Evaluate each option for bay 4
found_options = []

# Option A: grain in bay 4
solver.push()
solver.add(cargo_to_bay['grain'] == 4)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: livestock in bay 4
solver.push()
solver.add(cargo_to_bay['livestock'] == 4)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: machinery in bay 4
solver.push()
solver.add(cargo_to_bay['machinery'] == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: produce in bay 4
solver.push()
solver.add(cargo_to_bay['produce'] == 4)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: textiles in bay 4
solver.push()
solver.add(cargo_to_bay['textiles'] == 4)
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