from z3 import *

# Cargo types: 0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles
cargo_names = {0: "fuel", 1: "grain", 2: "livestock", 3: "machinery", 4: "produce", 5: "textiles"}

# bay[i] = cargo type assigned to bay i+1 (bays 1-6)
bay = [Int(f'bay_{i}') for i in range(6)]

solver = Solver()

# Each bay holds exactly one cargo type (0-5)
for i in range(6):
    solver.add(bay[i] >= 0, bay[i] <= 5)

# All different
solver.add(Distinct(bay))

# Helper: find the bay index (0-based) holding a given cargo type
def bay_of(cargo_id):
    """Returns the 0-based bay index holding cargo_id"""
    return [i for i in range(6) if bay[i] == cargo_id]

# We need to express constraints in terms of bay positions.
# Let pos[c] = the bay index (0-based) where cargo c is located
pos = [Int(f'pos_{c}') for c in range(6)]
for c in range(6):
    # pos[c] is the bay index holding cargo c
    solver.add(Or([And(bay[i] == c, pos[c] == i) for i in range(6)]))
    solver.add(pos[c] >= 0, pos[c] <= 5)

# Constraint 1: grain > livestock (higher bay number)
solver.add(pos[1] > pos[2])  # grain > livestock

# Constraint 2: livestock > textiles
solver.add(pos[2] > pos[5])  # livestock > textiles

# Constraint 3: produce > fuel
solver.add(pos[4] > pos[0])  # produce > fuel

# Constraint 4: textiles is next to produce
solver.add(Abs(pos[5] - pos[4]) == 1)

# Additional constraint: exactly one bay between machinery and grain
solver.add(Abs(pos[3] - pos[1]) == 2)

# Find all solutions
all_solutions = []
decision_vars = bay  # the variables we care about

while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(bay[i]).as_long() for i in range(6))
    all_solutions.append(sol)
    # Block this solution
    solver.add(Or([bay[i] != sol[i] for i in range(6)]))

print(f"Total solutions found: {len(all_solutions)}")

# For each bay, check if cargo is determined across all solutions
determined_count = 0
for i in range(6):
    values = set(sol[i] for sol in all_solutions)
    if len(values) == 1:
        determined_count += 1
        print(f"Bay {i+1} is DETERMINED: {cargo_names[values.pop()]}")
    else:
        print(f"Bay {i+1} is NOT determined: {[cargo_names[v] for v in sorted(values)]}")

print(f"\nNumber of completely determined bays: {determined_count}")

# Now map to answer choices
# (A) two, (B) three, (C) four, (D) five, (E) six
answer_map = {2: "A", 3: "B", 4: "C", 5: "D", 6: "E"}

if determined_count in answer_map:
    print("STATUS: sat")
    print(f"answer:{answer_map[determined_count]}")
else:
    print("STATUS: unsat")
    print(f"Refine: determined_count={determined_count} not in answer choices")