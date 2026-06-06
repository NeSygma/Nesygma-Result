from z3 import *

# Create solver
solver = Solver()

# Define cargo types as variables representing their bay numbers
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]
cargo_vars = {cargo: Int(cargo) for cargo in cargo_types}

# Each cargo gets a unique bay from 1 to 6
for cargo in cargo_vars.values():
    solver.add(cargo >= 1, cargo <= 6)

# All bays must be distinct
solver.add(Distinct(list(cargo_vars.values())))

# Add the given constraints
# 1. grain > livestock
solver.add(cargo_vars["grain"] > cargo_vars["livestock"])
# 2. livestock > textiles
solver.add(cargo_vars["livestock"] > cargo_vars["textiles"])
# 3. produce > fuel
solver.add(cargo_vars["produce"] > cargo_vars["fuel"])
# 4. textiles is next to produce (adjacent)
solver.add(Or(
    cargo_vars["textiles"] == cargo_vars["produce"] - 1,
    cargo_vars["textiles"] == cargo_vars["produce"] + 1
))

# Now test each answer choice for livestock
found_options = []

# Option A: livestock in bay 1
solver.push()
solver.add(cargo_vars["livestock"] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: livestock in bay 2
solver.push()
solver.add(cargo_vars["livestock"] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: livestock in bay 3
solver.push()
solver.add(cargo_vars["livestock"] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: livestock in bay 5
solver.push()
solver.add(cargo_vars["livestock"] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: livestock in bay 6
solver.push()
solver.add(cargo_vars["livestock"] == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results according to the required format
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")