from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define cargo types as symbolic constants
Fuel, Grain, Livestock, Machinery, Produce, Textiles = Bools('Fuel Grain Livestock Machinery Produce Textiles')
cargo_types = [Fuel, Grain, Livestock, Machinery, Produce, Textiles]

# Define bay positions as Int variables (1 through 6)
bay_positions = [Int(f'bay_{i+1}') for i in range(6)]

# Each bay holds exactly one cargo type, and each cargo type is in exactly one bay
# We will use a mapping: bay -> cargo type
# To do this, we can use a list of cargo types assigned to each bay, but ensure all are distinct

# Alternatively, we can use a function from bay to cargo type, but for simplicity,
# we will use a list of cargo types assigned to bays, and ensure all are distinct and cover all types.

# Let's define a list of cargo types assigned to each bay
bay_cargo = [Int(f'bay_cargo_{i+1}') for i in range(6)]

# Each bay_cargo[i] must be one of the cargo types (0-5 for Fuel, Grain, ...)
cargo_constants = [0, 1, 2, 3, 4, 5]  # 0:Fuel, 1:Grain, 2:Livestock, 3:Machinery, 4:Produce, 5:Textiles

solver = Solver()

# Each bay has a cargo type
for i in range(6):
    solver.add(And(bay_cargo[i] >= 0, bay_cargo[i] < 6))

# All cargo types are assigned to exactly one bay
solver.add(Distinct(bay_cargo))

# Helper: Define the actual cargo type variables for clarity
Fuel_bay = [And(bay_cargo[i] == 0, bay_positions[i] == i+1) for i in range(6)]
Grain_bay = [And(bay_cargo[i] == 1, bay_positions[i] == i+1) for i in range(6)]
Livestock_bay = [And(bay_cargo[i] == 2, bay_positions[i] == i+1) for i in range(6)]
Machinery_bay = [And(bay_cargo[i] == 3, bay_positions[i] == i+1) for i in range(6)]
Produce_bay = [And(bay_cargo[i] == 4, bay_positions[i] == i+1) for i in range(6)]
Textiles_bay = [And(bay_cargo[i] == 5, bay_positions[i] == i+1) for i in range(6)]

# Base constraints from the problem:
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(Or([And(Grain_bay[i], Livestock_bay[j], i+1 > j+1) for i in range(6) for j in range(6)]))

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(Or([And(Livestock_bay[i], Textiles_bay[j], i+1 > j+1) for i in range(6) for j in range(6)]))

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(Or([And(Produce_bay[i], Fuel_bay[j], i+1 > j+1) for i in range(6) for j in range(6)]))

# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or([And(Textiles_bay[i], Produce_bay[j], Or(i+1 == j+1 + 1, i+1 == j+1 - 1)) for i in range(6) for j in range(6)]))

# Conditional constraint for the question:
# If there is exactly one bay between the bay holding machinery and the bay holding grain,
# then ...
# This means abs(Machinery_bay_pos - Grain_bay_pos) == 2

# We will add this constraint to the solver
Machinery_pos = [m for m in bay_positions if m in [i+1 for i in range(6) if bay_cargo[i] == 3]]
Grain_pos = [g for g in bay_positions if g in [i+1 for i in range(6) if bay_cargo[i] == 1]]

# Since we can't directly extract the position from the solver, we will instead
# add the constraint that for some bay, the cargo is machinery and for some bay, the cargo is grain,
# and the absolute difference in their positions is 2.

solver.add(Or([And(bay_cargo[i] == 3, bay_cargo[j] == 1, abs((i+1) - (j+1)) == 2) for i in range(6) for j in range(6)]))

# Now, check if the problem is satisfiable
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("One valid assignment found:")
    for i in range(6):
        cargo_val = model[bay_cargo[i]]
        if cargo_val == 0:
            cargo_name = "Fuel"
        elif cargo_val == 1:
            cargo_name = "Grain"
        elif cargo_val == 2:
            cargo_name = "Livestock"
        elif cargo_val == 3:
            cargo_name = "Machinery"
        elif cargo_val == 4:
            cargo_name = "Produce"
        elif cargo_val == 5:
            cargo_name = "Textiles"
        else:
            cargo_name = "Unknown"
        print(f"Bay {i+1} holds {cargo_name}")
    
    # Now, to determine how many bays are completely determined,
    # we need to check if for each bay, there is only one possible cargo type
    # that can be assigned to it while satisfying all constraints.
    
    determined_count = 0
    
    for bay_idx in range(6):
        possible_cargos = []
        for cargo_val in range(6):
            s_temp = Solver()
            s_temp.add(solver.assertions())
            s_temp.add(bay_cargo[bay_idx] == cargo_val)
            if s_temp.check() == sat:
                possible_cargos.append(cargo_val)
        if len(possible_cargos) == 1:
            determined_count += 1
    
    print(f"Number of bays with determined cargo: {determined_count}")
    
    # Now, evaluate the answer choices
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
else:
    print("STATUS: unknown")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")