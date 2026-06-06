from z3 import *

# Each cargo type is assigned to a bay (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]
cargo_names = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']

solver = Solver()

# Each cargo in a bay 1-6
for c in cargos:
    solver.add(And(c >= 1, c <= 6))

# All different bays
solver.add(Distinct(cargos))

# Constraints
solver.add(grain > livestock)       # grain has higher number than livestock
solver.add(livestock > textiles)    # livestock has higher number than textiles
solver.add(produce > fuel)          # produce has higher number than fuel
solver.add(Abs(textiles - produce) == 1)  # textiles is next to produce

# Bay 4 is holding produce
solver.add(produce == 4)

# Enumerate ALL valid solutions
solutions = []
decision_vars = cargos

while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True).as_long() for v in decision_vars}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total valid solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"  Solution {i+1}: {sol}")

# For each bay, check if cargo is the same across ALL solutions
bay_cargo = {b: set() for b in range(1, 7)}
for sol in solutions:
    for cname, bay_num in sol.items():
        bay_cargo[bay_num].add(cname)

determined_count = 0
for bay in range(1, 7):
    if len(bay_cargo[bay]) == 1:
        determined_count += 1
        print(f"  Bay {bay}: DETERMINED -> {bay_cargo[bay]}")
    else:
        print(f"  Bay {bay}: UNDETERMINED -> {bay_cargo[bay]}")

print(f"\nNumber of completely determined bays: {determined_count}")

# Now evaluate answer choices
# (A) two, (B) three, (C) four, (D) five, (E) six
found_options = []
for letter, count in [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
    if determined_count == count:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")