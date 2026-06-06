from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare cargo types as symbolic constants
Fuel, Grain, Livestock, Machinery, Produce, Textiles = Ints('Fuel Grain Livestock Machinery Produce Textiles')
# We will assign each cargo to a bay (1-6). Let's represent the assignment as a list where index 0 corresponds to bay 1, index 1 to bay 2, etc.
cargo_in_bay = [Int(f'cargo_in_bay_{i+1}') for i in range(6)]

# Each bay must hold exactly one cargo type
solver = Solver()
solver.add(Distinct(cargo_in_bay))

# Helper: cargo type constants for constraints
Fuel_val, Grain_val, Livestock_val, Machinery_val, Produce_val, Textiles_val = 0, 1, 2, 3, 4, 5

# Add constraints based on the problem statement
# 1. The bay holding grain has a higher number than the bay holding livestock.
# This means the index of grain is less than the index of livestock (since bay 1 is index 0)
solver.add(
    Or(
        And(cargo_in_bay[0] == Grain_val, cargo_in_bay[1] == Livestock_val),
        And(cargo_in_bay[0] == Grain_val, cargo_in_bay[2] == Livestock_val),
        And(cargo_in_bay[0] == Grain_val, cargo_in_bay[3] == Livestock_val),
        And(cargo_in_bay[0] == Grain_val, cargo_in_bay[4] == Livestock_val),
        And(cargo_in_bay[0] == Grain_val, cargo_in_bay[5] == Livestock_val),
        And(cargo_in_bay[1] == Grain_val, cargo_in_bay[2] == Livestock_val),
        And(cargo_in_bay[1] == Grain_val, cargo_in_bay[3] == Livestock_val),
        And(cargo_in_bay[1] == Grain_val, cargo_in_bay[4] == Livestock_val),
        And(cargo_in_bay[1] == Grain_val, cargo_in_bay[5] == Livestock_val),
        And(cargo_in_bay[2] == Grain_val, cargo_in_bay[3] == Livestock_val),
        And(cargo_in_bay[2] == Grain_val, cargo_in_bay[4] == Livestock_val),
        And(cargo_in_bay[2] == Grain_val, cargo_in_bay[5] == Livestock_val),
        And(cargo_in_bay[3] == Grain_val, cargo_in_bay[4] == Livestock_val),
        And(cargo_in_bay[3] == Grain_val, cargo_in_bay[5] == Livestock_val),
        And(cargo_in_bay[4] == Grain_val, cargo_in_bay[5] == Livestock_val),
    )
)

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(
    Or(
        And(cargo_in_bay[0] == Livestock_val, cargo_in_bay[1] == Textiles_val),
        And(cargo_in_bay[0] == Livestock_val, cargo_in_bay[2] == Textiles_val),
        And(cargo_in_bay[0] == Livestock_val, cargo_in_bay[3] == Textiles_val),
        And(cargo_in_bay[0] == Livestock_val, cargo_in_bay[4] == Textiles_val),
        And(cargo_in_bay[0] == Livestock_val, cargo_in_bay[5] == Textiles_val),
        And(cargo_in_bay[1] == Livestock_val, cargo_in_bay[2] == Textiles_val),
        And(cargo_in_bay[1] == Livestock_val, cargo_in_bay[3] == Textiles_val),
        And(cargo_in_bay[1] == Livestock_val, cargo_in_bay[4] == Textiles_val),
        And(cargo_in_bay[1] == Livestock_val, cargo_in_bay[5] == Textiles_val),
        And(cargo_in_bay[2] == Livestock_val, cargo_in_bay[3] == Textiles_val),
        And(cargo_in_bay[2] == Livestock_val, cargo_in_bay[4] == Textiles_val),
        And(cargo_in_bay[2] == Livestock_val, cargo_in_bay[5] == Textiles_val),
        And(cargo_in_bay[3] == Livestock_val, cargo_in_bay[4] == Textiles_val),
        And(cargo_in_bay[3] == Livestock_val, cargo_in_bay[5] == Textiles_val),
        And(cargo_in_bay[4] == Livestock_val, cargo_in_bay[5] == Textiles_val),
    )
)

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(
    Or(
        And(cargo_in_bay[0] == Produce_val, cargo_in_bay[1] == Fuel_val),
        And(cargo_in_bay[0] == Produce_val, cargo_in_bay[2] == Fuel_val),
        And(cargo_in_bay[0] == Produce_val, cargo_in_bay[3] == Fuel_val),
        And(cargo_in_bay[0] == Produce_val, cargo_in_bay[4] == Fuel_val),
        And(cargo_in_bay[0] == Produce_val, cargo_in_bay[5] == Fuel_val),
        And(cargo_in_bay[1] == Produce_val, cargo_in_bay[2] == Fuel_val),
        And(cargo_in_bay[1] == Produce_val, cargo_in_bay[3] == Fuel_val),
        And(cargo_in_bay[1] == Produce_val, cargo_in_bay[4] == Fuel_val),
        And(cargo_in_bay[1] == Produce_val, cargo_in_bay[5] == Fuel_val),
        And(cargo_in_bay[2] == Produce_val, cargo_in_bay[3] == Fuel_val),
        And(cargo_in_bay[2] == Produce_val, cargo_in_bay[4] == Fuel_val),
        And(cargo_in_bay[2] == Produce_val, cargo_in_bay[5] == Fuel_val),
        And(cargo_in_bay[3] == Produce_val, cargo_in_bay[4] == Fuel_val),
        And(cargo_in_bay[3] == Produce_val, cargo_in_bay[5] == Fuel_val),
        And(cargo_in_bay[4] == Produce_val, cargo_in_bay[5] == Fuel_val),
    )
)

# 4. The bay holding textiles is next to the bay holding produce.
# This means the absolute difference between their indices is 1.
for i in range(6):
    for j in range(6):
        if abs(i - j) == 1:
            solver.add(Implies(And(cargo_in_bay[i] == Textiles_val, cargo_in_bay[j] == Produce_val), True))
            solver.add(Implies(And(cargo_in_bay[i] == Produce_val, cargo_in_bay[j] == Textiles_val), True))

# Additional condition for the question: The bay holding produce is next to the bay holding livestock.
for i in range(6):
    for j in range(6):
        if abs(i - j) == 1:
            solver.add(Implies(And(cargo_in_bay[i] == Produce_val, cargo_in_bay[j] == Livestock_val), True))
            solver.add(Implies(And(cargo_in_bay[i] == Livestock_val, cargo_in_bay[j] == Produce_val), True))

# Now, evaluate each option to see if it could be true under the given constraints.
found_options = []

# Option A: Bay 2 is holding fuel. (Bay 2 is index 1)
opt_a_constr = (cargo_in_bay[1] == Fuel_val)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Bay 4 is holding produce. (Bay 4 is index 3)
opt_b_constr = (cargo_in_bay[3] == Produce_val)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Bay 4 is holding textiles. (Bay 4 is index 3)
opt_c_constr = (cargo_in_bay[3] == Textiles_val)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Bay 5 is holding grain. (Bay 5 is index 4)
opt_d_constr = (cargo_in_bay[4] == Grain_val)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Bay 5 is holding machinery. (Bay 5 is index 4)
opt_e_constr = (cargo_in_bay[4] == Machinery_val)
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