from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define cargo types as symbolic constants
Fuel, Grain, Livestock, Machinery, Produce, Textiles = Ints('Fuel Grain Livestock Machinery Produce Textiles')
cargo_types = [Fuel, Grain, Livestock, Machinery, Produce, Textiles]

# Define bay positions as Int variables (1 through 6)
bays = [Int(f'bay_{i+1}') for i in range(6)]

# Each bay holds a distinct cargo type
solver = Solver()
solver.add(Distinct(bays))

# Helper: Map cargo type to its bay position
# We will use the cargo type values to represent the bay positions
# So, for example, if bay 3 holds Grain, then Grain == 3

# Base constraints from the problem:
# 1. The bay holding grain has a higher number than the bay holding livestock.
solver.add(Grain > Livestock)

# 2. The bay holding livestock has a higher number than the bay holding textiles.
solver.add(Livestock > Textiles)

# 3. The bay holding produce has a higher number than the bay holding fuel.
solver.add(Produce > Fuel)

# 4. The bay holding textiles is next to the bay holding produce.
solver.add(Or(Textiles == Produce + 1, Textiles == Produce - 1))

# Conditional constraint for the question:
# If there is exactly one bay between the bay holding machinery and the bay holding grain,
# then ...
# This means abs(Machinery - Grain) == 2
# We will add this constraint as part of the conditional scenario.

# For the purpose of this problem, we assume the conditional constraint holds.
# So we add it to the solver.
solver.add(abs(Machinery - Grain) == 2)

# Now, we need to find all possible assignments (models) that satisfy the constraints.
# For each bay, we want to check if the cargo type is uniquely determined.

# To do this, we will find all models and check consistency of cargo types per bay.

# However, since we cannot easily enumerate all models in a single script,
# we will instead check for each bay if changing its cargo type to any other type
# violates the constraints. If yes, then it is determined.

# But a more straightforward way is to find one model and then check
# if the cargo types are forced for some bays.

# Let's find one model first.
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("One valid assignment found:")
    for i in range(6):
        bay_var = bays[i]
        bay_num = model[bay_var]
        # Find which cargo type is assigned to this bay
        for ct in cargo_types:
            if model[ct] == bay_num:
                print(f"Bay {bay_num} holds {ct}")
                break
    
    # Now, to determine how many bays are completely determined,
    # we need to check if for each bay, there is only one possible cargo type
    # that can be assigned to it while satisfying all constraints.
    
    # We will check each bay position (1-6) and see if the cargo type is forced.
    determined_count = 0
    
    for bay_pos in range(1, 7):
        possible_cargos = []
        for ct in cargo_types:
            # Create a new solver instance
            s_temp = Solver()
            s_temp.add(solver.assertions())
            # Constrain this cargo type to be at this bay position
            s_temp.add(ct == bay_pos)
            # Check if this is satisfiable
            if s_temp.check() == sat:
                possible_cargos.append(ct)
        # If only one cargo type is possible for this bay, it is determined
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