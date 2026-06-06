from z3 import *

# Define cargo types
cargo_names = ['fuel','grain','livestock','machinery','produce','textiles']
num_cargo = len(cargo_names)
# Variables: bay position for each cargo (1..6)
bay = [Int(f'bay_{c}') for c in cargo_names]
solver = Solver()
# Domain constraints
for b in bay:
    solver.add(b >= 1, b <= 6)
# All distinct bays
solver.add(Distinct(bay))
# Helper to get index
idx = {name:i for i,name in enumerate(cargo_names)}
# Constraints from problem
solver.add(bay[idx['grain']] > bay[idx['livestock']])
solver.add(bay[idx['livestock']] > bay[idx['textiles']])
solver.add(bay[idx['produce']] > bay[idx['fuel']])
solver.add(Abs(bay[idx['textiles']] - bay[idx['produce']]) == 1)
solver.add(Abs(bay[idx['machinery']] - bay[idx['grain']]) == 2)

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    # Record mapping bay -> cargo
    bay_to_cargo = {}
    for name in cargo_names:
        b = m[bay[idx[name]]].as_long()
        bay_to_cargo[b] = name
    solutions.append(bay_to_cargo)
    # Block this solution
    block = []
    for var in bay:
        block.append(var != m[var])
    solver.add(Or(block))

# Determine for each bay whether cargo is fixed across all solutions
fixed_counts = 0
fixed_info = {}
for b in range(1,7):
    cargos = set(sol[b] for sol in solutions)
    if len(cargos) == 1:
        fixed_counts += 1
        fixed_info[b] = next(iter(cargos))

# Now test each answer option
# Recreate base solver for option testing
base_solver = Solver()
# add same base constraints again
for b in bay:
    base_solver.add(b >= 1, b <= 6)
base_solver.add(Distinct(bay))
base_solver.add(bay[idx['grain']] > bay[idx['livestock']])
base_solver.add(bay[idx['livestock']] > bay[idx['textiles']])
base_solver.add(bay[idx['produce']] > bay[idx['fuel']])
base_solver.add(Abs(bay[idx['textiles']] - bay[idx['produce']]) == 1)
base_solver.add(Abs(bay[idx['machinery']] - bay[idx['grain']]) == 2)

found_options = []
options = [
    ("A", 2),
    ("B", 3),
    ("C", 4),
    ("D", 5),
    ("E", 6)
]
for letter, k in options:
    base_solver.push()
    # Add constraint that fixed_counts == k as a Boolean constant
    base_solver.add(BoolVal(fixed_counts == k))
    if base_solver.check() == sat:
        found_options.append(letter)
    base_solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")