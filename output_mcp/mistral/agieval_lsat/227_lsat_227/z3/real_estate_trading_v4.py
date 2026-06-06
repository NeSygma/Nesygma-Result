from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define companies
companies = ["RealProp", "Southco", "Trustcorp"]

# Define buildings and their classes
buildings = {
    "Garza Tower": 1,
    "Yates House": 3,
    "Zimmer House": 3,
    "Flores Tower": 1,
    "Lynch Building": 2,
    "King Building": 2,
    "Meyer Building": 2,
    "Ortiz Building": 2,
}

# Initial ownership
initial_ownership = {
    "Garza Tower": "RealProp",
    "Yates House": "RealProp",
    "Zimmer House": "RealProp",
    "Flores Tower": "Southco",
    "Lynch Building": "Southco",
    "King Building": "Trustcorp",
    "Meyer Building": "Trustcorp",
    "Ortiz Building": "Trustcorp",
}

# All buildings
all_buildings = list(buildings.keys())

# Initialize the solver
solver = Solver()

# Declare ownership variables for each building
owner = {b: String(f"owner_{b}") for b in all_buildings}

# Set initial ownership
for b in all_buildings:
    solver.add(owner[b] == initial_ownership[b])

# Count the number of buildings of each class per company
# We will track the number of class 1, 2, and 3 buildings per company
class_counts = {
    (c, 1): Int(f"{c}_class1") for c in companies
}
class_counts.update({
    (c, 2): Int(f"{c}_class2") for c in companies
})
class_counts.update({
    (c, 3): Int(f"{c}_class3") for c in companies
})

# Set initial class counts
for c in companies:
    solver.add(class_counts[(c, 1)] == Sum([1 for b in all_buildings if buildings[b] == 1 and initial_ownership[b] == c]))
    solver.add(class_counts[(c, 2)] == Sum([1 for b in all_buildings if buildings[b] == 2 and initial_ownership[b] == c]))
    solver.add(class_counts[(c, 3)] == Sum([1 for b in all_buildings if buildings[b] == 3 and initial_ownership[b] == c]))

# Trading rules:
# 1. Trade one building for one other building of the same class
#    - This does not change the total number of buildings of that class per company
# 2. Trade one class 1 building for two class 2 buildings
#    - Decrease class 1 by 1, increase class 2 by 2
# 3. Trade one class 2 building for two class 3 buildings
#    - Decrease class 2 by 1, increase class 3 by 2

# We will not model the sequence of trades, but the possible final class counts
# The total number of buildings is fixed, but their classes can change

# Option A: The buildings owned by RealProp are the Flores Tower and the Garza Tower.
# This means RealProp owns "Flores Tower" and "Garza Tower"
# So RealProp must have 2 buildings: one class 1 (Garza Tower) and one class 1 (Flores Tower)
# So RealProp must have 2 class 1 buildings, 0 class 2, 0 class 3
opt_a_constr = And(
    owner["Flores Tower"] == "RealProp",
    owner["Garza Tower"] == "RealProp",
    class_counts[("RealProp", 1)] == 2,
    class_counts[("RealProp", 2)] == 0,
    class_counts[("RealProp", 3)] == 0,
)

# Option B: The buildings owned by Southco are the Flores Tower and the Meyer Building.
# This means Southco owns "Flores Tower" and "Meyer Building"
# So Southco must have 2 buildings: one class 1 (Flores Tower) and one class 2 (Meyer Building)
opt_b_constr = And(
    owner["Flores Tower"] == "Southco",
    owner["Meyer Building"] == "Southco",
    class_counts[("Southco", 1)] == 1,
    class_counts[("Southco", 2)] == 1,
    class_counts[("Southco", 3)] == 0,
)

# Option C: The buildings owned by Southco are the Garza Tower and the Lynch Building.
# This means Southco owns "Garza Tower" and "Lynch Building"
# So Southco must have 2 buildings: one class 1 (Garza Tower) and one class 2 (Lynch Building)
opt_c_constr = And(
    owner["Garza Tower"] == "Southco",
    owner["Lynch Building"] == "Southco",
    class_counts[("Southco", 1)] == 1,
    class_counts[("Southco", 2)] == 1,
    class_counts[("Southco", 3)] == 0,
)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
# This means Trustcorp owns "Flores Tower" and "Ortiz Building"
# So Trustcorp must have 2 buildings: one class 1 (Flores Tower) and one class 2 (Ortiz Building)
opt_d_constr = And(
    owner["Flores Tower"] == "Trustcorp",
    owner["Ortiz Building"] == "Trustcorp",
    class_counts[("Trustcorp", 1)] == 1,
    class_counts[("Trustcorp", 2)] == 1,
    class_counts[("Trustcorp", 3)] == 0,
)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
# This means Trustcorp owns "Garza Tower" and "Meyer Building"
# So Trustcorp must have 2 buildings: one class 1 (Garza Tower) and one class 2 (Meyer Building)
opt_e_constr = And(
    owner["Garza Tower"] == "Trustcorp",
    owner["Meyer Building"] == "Trustcorp",
    class_counts[("Trustcorp", 1)] == 1,
    class_counts[("Trustcorp", 2)] == 1,
    class_counts[("Trustcorp", 3)] == 0,
)

# Now, we will check each option for satisfiability
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