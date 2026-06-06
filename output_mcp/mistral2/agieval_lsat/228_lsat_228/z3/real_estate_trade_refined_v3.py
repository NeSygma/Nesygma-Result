from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Buildings and their initial classes
buildings = {
    "Garza Tower": 1,  # RealProp
    "Yates House": 3,  # RealProp
    "Zimmer House": 3, # RealProp
    "Flores Tower": 1, # Southco
    "Lynch Building": 2, # Southco
    "King Building": 2, # Trustcorp
    "Meyer Building": 2, # Trustcorp
    "Ortiz Building": 2, # Trustcorp
}

# Initial owners
initial_owners = {
    "Garza Tower": "RealProp",
    "Yates House": "RealProp",
    "Zimmer House": "RealProp",
    "Flores Tower": "Southco",
    "Lynch Building": "Southco",
    "King Building": "Trustcorp",
    "Meyer Building": "Trustcorp",
    "Ortiz Building": "Trustcorp",
}

# After trades, track final ownership and class of each building.
final_owners = {b: String(f"final_owner_{b}") for b in buildings}
final_classes = {b: Int(f"final_class_{b}") for b in buildings}

# Helper: Map owner names to symbolic constants
owner_constants = {
    "RealProp": String("RealProp"),
    "Southco": String("Southco"),
    "Trustcorp": String("Trustcorp"),
}

# Initialize final owners to initial owners
solver = Solver()
for b in buildings:
    solver.add(final_owners[b] == owner_constants[initial_owners[b]])
    solver.add(final_classes[b] == buildings[b])

# RealProp owns only class 2 buildings after trades
solver.add(And([
    Implies(final_owners[b] == owner_constants["RealProp"], final_classes[b] == 2)
    for b in buildings
]))

# Now, we need to check which of the options (A) through (E) must be true.
# We will test each option one by one.

# Define the options as constraints
# (A) Trustcorp owns a class 1 building.
opt_a_constr = Or([
    And(final_owners[b] == owner_constants["Trustcorp"], final_classes[b] == 1)
    for b in buildings
])

# (B) Trustcorp owns the Meyer Building.
opt_b_constr = (final_owners["Meyer Building"] == owner_constants["Trustcorp"])

# (C) Southco owns a class 2 building.
opt_c_constr = Or([
    And(final_owners[b] == owner_constants["Southco"], final_classes[b] == 2)
    for b in buildings
])

# (D) Southco owns both of the class 3 buildings.
# First, identify the class 3 buildings (Yates House, Zimmer House)
class3_buildings = ["Yates House", "Zimmer House"]
opt_d_constr = And([
    final_owners[b] == owner_constants["Southco"]
    for b in class3_buildings
])

# (E) Southco owns the Flores Tower.
opt_e_constr = (final_owners["Flores Tower"] == owner_constants["Southco"])

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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