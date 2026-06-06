from z3 import *

solver = Solver()

# Bay positions for each cargo type (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Each cargo in a bay 1-6
for c in cargos:
    solver.add(And(c >= 1, c <= 6))

# All different
solver.add(Distinct(cargos))

# grain > livestock
solver.add(grain > livestock)

# livestock > textiles
solver.add(livestock > textiles)

# produce > fuel
solver.add(produce > fuel)

# textiles is next to produce
solver.add(Or(textiles - produce == 1, produce - textiles == 1))

# The question asks which CANNOT be in bay 4
# Check each option: if adding cargo_var == 4 makes it UNSAT, that cargo CANNOT be in bay 4
cannot_options = []
for letter, cargo_var in [("A", grain), ("B", livestock), ("C", machinery), ("D", produce), ("E", textiles)]:
    solver.push()
    solver.add(cargo_var == 4)
    if solver.check() == unsat:
        cannot_options.append(letter)
    solver.pop()

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple CANNOT options found {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: No CANNOT options found")