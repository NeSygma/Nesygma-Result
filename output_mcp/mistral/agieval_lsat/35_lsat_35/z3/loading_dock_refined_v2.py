from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare cargo types as symbolic constants
Fuel, Grain, Livestock, Machinery, Produce, Textiles = 0, 1, 2, 3, 4, 5

# Assign each cargo to a bay (1-6). Let's represent the assignment as a list where index 0 corresponds to bay 1, index 1 to bay 2, etc.
cargo_in_bay = [Int(f'cargo_in_bay_{i+1}') for i in range(6)]

# Each bay must hold exactly one cargo type
solver = Solver()
solver.add(Distinct(cargo_in_bay))

# Add ordering constraints
# 1. Grain > Livestock (bay number)
# 2. Livestock > Textiles (bay number)
# 3. Produce > Fuel (bay number)

# To enforce these, we need to find the indices of these cargo types and compare them.
# We can use the following approach:
# For all pairs of bays, if one contains Grain and the other contains Livestock, the Grain bay must have a higher index.
for i in range(6):
    for j in range(6):
        if i != j:
            solver.add(Implies(cargo_in_bay[i] == Grain, cargo_in_bay[j] != Livestock))
            solver.add(Implies(cargo_in_bay[i] == Livestock, cargo_in_bay[j] != Textiles))
            solver.add(Implies(cargo_in_bay[i] == Produce, cargo_in_bay[j] != Fuel))

# Now, enforce the ordering by ensuring that the index of Grain is greater than the index of Livestock,
# the index of Livestock is greater than the index of Textiles, and the index of Produce is greater than the index of Fuel.
# We can do this by finding the indices of these cargo types and comparing them.

# Let's define the indices of each cargo type as variables.
cargo_indices = {cargo: Int(f'index_{cargo}') for cargo in [Fuel, Grain, Livestock, Machinery, Produce, Textiles]}

# For each cargo type, its index is the position in the cargo_in_bay list where it appears.
for cargo in [Fuel, Grain, Livestock, Machinery, Produce, Textiles]:
    solver.add(Or([cargo_in_bay[i] == cargo for i in range(6)]))
    for i in range(6):
        solver.add(Implies(cargo_in_bay[i] == cargo, cargo_indices[cargo] == i))

# Now, enforce the ordering constraints using the indices.
solver.add(cargo_indices[Grain] > cargo_indices[Livestock])
solver.add(cargo_indices[Livestock] > cargo_indices[Textiles])
solver.add(cargo_indices[Produce] > cargo_indices[Fuel])

# Add adjacency constraints
# 1. Textiles is next to Produce
# 2. Produce is next to Livestock

# Define adjacency: two bays are adjacent if their indices differ by 1.
for i in range(6):
    for j in range(6):
        if abs(i - j) == 1:
            solver.add(Implies(Or(cargo_in_bay[i] == Textiles, cargo_in_bay[j] == Textiles), 
                              Or(cargo_in_bay[i] == Produce, cargo_in_bay[j] == Produce)))
            solver.add(Implies(Or(cargo_in_bay[i] == Produce, cargo_in_bay[j] == Produce), 
                              Or(cargo_in_bay[i] == Livestock, cargo_in_bay[j] == Livestock)))

# Now, evaluate each option to see if it could be true under the given constraints.
found_options = []

# Option A: Bay 2 is holding fuel. (Bay 2 is index 1)
opt_a_constr = (cargo_in_bay[1] == Fuel)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Bay 4 is holding produce. (Bay 4 is index 3)
opt_b_constr = (cargo_in_bay[3] == Produce)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Bay 4 is holding textiles. (Bay 4 is index 3)
opt_c_constr = (cargo_in_bay[3] == Textiles)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Bay 5 is holding grain. (Bay 5 is index 4)
opt_d_constr = (cargo_in_bay[4] == Grain)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Bay 5 is holding machinery. (Bay 5 is index 4)
opt_e_constr = (cargo_in_bay[4] == Machinery)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")