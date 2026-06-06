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

# Option A: The buildings owned by RealProp are the Flores Tower and the Garza Tower.
# This means RealProp owns "Flores Tower" and "Garza Tower"
# Other buildings can be owned by anyone
opt_a_constr = And(
    owner["Flores Tower"] == "RealProp",
    owner["Garza Tower"] == "RealProp",
)

# Option B: The buildings owned by Southco are the Flores Tower and the Meyer Building.
# This means Southco owns "Flores Tower" and "Meyer Building"
opt_b_constr = And(
    owner["Flores Tower"] == "Southco",
    owner["Meyer Building"] == "Southco",
)

# Option C: The buildings owned by Southco are the Garza Tower and the Lynch Building.
# This means Southco owns "Garza Tower" and "Lynch Building"
opt_c_constr = And(
    owner["Garza Tower"] == "Southco",
    owner["Lynch Building"] == "Southco",
)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Ortiz Building.
# This means Trustcorp owns "Flores Tower" and "Ortiz Building"
opt_d_constr = And(
    owner["Flores Tower"] == "Trustcorp",
    owner["Ortiz Building"] == "Trustcorp",
)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Meyer Building.
# This means Trustcorp owns "Garza Tower" and "Meyer Building"
opt_e_constr = And(
    owner["Garza Tower"] == "Trustcorp",
    owner["Meyer Building"] == "Trustcorp",
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