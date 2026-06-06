from z3 import *

solver = Solver()

# Bays 1-6, each holds a different cargo type
# Cargo types: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargo = [Int(f'cargo_{i}') for i in range(1, 7)]  # cargo[0]=bay1, cargo[1]=bay2, ..., cargo[5]=bay6

# Each bay holds a different cargo type (0-5)
for i in range(6):
    solver.add(cargo[i] >= 0, cargo[i] <= 5)
solver.add(Distinct(cargo))

# Helper: find which bay holds a given cargo type
def bay_of(cargo_type):
    return [i for i in range(6) if cargo[i] == cargo_type]

# Constraint 1: bay(grain) > bay(livestock)
# grain=1, livestock=2
# We need: the bay number holding grain > bay number holding livestock
# Bay number = index + 1
# Use Or-loop pattern to express: for all pairs of indices, if cargo[i]=grain and cargo[j]=livestock, then i > j
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(cargo[i] == 1, cargo[j] == 2), i > j))

# Constraint 2: bay(livestock) > bay(textiles)
# livestock=2, textiles=5
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(cargo[i] == 2, cargo[j] == 5), i > j))

# Constraint 3: bay(produce) > bay(fuel)
# produce=4, fuel=0
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(cargo[i] == 4, cargo[j] == 0), i > j))

# Constraint 4: bay(textiles) is next to bay(produce)
# textiles=5, produce=4
for i in range(6):
    for j in range(6):
        solver.add(Implies(And(cargo[i] == 5, cargo[j] == 4), Or(i == j + 1, i == j - 1)))

# Now test each option: which CANNOT be in bay 4 (index 3)?
# Bay 4 corresponds to cargo[3]

# Option A: grain in bay 4 => cargo[3] == 1
# Option B: livestock in bay 4 => cargo[3] == 2
# Option C: machinery in bay 4 => cargo[3] == 3
# Option D: produce in bay 4 => cargo[3] == 4
# Option E: textiles in bay 4 => cargo[3] == 5

found_options = []
for letter, constr in [("A", cargo[3] == 1), ("B", cargo[3] == 2), ("C", cargo[3] == 3), ("D", cargo[3] == 4), ("E", cargo[3] == 5)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# We want the one that CANNOT be in bay 4
# So the answer is the one NOT in found_options
cannot_options = [l for l in ["A", "B", "C", "D", "E"] if l not in found_options]

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: All options possible")