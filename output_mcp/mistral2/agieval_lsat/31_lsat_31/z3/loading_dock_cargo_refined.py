from z3 import *

solver = Solver()

# Bays are numbered 1 through 6
bays = [1, 2, 3, 4, 5, 6]

# Cargo types
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']

# Assign each bay a unique cargo type
bay_to_cargo = [Int(f'bay_to_cargo_{i}') for i in bays]
solver.add(Distinct(bay_to_cargo))
for i, bay in enumerate(bays):
    solver.add(bay_to_cargo[i] >= 0, bay_to_cargo[i] < 6)

# Helper: cargo type index to name
cargo_to_index = {cargo: idx for idx, cargo in enumerate(cargo_types)}

# Constraints:
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(
    bay_to_cargo[cargo_to_index['grain']] > bay_to_cargo[cargo_to_index['livestock']]
)

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(
    bay_to_cargo[cargo_to_index['livestock']] > bay_to_cargo[cargo_to_index['textiles']]
)

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(
    bay_to_cargo[cargo_to_index['produce']] > bay_to_cargo[cargo_to_index['fuel']]
)

# 4. The bay holding textiles is next to the bay holding produce.
textiles_bay = bay_to_cargo[cargo_to_index['textiles']]
produce_bay = bay_to_cargo[cargo_to_index['produce']]
solver.add(Or(
    textiles_bay == produce_bay + 1,
    textiles_bay == produce_bay - 1
))

# Evaluate each option for bay 4
found_options = []

# Option A: grain in bay 4
solver.push()
solver.add(bay_to_cargo[3] == cargo_to_index['grain'])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: livestock in bay 4
solver.push()
solver.add(bay_to_cargo[3] == cargo_to_index['livestock'])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: machinery in bay 4
solver.push()
solver.add(bay_to_cargo[3] == cargo_to_index['machinery'])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: produce in bay 4
solver.push()
solver.add(bay_to_cargo[3] == cargo_to_index['produce'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: textiles in bay 4
solver.push()
solver.add(bay_to_cargo[3] == cargo_to_index['textiles'])
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