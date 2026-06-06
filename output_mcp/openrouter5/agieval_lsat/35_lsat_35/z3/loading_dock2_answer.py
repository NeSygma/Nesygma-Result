from z3 import *

solver = Solver()

fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

for c in cargos:
    solver.add(c >= 1, c <= 6)

solver.add(Distinct(cargos))
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce + 1, textiles == produce - 1))
solver.add(Or(produce == livestock + 1, produce == livestock - 1))

opt_a = (fuel == 2)
opt_b = (produce == 4)
opt_c = (textiles == 4)
opt_d = (grain == 5)
opt_e = (machinery == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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