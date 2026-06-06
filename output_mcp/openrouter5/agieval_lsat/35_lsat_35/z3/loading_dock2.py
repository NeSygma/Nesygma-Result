from z3 import *

solver = Solver()

# Bays 1 through 6
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

# Constraints:
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)

# textiles is next to produce
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Additional condition: produce is next to livestock
solver.add(Or(produce == livestock + 1, produce == livestock - 1))

# Let's first find all valid models to understand the space
# We'll enumerate all solutions
solutions = []
solver_copy = Solver()
for c in cargos:
    solver_copy.add(c >= 1, c <= 6)
solver_copy.add(Distinct(cargos))
solver_copy.add(grain > livestock)
solver_copy.add(livestock > textiles)
solver_copy.add(produce > fuel)
solver_copy.add(Or(textiles == produce + 1, textiles == produce - 1))
solver_copy.add(Or(produce == livestock + 1, produce == livestock - 1))

while solver_copy.check() == sat:
    m = solver_copy.model()
    sol = {str(c): m.eval(c, model_completion=True).as_long() for c in cargos}
    solutions.append(sol)
    solver_copy.add(Or([c != m.eval(c, model_completion=True) for c in cargos]))

print(f"Total valid assignments: {len(solutions)}")
for s in solutions:
    print(s)

# Now check each option
# The question asks: "each of the following could be true EXCEPT"
# So we need to find which option CANNOT be true (unsat)

opt_a = (fuel == 2)
opt_b = (produce == 4)
opt_c = (textiles == 4)
opt_d = (grain == 5)
opt_e = (machinery == 5)

print("\n--- Checking each option ---")
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    for c in cargos:
        s.add(c >= 1, c <= 6)
    s.add(Distinct(cargos))
    s.add(grain > livestock)
    s.add(livestock > textiles)
    s.add(produce > fuel)
    s.add(Or(textiles == produce + 1, textiles == produce - 1))
    s.add(Or(produce == livestock + 1, produce == livestock - 1))
    s.add(constr)
    res = s.check()
    print(f"Option {letter}: {res}")
    if res == sat:
        print(f"  Model: {s.model()}")