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

# Helper function to get the class of a building
def get_class(building):
    return buildings[building]

# Helper function to get the owner of a building in a given state
# We will model ownership as a function from buildings to companies
# owner[building] = company

# Initialize the solver
solver = Solver()

# Declare ownership variables for each building
owner = {b: String(f"owner_{b}") for b in all_buildings}

# Set initial ownership
for b in all_buildings:
    solver.add(owner[b] == initial_ownership[b])

# Define the allowed trades
# Trade type 1: Trade one building for one other building of the same class
# This means swapping ownership of two buildings of the same class
# Trade type 2: Trade one class 1 building for two class 2 buildings
# This means the company loses one class 1 building and gains two class 2 buildings
# Trade type 3: Trade one class 2 building for two class 3 buildings
# This means the company loses one class 2 building and gains two class 3 buildings

# We will model the trades as constraints on the ownership
# Since trades can be applied any number of times, we need to model the possible ownership states

# For the purpose of this problem, we will not model the exact sequence of trades
# Instead, we will model the possible ownership states that can be reached

# We will use a simplified approach: for each option, we will check if the desired ownership is possible
# by encoding the constraints directly

# Option A: The buildings owned by RealProp are the Flores Tower and the Garza Tower.
# This means RealProp owns "Flores Tower" and "Garza Tower"
# Southco and Trustcorp own the remaining buildings
opt_a_constr = And(
    owner["Flores Tower"] == "RealProp",
    owner["Garza Tower"] == "RealProp",
    owner["Yates House"] != "RealProp",
    owner["Zimmer House"] != "RealProp",
)

# Option B: The buildings owned by Southco are the Flores Tower and the Meyer Building.
# This means Southco owns "Flores Tower" and "Meyer Building"
opt_b_constr = And(
    owner["Flores Tower"] == "Southco",
    owner["Meyer Building"] == "Southco",
    owner["Lynch Building"] != "Southco",
    owner["King Building"] != "Southco",
    owner["Ortiz Building"] != "Southco",
)

# Option C: The buildings owned by Southco are the Garza Tower and the Lynch Building.
# This means Southco owns "Garza Tower" and "Lynch Building"
opt_c_constr = And(
    owner["Garza Tower"] == "Southco",
    owner["Lynch Building"] == "Southco",
    owner["Flores Tower"] != "Southco",
    owner["King Building"] != "Southco",
    owner["Meyer Building"] != "Southco",
    owner["Ortiz Building"] != "Southco",
)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
# This means Trustcorp owns "Flores Tower" and "Ortiz Building"
opt_d_constr = And(
    owner["Flores Tower"] == "Trustcorp",
    owner["Ortiz Building"] == "Trustcorp",
    owner["King Building"] != "Trustcorp",
    owner["Meyer Building"] != "Trustcorp",
    owner["Garza Tower"] != "Trustcorp",
    owner["Lynch Building"] != "Trustcorp",
)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
# This means Trustcorp owns "Garza Tower" and "Meyer Building"
opt_e_constr = And(
    owner["Garza Tower"] == "Trustcorp",
    owner["Meyer Building"] == "Trustcorp",
    owner["Flores Tower"] != "Trustcorp",
    owner["King Building"] != "Trustcorp",
    owner["Ortiz Building"] != "Trustcorp",
    owner["Lynch Building"] != "Trustcorp",
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