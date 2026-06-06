from z3 import *

# Base constraints for the loading dock problem
solver = Solver()

# Six bays, numbered 1 through 6
bay_numbers = [1, 2, 3, 4, 5, 6]

# Each bay holds a unique cargo
cargos = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# Assign a cargo to each bay
bay_to_cargo = [Int(f'bay_to_cargo_{i}') for i in range(1, 7)]
solver.add(Distinct(bay_to_cargo))

# Map cargo names to their assignments
cargo_to_bay = {cargo: Int(f'cargo_to_bay_{cargo}') for cargo in cargos}
for cargo in cargos:
    solver.add(cargo_to_bay[cargo] >= 1, cargo_to_bay[cargo] <= 6)
    solver.add(Or([bay_to_cargo[i] == cargo_to_bay[cargo] for i in range(6)]))

# Add constraints from the problem statement
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(cargo_to_bay["grain"] > cargo_to_bay["livestock"])

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(cargo_to_bay["livestock"] > cargo_to_bay["textiles"])

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(cargo_to_bay["produce"] > cargo_to_bay["fuel"])

# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or(
    cargo_to_bay["textiles"] == cargo_to_bay["produce"] + 1,
    cargo_to_bay["textiles"] == cargo_to_bay["produce"] - 1
))

# Now, evaluate each option to see which one fits the constraints for the first three bays
found_options = []

# Option A: fuel, machinery, textiles
solver.push()
solver.add(cargo_to_bay["fuel"] == 1)
solver.add(cargo_to_bay["machinery"] == 2)
solver.add(cargo_to_bay["textiles"] == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: grain, machinery, fuel
solver.push()
solver.add(cargo_to_bay["grain"] == 1)
solver.add(cargo_to_bay["machinery"] == 2)
solver.add(cargo_to_bay["fuel"] == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: machinery, livestock, fuel
solver.push()
solver.add(cargo_to_bay["machinery"] == 1)
solver.add(cargo_to_bay["livestock"] == 2)
solver.add(cargo_to_bay["fuel"] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: machinery, textiles, fuel
solver.push()
solver.add(cargo_to_bay["machinery"] == 1)
solver.add(cargo_to_bay["textiles"] == 2)
solver.add(cargo_to_bay["fuel"] == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: machinery, textiles, produce
solver.push()
solver.add(cargo_to_bay["machinery"] == 1)
solver.add(cargo_to_bay["textiles"] == 2)
solver.add(cargo_to_bay["produce"] == 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")