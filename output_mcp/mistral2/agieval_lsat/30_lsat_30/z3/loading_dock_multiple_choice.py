from z3 import *

# Base constraints for the loading dock problem
solver = Solver()

# Six bays, each with a unique cargo
bays = [Int(f'bay_{i}') for i in range(1, 7)]

# Each bay holds a distinct cargo
cargos = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]
solver.add(Distinct(bays))

# Encode cargo assignments as values 0-5 for simplicity
# We'll map these to the actual cargo names later
cargo_values = {cargo: i for i, cargo in enumerate(cargos)}

# Add constraints from the problem statement
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(bays[cargo_values["grain"]] > bays[cargo_values["livestock"]])

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(bays[cargo_values["livestock"]] > bays[cargo_values["textiles"]])

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(bays[cargo_values["produce"]] > bays[cargo_values["fuel"]])

# 4. The bay holding textiles is next to the bay holding produce.
# This means the absolute difference between their bay numbers is 1.
solver.add(Or(
    bays[cargo_values["textiles"]] == bays[cargo_values["produce"]] + 1,
    bays[cargo_values["textiles"]] == bays[cargo_values["produce"]] - 1
))

# Now, evaluate each option to see which one fits the constraints
found_options = []

# Option A: fuel, machinery, textiles
solver.push()
solver.add(bays[0] == cargo_values["fuel"])
solver.add(bays[1] == cargo_values["machinery"])
solver.add(bays[2] == cargo_values["textiles"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: grain, machinery, fuel
solver.push()
solver.add(bays[0] == cargo_values["grain"])
solver.add(bays[1] == cargo_values["machinery"])
solver.add(bays[2] == cargo_values["fuel"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: machinery, livestock, fuel
solver.push()
solver.add(bays[0] == cargo_values["machinery"])
solver.add(bays[1] == cargo_values["livestock"])
solver.add(bays[2] == cargo_values["fuel"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: machinery, textiles, fuel
solver.push()
solver.add(bays[0] == cargo_values["machinery"])
solver.add(bays[1] == cargo_values["textiles"])
solver.add(bays[2] == cargo_values["fuel"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: machinery, textiles, produce
solver.push()
solver.add(bays[0] == cargo_values["machinery"])
solver.add(bays[1] == cargo_values["textiles"])
solver.add(bays[2] == cargo_values["produce"])
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