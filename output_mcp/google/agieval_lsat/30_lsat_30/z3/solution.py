from z3 import *

# Cargo types
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
# Map cargo to integers 0-5
cargo_map = {c: i for i, c in enumerate(cargo_types)}
# Map integers to cargo names
int_to_cargo = {i: c for c, i in cargo_map.items()}

# Variables: bay number for each cargo
bays = {c: Int(c) for c in cargo_types}

solver = Solver()

# Each bay holds a different cargo
solver.add(Distinct([bays[c] for c in cargo_types]))
for c in cargo_types:
    solver.add(bays[c] >= 1, bays[c] <= 6)

# Constraints
solver.add(bays['grain'] > bays['livestock'])
solver.add(bays['livestock'] > bays['textiles'])
solver.add(bays['produce'] > bays['fuel'])
solver.add(Or(bays['textiles'] == bays['produce'] - 1, bays['textiles'] == bays['produce'] + 1))

# Helper to get cargo at a specific bay
def get_cargo_at_bay(b):
    return Or([And(bays[c] == b, c == cargo) for c in cargo_types for cargo in [c]])

# Options
options = {
    "A": ["fuel", "machinery", "textiles"],
    "B": ["grain", "machinery", "fuel"],
    "C": ["machinery", "livestock", "fuel"],
    "D": ["machinery", "textiles", "fuel"],
    "E": ["machinery", "textiles", "produce"]
}

found_options = []
for letter, cargo_list in options.items():
    solver.push()
    # Add constraints for the first three bays
    for i in range(3):
        solver.add(bays[cargo_list[i]] == i + 1)
    
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