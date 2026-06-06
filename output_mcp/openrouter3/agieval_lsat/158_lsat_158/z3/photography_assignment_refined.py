from z3 import *

# Photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
# Assignment: 0 = Silva, 1 = Thorne, 2 = unassigned
assign = {p: Int(f"assign_{p}") for p in photographers}

# Base constraints function
def add_base_constraints(solver):
    # Domain constraints: each photographer assigned to 0, 1, or 2
    for p in photographers:
        solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))
    
    # Constraint 1: At least 2 photographers assigned to each ceremony
    silva_count = Sum([If(assign[p] == 0, 1, 0) for p in photographers])
    thorne_count = Sum([If(assign[p] == 1, 1, 0) for p in photographers])
    solver.add(silva_count >= 2)
    solver.add(thorne_count >= 2)
    
    # Constraint 3: Frost must be assigned together with Heideck to one ceremony
    solver.add(Or(
        And(assign["Frost"] == 0, assign["Heideck"] == 0),
        And(assign["Frost"] == 1, assign["Heideck"] == 1)
    ))
    solver.add(assign["Frost"] != 2)
    solver.add(assign["Heideck"] != 2)
    
    # Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
    solver.add(Implies(
        And(assign["Lai"] != 2, assign["Mays"] != 2),
        assign["Lai"] != assign["Mays"]
    ))
    
    # Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
    solver.add(Implies(
        assign["Gonzalez"] == 0,
        assign["Lai"] == 1
    ))
    
    # Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
    solver.add(Implies(
        Or(assign["Knutson"] == 0, assign["Knutson"] == 2),
        And(assign["Heideck"] == 1, assign["Mays"] == 1)
    ))

# Now, for each answer choice, we need to check if that set is exactly the set of mandatory photographers
# But the skeleton checks if the option is satisfiable under base constraints
# Actually, we need to check: for each option, is it possible that the photographers in that option are NOT all assigned?
# No, we need to find which option is the complete list of mandatory photographers

# Let's compute mandatory photographers by checking each photographer
mandatory = []
for p in photographers:
    s = Solver()
    add_base_constraints(s)
    # Add constraint that p is unassigned
    s.add(assign[p] == 2)
    if s.check() == unsat:
        mandatory.append(p)

print("Mandatory photographers:", mandatory)

# Now, for each answer choice, we need to check if it matches the mandatory set
# But the skeleton is for checking if an option is valid under base constraints
# Actually, we need to check if the option is the exact set of mandatory photographers

# Let's define the answer choices
options = {
    "A": ["Frost", "Heideck"],
    "B": ["Frost", "Heideck", "Knutson"],
    "C": ["Frost", "Heideck", "Knutson", "Lai"],
    "D": ["Frost", "Gonzalez", "Heideck"],
    "E": ["Frost", "Gonzalez", "Heideck", "Mays"]
}

# For each option, we need to check if it is exactly the set of mandatory photographers
# That means:
# 1. Every photographer in the option must be mandatory (i.e., cannot be unassigned in any solution)
# 2. Every photographer not in the option must NOT be mandatory (i.e., can be unassigned in some solution)

# We already have mandatory set from above
# Let's verify each option

found_options = []
for letter, photographers_in_option in options.items():
    # Check if this option matches the mandatory set
    if set(photographers_in_option) == set(mandatory):
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