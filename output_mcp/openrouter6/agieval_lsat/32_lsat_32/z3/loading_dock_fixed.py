from z3 import *

# Declare variables for each cargo type's bay number
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

solver = Solver()

# Domain constraints: each bay number between 1 and 6
solver.add(fuel >= 1, fuel <= 6)
solver.add(grain >= 1, grain <= 6)
solver.add(livestock >= 1, livestock <= 6)
solver.add(machinery >= 1, machinery <= 6)
solver.add(produce >= 1, produce <= 6)
solver.add(textiles >= 1, textiles <= 6)

# All distinct
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Given constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(produce - textiles == 1, textiles - produce == 1))  # next to each other
solver.add(Or(machinery - grain == 2, grain - machinery == 2))   # exactly one bay between

# Enumerate all solutions
decision_vars = [fuel, grain, livestock, machinery, produce, textiles]
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = tuple(int(m.eval(v, model_completion=True).as_long()) for v in decision_vars)
    solutions.append(sol)
    # Blocking clause: at least one variable differs from its value in this model
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")

# For each bay number (1..6), collect which cargo types appear there
cargo_names = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
bay_cargos = {bay: set() for bay in range(1, 7)}
for sol in solutions:
    # sol is tuple of (fuel, grain, livestock, machinery, produce, textiles) bay numbers
    for i, cargo in enumerate(cargo_names):
        bay = sol[i]
        bay_cargos[bay].add(cargo)

# Count bays with exactly one cargo type (determined)
determined_bays = 0
for bay in range(1, 7):
    if len(bay_cargos[bay]) == 1:
        determined_bays += 1
        print(f"Bay {bay} always holds {list(bay_cargos[bay])[0]}")
    else:
        print(f"Bay {bay} can hold {sorted(bay_cargos[bay])}")

print(f"Determined bays: {determined_bays}")

# Map count to answer letter
count_to_letter = {2: 'A', 3: 'B', 4: 'C', 5: 'D', 6: 'E'}
if determined_bays in count_to_letter:
    answer_letter = count_to_letter[determined_bays]
    print("STATUS: sat")
    print(f"answer:{answer_letter}")
else:
    print("STATUS: unsat")
    print(f"Refine: Count {determined_bays} not in options")