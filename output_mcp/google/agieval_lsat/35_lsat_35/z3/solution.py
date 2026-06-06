from z3 import *

# Define cargo types
cargo_types = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
# pos[c] is the bay number (1-6) for cargo c
pos = {c: Int(c) for c in cargo_types}

solver = Solver()

# Each bay holds a different cargo
for c in cargo_types:
    solver.add(pos[c] >= 1, pos[c] <= 6)
solver.add(Distinct([pos[c] for c in cargo_types]))

# Constraints
solver.add(pos['grain'] > pos['livestock'])
solver.add(pos['livestock'] > pos['textiles'])
solver.add(pos['produce'] > pos['fuel'])
solver.add(Or(pos['textiles'] == pos['produce'] + 1, pos['textiles'] == pos['produce'] - 1))

# "If the bay holding produce is next to the bay holding livestock"
solver.add(Or(pos['produce'] == pos['livestock'] + 1, pos['produce'] == pos['livestock'] - 1))

# Options
options = [
    ("A", pos['fuel'] == 2),
    ("B", pos['produce'] == 4),
    ("C", pos['textiles'] == 4),
    ("D", pos['grain'] == 5),
    ("E", pos['machinery'] == 5)
]

# We want to find the one that CANNOT be true (UNSAT)
# The question asks "each of the following could be true EXCEPT"
# So we are looking for the option that is NOT SAT.

results = {}
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        results[letter] = True
    else:
        results[letter] = False
    solver.pop()

# Identify the one that is False (the exception)
false_options = [letter for letter, possible in results.items() if not possible]

if len(false_options) == 1:
    print("STATUS: sat")
    print(f"answer:{false_options[0]}")
elif len(false_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple exceptions found {false_options}")
else:
    print("STATUS: unsat")
    print("Refine: No exceptions found")