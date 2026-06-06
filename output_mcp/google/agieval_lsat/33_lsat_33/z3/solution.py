from z3 import *

# Define cargo types
cargo_types = ['Fuel', 'Grain', 'Livestock', 'Machinery', 'Produce', 'Textiles']
# Define bay numbers
bays = range(1, 7)

# Create variables for each cargo's bay number
bay_of = {c: Int(f'bay_of_{c}') for c in cargo_types}

solver = Solver()

# Each cargo is in a bay 1-6
for c in cargo_types:
    solver.add(bay_of[c] >= 1, bay_of[c] <= 6)

# Each cargo is in a different bay
solver.add(Distinct([bay_of[c] for c in cargo_types]))

# Constraints
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(bay_of['Grain'] > bay_of['Livestock'])
# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(bay_of['Livestock'] > bay_of['Textiles'])
# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(bay_of['Produce'] > bay_of['Fuel'])
# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or(bay_of['Textiles'] == bay_of['Produce'] + 1, bay_of['Textiles'] == bay_of['Produce'] - 1))

# Test each option for "Which one of the following could be the bay holding livestock?"
options = [
    ("A", 1),
    ("B", 2),
    ("C", 3),
    ("D", 5),
    ("E", 6)
]

found_options = []
for letter, bay_num in options:
    solver.push()
    solver.add(bay_of['Livestock'] == bay_num)
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