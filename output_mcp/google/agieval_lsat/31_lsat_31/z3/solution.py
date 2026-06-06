from z3 import *

# Cargo types
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
# Map cargo to bay number (1-6)
pos = {c: Int(c) for c in cargo_types}

solver = Solver()

# Each bay holds a different cargo
solver.add(Distinct([pos[c] for c in cargo_types]))
for c in cargo_types:
    solver.add(pos[c] >= 1, pos[c] <= 6)

# Constraints
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(pos['grain'] > pos['livestock'])
# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(pos['livestock'] > pos['textiles'])
# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(pos['produce'] > pos['fuel'])
# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or(pos['textiles'] == pos['produce'] + 1, pos['textiles'] == pos['produce'] - 1))

# Check which cargo CANNOT be in bay 4
# Options: (A)grain (B)livestock (C)machinery (D)produce (E)textiles
options = [
    ("A", "grain"),
    ("B", "livestock"),
    ("C", "machinery"),
    ("D", "produce"),
    ("E", "textiles")
]

found_options = []
for letter, cargo in options:
    solver.push()
    solver.add(pos[cargo] == 4)
    if solver.check() == sat:
        # This option is possible
        pass
    else:
        # This option is NOT possible
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