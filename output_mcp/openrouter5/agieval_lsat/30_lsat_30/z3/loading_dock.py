from z3 import *

# There are 6 bays numbered 1 through 6.
# Each bay holds a different cargo type.
# Cargo types: fuel, grain, livestock, machinery, produce, textiles
# We'll assign each cargo type a bay number (1-6), all distinct.

fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

solver = Solver()

# Domain: each bay is 1..6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different
solver.add(Distinct(cargos))

# Constraints:
# 1. grain > livestock
solver.add(grain > livestock)
# 2. livestock > textiles
solver.add(livestock > textiles)
# 3. produce > fuel
solver.add(produce > fuel)
# 4. textiles is next to produce: |textiles - produce| == 1
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Now evaluate each option.
# Each option gives the cargo in bays 1, 2, 3 (in order).
# So we need to add constraints that bay1 = option[0], bay2 = option[1], bay3 = option[2].

# Helper: map cargo name to Z3 variable
name_to_var = {
    "fuel": fuel,
    "grain": grain,
    "livestock": livestock,
    "machinery": machinery,
    "produce": produce,
    "textiles": textiles
}

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
    # bay 1, 2, 3 must equal the given cargo types
    solver.add(name_to_var[cargo_list[0]] == 1)
    solver.add(name_to_var[cargo_list[1]] == 2)
    solver.add(name_to_var[cargo_list[2]] == 3)
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