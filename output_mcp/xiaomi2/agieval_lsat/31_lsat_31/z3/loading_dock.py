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
names = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']

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

# Now check each option: can that cargo be in bay 4?
cargo_map = {
    "A": grain,
    "B": livestock,
    "C": machinery,
    "D": produce,
    "E": textiles
}

found_options = []
for letter, cargo_var in [("A", grain), ("B", livestock), ("C", machinery), ("D", produce), ("E", textiles)]:
    solver.push()
    solver.add(cargo_var == 4)
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

# Also print which options are possible for debugging
print(f"Possible options for bay 4: {found_options}")
print(f"Cannot be in bay 4: {[l for l in ['A','B','C','D','E'] if l not in found_options]}")