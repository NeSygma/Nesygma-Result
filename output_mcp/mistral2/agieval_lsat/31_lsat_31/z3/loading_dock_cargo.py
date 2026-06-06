from z3 import *

solver = Solver()

# Declare the bays and cargo types
bays = [Int(f'bay_{i}') for i in range(1, 7)]  # bays 1 through 6
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']

# Each bay holds a different cargo type
solver.add(Distinct(bays))

# Helper function to ensure cargo types are assigned correctly
def cargo_constraint(cargo, bay):
    return And(bay == cargo_types.index(cargo) + 1)

# Constraints from the problem statement
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(Or([
    And(bays[i] == cargo_types.index('grain') + 1, bays[j] == cargo_types.index('livestock') + 1, bays[i] > bays[j])
    for i in range(6) for j in range(6) if i != j
]))

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(Or([
    And(bays[i] == cargo_types.index('livestock') + 1, bays[j] == cargo_types.index('textiles') + 1, bays[i] > bays[j])
    for i in range(6) for j in range(6) if i != j
]))

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(Or([
    And(bays[i] == cargo_types.index('produce') + 1, bays[j] == cargo_types.index('fuel') + 1, bays[i] > bays[j])
    for i in range(6) for j in range(6) if i != j
]))

# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or([
    And(bays[i] == cargo_types.index('textiles') + 1, bays[j] == cargo_types.index('produce') + 1, abs(i - j) == 1)
    for i in range(6) for j in range(6) if i != j
]))

# Ensure all bays are assigned a cargo type
for cargo in cargo_types:
    solver.add(Or([bays[i] == cargo_types.index(cargo) + 1 for i in range(6)]))

# Evaluate each option for bay 4
found_options = []

# Option A: grain in bay 4
solver.push()
solver.add(bays[3] == cargo_types.index('grain') + 1)  # bay 4 is index 3
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: livestock in bay 4
solver.push()
solver.add(bays[3] == cargo_types.index('livestock') + 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: machinery in bay 4
solver.push()
solver.add(bays[3] == cargo_types.index('machinery') + 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: produce in bay 4
solver.push()
solver.add(bays[3] == cargo_types.index('produce') + 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: textiles in bay 4
solver.push()
solver.add(bays[3] == cargo_types.index('textiles') + 1)
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