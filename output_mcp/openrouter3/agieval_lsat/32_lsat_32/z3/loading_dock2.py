from z3 import *

# Declare variables for each cargo type's bay number
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

solver = Solver()

# All bays are between 1 and 6
solver.add(fuel >= 1, fuel <= 6)
solver.add(grain >= 1, grain <= 6)
solver.add(livestock >= 1, livestock <= 6)
solver.add(machinery >= 1, machinery <= 6)
solver.add(produce >= 1, produce <= 6)
solver.add(textiles >= 1, textiles <= 6)

# All bays are different
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Base constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce - 1, textiles == produce + 1))  # next to

# Additional condition: exactly one bay between machinery and grain
solver.add(Or(machinery == grain - 2, machinery == grain + 2))

# Find all solutions
all_solutions = []
while solver.check() == sat:
    m = solver.model()
    solution = {
        'fuel': m[fuel].as_long(),
        'grain': m[grain].as_long(),
        'livestock': m[livestock].as_long(),
        'machinery': m[machinery].as_long(),
        'produce': m[produce].as_long(),
        'textiles': m[textiles].as_long()
    }
    all_solutions.append(solution)
    
    # Blocking clause to find next solution
    solver.add(Or(
        fuel != m[fuel],
        grain != m[grain],
        livestock != m[livestock],
        machinery != m[machinery],
        produce != m[produce],
        textiles != m[textiles]
    ))

print(f"Total solutions found: {len(all_solutions)}")

# For each bay (1-6), check if the cargo type is fixed across all solutions
bay_determined = [True] * 7  # index 1-6
for bay in range(1, 7):
    cargo_types = set()
    for sol in all_solutions:
        # Find which cargo is in this bay
        for cargo, value in sol.items():
            if value == bay:
                cargo_types.add(cargo)
                break
    if len(cargo_types) != 1:
        bay_determined[bay] = False
    else:
        print(f"Bay {bay} has fixed cargo: {list(cargo_types)[0]}")

# Count determined bays
determined_count = sum(1 for bay in range(1, 7) if bay_determined[bay])
print(f"Determined bays: {determined_count}")

# Now test each answer choice
found_options = []

# Option A: exactly 2 bays determined
if determined_count == 2:
    found_options.append("A")
# Option B: exactly 3 bays determined
if determined_count == 3:
    found_options.append("B")
# Option C: exactly 4 bays determined
if determined_count == 4:
    found_options.append("C")
# Option D: exactly 5 bays determined
if determined_count == 5:
    found_options.append("D")
# Option E: exactly 6 bays determined
if determined_count == 6:
    found_options.append("E")

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")