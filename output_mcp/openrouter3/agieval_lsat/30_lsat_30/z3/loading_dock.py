from z3 import *

# Create solver
solver = Solver()

# Define cargo types as integers for easier comparison
cargo_types = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]
cargo_to_int = {cargo: i for i, cargo in enumerate(cargo_types)}

# Create variables: bay[i] = cargo type in bay i+1 (since bays are 1-6)
bay = [Int(f"bay_{i}") for i in range(6)]

# Domain constraints: each bay holds exactly one cargo type (0-5)
for i in range(6):
    solver.add(bay[i] >= 0)
    solver.add(bay[i] <= 5)

# All bays have different cargo types
solver.add(Distinct(bay))

# Map cargo types to bay numbers for easier constraint formulation
# Create variables for each cargo's bay number
cargo_bay = {}
for cargo in cargo_types:
    cargo_bay[cargo] = Int(f"bay_of_{cargo}")

# Each cargo is in exactly one bay
for cargo in cargo_types:
    solver.add(cargo_bay[cargo] >= 1)
    solver.add(cargo_bay[cargo] <= 6)

# All cargo bays are distinct
solver.add(Distinct([cargo_bay[cargo] for cargo in cargo_types]))

# Link cargo_bay to bay variables
for i in range(6):
    # bay[i] is the cargo type in bay i+1
    # For each cargo, if cargo_bay[cargo] == i+1, then bay[i] should equal cargo_to_int[cargo]
    solver.add(Or([And(cargo_bay[cargo] == i+1, bay[i] == cargo_to_int[cargo]) for cargo in cargo_types]))

# Constraint 1: grain > livestock
solver.add(cargo_bay["grain"] > cargo_bay["livestock"])

# Constraint 2: livestock > textiles
solver.add(cargo_bay["livestock"] > cargo_bay["textiles"])

# Constraint 3: produce > fuel
solver.add(cargo_bay["produce"] > cargo_bay["fuel"])

# Constraint 4: textiles is next to produce (adjacent)
solver.add(Or(
    cargo_bay["textiles"] == cargo_bay["produce"] - 1,
    cargo_bay["textiles"] == cargo_bay["produce"] + 1
))

# Now test each answer choice for the first three bays
# Each choice gives cargo for bays 1, 2, 3 in order

found_options = []

# Option A: fuel, machinery, textiles
opt_a = And(
    bay[0] == cargo_to_int["fuel"],
    bay[1] == cargo_to_int["machinery"],
    bay[2] == cargo_to_int["textiles"]
)

# Option B: grain, machinery, fuel
opt_b = And(
    bay[0] == cargo_to_int["grain"],
    bay[1] == cargo_to_int["machinery"],
    bay[2] == cargo_to_int["fuel"]
)

# Option C: machinery, livestock, fuel
opt_c = And(
    bay[0] == cargo_to_int["machinery"],
    bay[1] == cargo_to_int["livestock"],
    bay[2] == cargo_to_int["fuel"]
)

# Option D: machinery, textiles, fuel
opt_d = And(
    bay[0] == cargo_to_int["machinery"],
    bay[1] == cargo_to_int["textiles"],
    bay[2] == cargo_to_int["fuel"]
)

# Option E: machinery, textiles, produce
opt_e = And(
    bay[0] == cargo_to_int["machinery"],
    bay[1] == cargo_to_int["textiles"],
    bay[2] == cargo_to_int["produce"]
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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