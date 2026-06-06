from z3 import *

solver = Solver()

# Bays 1-6, each holds a different cargo type
# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
bays = [Int(f'bay_{i}') for i in range(1, 7)]

# Each bay holds a value 0-5, all different
for b in bays:
    solver.add(b >= 0, b <= 5)
solver.add(Distinct(bays))

# Define cargo names for readability
fuel, grain, livestock, machinery, produce, textiles = 0, 1, 2, 3, 4, 5

# Helper: position of a cargo type
def pos(cargo):
    return [b for b in bays]  # we'll use Or-logic

# The bay holding grain has a higher number than the bay holding livestock
# grain_pos > livestock_pos
grain_pos = Int('grain_pos')
livestock_pos = Int('livestock_pos')
textiles_pos = Int('textiles_pos')
produce_pos = Int('produce_pos')
fuel_pos = Int('fuel_pos')

# Map cargo to bay position (1-indexed)
for i in range(6):
    solver.add(Implies(bays[i] == grain, grain_pos == i+1))
    solver.add(Implies(bays[i] == livestock, livestock_pos == i+1))
    solver.add(Implies(bays[i] == textiles, textiles_pos == i+1))
    solver.add(Implies(bays[i] == produce, produce_pos == i+1))
    solver.add(Implies(bays[i] == fuel, fuel_pos == i+1))

# Constraint 1: grain > livestock
solver.add(grain_pos > livestock_pos)

# Constraint 2: livestock > textiles
solver.add(livestock_pos > textiles_pos)

# Constraint 3: produce > fuel
solver.add(produce_pos > fuel_pos)

# Constraint 4: textiles is next to produce
solver.add(Or(textiles_pos == produce_pos + 1, textiles_pos == produce_pos - 1))

# Additional constraint: bay 4 is holding produce
solver.add(bays[3] == produce)  # bay 4 is index 3

# Now we need to find how many bays are completely determined
# First, find all solutions
solutions = []
decision_vars = bays
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(v, model_completion=True).as_long() for v in decision_vars)
    solutions.append(sol)
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")

# For each bay, check if it has the same value in all solutions
determined_count = 0
for i in range(6):
    values = set(sol[i] for sol in solutions)
    if len(values) == 1:
        determined_count += 1
        cargo_names = {0: 'fuel', 1: 'grain', 2: 'livestock', 3: 'machinery', 4: 'produce', 5: 'textiles'}
        print(f"Bay {i+1} is determined: {cargo_names[values.pop()]}")
    else:
        print(f"Bay {i+1} is NOT determined: possible values {values}")

print(f"\nNumber of determined bays: {determined_count}")

# Now check which answer option matches
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