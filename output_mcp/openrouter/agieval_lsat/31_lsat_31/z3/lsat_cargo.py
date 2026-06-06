from z3 import *

# Declare integer variables for each cargo type representing its bay number (1..6)
grain = Int('grain')
livestock = Int('livestock')
textiles = Int('textiles')
produce = Int('produce')
fuel = Int('fuel')
machinery = Int('machinery')

cargo_vars = [grain, livestock, textiles, produce, fuel, machinery]

solver = Solver()
# Domain constraints: each cargo occupies a distinct bay 1..6
for v in cargo_vars:
    solver.add(v >= 1, v <= 6)
solver.add(Distinct(cargo_vars))

# Problem constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(produce - textiles == 1, textiles - produce == 1))

# Prepare option-specific constraints: each option asserts a specific cargo is in bay 4
# We'll collect options that lead to UNSAT (i.e., cannot be in bay 4)
found_options = []
options = [
    ("A", grain),
    ("B", livestock),
    ("C", machinery),
    ("D", produce),
    ("E", textiles)
]
for letter, var in options:
    solver.push()
    solver.add(var == 4)
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

# According to LSAT style, exactly one option should be impossible (unsat)
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")