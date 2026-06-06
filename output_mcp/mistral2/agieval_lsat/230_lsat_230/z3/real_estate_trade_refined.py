from z3 import *

solver = Solver()

# Define the buildings and their initial owners
buildings = {
    "Garza Tower": "RealProp",
    "Yates House": "RealProp",
    "Zimmer House": "RealProp",
    "Flores Tower": "Southco",
    "Lynch Building": "Southco",
    "King Building": "Trustcorp",
    "Meyer Building": "Trustcorp",
    "Ortiz Building": "Trustcorp"
}

# Define the class of each building
building_class = {
    "Garza Tower": 1,
    "Yates House": 3,
    "Zimmer House": 3,
    "Flores Tower": 1,
    "Lynch Building": 2,
    "King Building": 2,
    "Meyer Building": 2,
    "Ortiz Building": 2
}

# Define the companies
companies = ["RealProp", "Southco", "Trustcorp"]

# Final ownership of buildings (can change due to trades)
final_owner = {b: String(f"final_owner_{b}") for b in buildings}

# Initialize final_owner with the initial owners
for b in buildings:
    solver.add(final_owner[b] == buildings[b])

# Define the final number of buildings owned by each company
final_count = {c: Int(f"final_count_{c}") for c in companies}
for c in companies:
    solver.add(final_count[c] == Sum([If(final_owner[b] == c, 1, 0) for b in buildings]))

# The total number of buildings must remain 8
solver.add(Sum([final_count[c] for c in companies]) == 8)

# Each company must own exactly 3 buildings in the end
for c in companies:
    solver.add(final_count[c] == 3)

# Now, we will define the constraints for each multiple-choice option.
# We will check which options are possible under the constraints.

# Option A: The buildings owned by RealProp are the Lynch Building, the Meyer Building, and the Ortiz Building.
opt_a_constr = And(
    final_owner["Lynch Building"] == "RealProp",
    final_owner["Meyer Building"] == "RealProp",
    final_owner["Ortiz Building"] == "RealProp",
    final_count["RealProp"] == 3
)

# Option B: The buildings owned by Southco are the Garza Tower and the Meyer Building.
# This is impossible because Southco must own exactly 3 buildings, and this option only lists 2.
opt_b_constr = And(
    final_owner["Garza Tower"] == "Southco",
    final_owner["Meyer Building"] == "Southco",
    final_count["Southco"] == 2
)

# Option C: The buildings owned by Southco are the King Building, the Meyer Building, and the Ortiz Building.
opt_c_constr = And(
    final_owner["King Building"] == "Southco",
    final_owner["Meyer Building"] == "Southco",
    final_owner["Ortiz Building"] == "Southco",
    final_count["Southco"] == 3
)

# Option D: The buildings owned by Trustcorp are the Flores Tower and the Yates House.
# This is impossible because Trustcorp must own exactly 3 buildings, and this option only lists 2.
opt_d_constr = And(
    final_owner["Flores Tower"] == "Trustcorp",
    final_owner["Yates House"] == "Trustcorp",
    final_count["Trustcorp"] == 2
)

# Option E: The buildings owned by Trustcorp are the Garza Tower and the Lynch Building.
# This is impossible because Trustcorp must own exactly 3 buildings, and this option only lists 2.
opt_e_constr = And(
    final_owner["Garza Tower"] == "Trustcorp",
    final_owner["Lynch Building"] == "Trustcorp",
    final_count["Trustcorp"] == 2
)

# Now, we will check each option to see if it is possible.
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