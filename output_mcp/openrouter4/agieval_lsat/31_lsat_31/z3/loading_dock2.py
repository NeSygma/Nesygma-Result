from z3 import *

solver = Solver()

# Define variables for each cargo type - the bay number (1-6) they occupy
grain = Int('grain')
livestock = Int('livestock')
textiles = Int('textiles')
produce = Int('produce')
fuel = Int('fuel')
machinery = Int('machinery')

cargos = [grain, livestock, textiles, produce, fuel, machinery]

# Domain constraints: each bay between 1 and 6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different
solver.add(Distinct(cargos))

# Constraints
solver.add(grain > livestock)       # grain higher than livestock
solver.add(livestock > textiles)    # livestock higher than textiles
solver.add(produce > fuel)          # produce higher than fuel
# textiles is next to produce
solver.add(Or(textiles - produce == 1, produce - textiles == 1))

# Now test each option: can that cargo be in bay 4?
options = [
    ("A", grain == 4, "grain"),
    ("B", livestock == 4, "livestock"),
    ("C", machinery == 4, "machinery"),
    ("D", produce == 4, "produce"),
    ("E", textiles == 4, "textiles"),
]

# Find the option that is UNSAT (impossible) - that is the answer
impossible_options = []
for letter, constr, name in options:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")