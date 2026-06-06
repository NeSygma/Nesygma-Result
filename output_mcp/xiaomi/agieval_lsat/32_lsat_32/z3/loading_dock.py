from z3 import *

solver = Solver()

# Define cargo types as integers
FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES = 0, 1, 2, 3, 4, 5
cargo_names = {0: "fuel", 1: "grain", 2: "livestock", 3: "machinery", 4: "produce", 5: "textiles"}

# Variables: bay[c] = bay number where cargo type c is located
bay = [Int(f'bay_{c}') for c in range(6)]
for c in range(6):
    solver.add(bay[c] >= 1, bay[c] <= 6)
solver.add(Distinct(bay))

# Constraints:
# 1. grain > livestock
solver.add(bay[GRAIN] > bay[LIVESTOCK])
# 2. livestock > textiles
solver.add(bay[LIVESTOCK] > bay[TEXTILES])
# 3. produce > fuel
solver.add(bay[PRODUCE] > bay[FUEL])
# 4. textiles is next to produce (adjacent)
solver.add(Or(bay[TEXTILES] == bay[PRODUCE] + 1, bay[TEXTILES] == bay[PRODUCE] - 1))

# Additional condition: exactly one bay between machinery and grain
solver.add(Or(bay[MACHINERY] == bay[GRAIN] + 2, bay[MACHINERY] == bay[GRAIN] - 2))

# First, find all valid solutions
solutions = []
decision_vars = bay  # All bay assignments

while solver.check() == sat:
    m = solver.model()
    sol = {c: m.eval(bay[c]).as_long() for c in range(6)}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([bay[c] != sol[c] for c in range(6)]))

print(f"Total valid solutions: {len(solutions)}")

# For each bay, check if its cargo is determined across all solutions
determined_count = 0
for bay_num in range(1, 7):
    # Get cargo in this bay for each solution
    cargos_in_bay = set()
    for sol in solutions:
        for c in range(6):
            if sol[c] == bay_num:
                cargos_in_bay.add(c)
                break
    if len(cargos_in_bay) == 1:
        determined_count += 1
        print(f"Bay {bay_num}: determined to be {cargo_names[list(cargos_in_bay)[0]]}")
    else:
        print(f"Bay {bay_num}: could be {', '.join(cargo_names[c] for c in cargos_in_bay)}")

print(f"\nNumber of completely determined bays: {determined_count}")

# Now evaluate answer choices
# A: two, B: three, C: four, D: five, E: six
opt_a_constr = (determined_count == 2)
opt_b_constr = (determined_count == 3)
opt_c_constr = (determined_count == 4)
opt_d_constr = (determined_count == 5)
opt_e_constr = (determined_count == 6)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if constr:
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