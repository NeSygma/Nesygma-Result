from z3 import *

# Photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Variables: assignment to Silva (S) and Thorne (T)
# For each photographer p, we have Bool(p_S) and Bool(p_T)
# We'll use a dictionary for easy access
assign_S = {p: Bool(f"{p}_S") for p in photographers}
assign_T = {p: Bool(f"{p}_T") for p in photographers}

solver = Solver()

# Constraint 1: At least 2 photographers assigned to each ceremony
# Count assigned to Silva
silva_count = Sum([If(assign_S[p], 1, 0) for p in photographers])
thorne_count = Sum([If(assign_T[p], 1, 0) for p in photographers])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 2: No photographer assigned to both ceremonies
for p in photographers:
    solver.add(Not(And(assign_S[p], assign_T[p])))

# Constraint 3: Frost must be assigned together with Heideck to one ceremony
# They must be assigned to the same ceremony (both to Silva or both to Thorne)
solver.add(Or(
    And(assign_S["Frost"], assign_S["Heideck"]),
    And(assign_T["Frost"], assign_T["Heideck"])
))

# Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
# If both are assigned (to any ceremony), then they cannot be assigned to the same ceremony
# We need to ensure: if Lai assigned and Mays assigned, then not (same ceremony)
# This means: not (both to Silva) and not (both to Thorne)
solver.add(Implies(
    And(Or(assign_S["Lai"], assign_T["Lai"]), Or(assign_S["Mays"], assign_T["Mays"])),
    And(
        Not(And(assign_S["Lai"], assign_S["Mays"])),
        Not(And(assign_T["Lai"], assign_T["Mays"]))
    )
))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(
    assign_S["Gonzalez"],
    assign_T["Lai"]
))

# Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(
    Not(assign_T["Knutson"]),
    And(assign_T["Heideck"], assign_T["Mays"])
))

# Additional constraint: Not all photographers have to be assigned
# This is already handled by the variables being Boolean (can be False)

# Now evaluate each answer choice
# Answer choices represent the complete assignment to Silva University ceremony
# We need to check if there exists a valid assignment to Thorne that satisfies all constraints

# Define the options as constraints on Silva assignment
opt_a_constr = And(
    assign_S["Frost"],
    assign_S["Gonzalez"],
    assign_S["Heideck"],
    assign_S["Knutson"],
    Not(assign_S["Lai"]),
    Not(assign_S["Mays"])
)

opt_b_constr = And(
    assign_S["Frost"],
    assign_S["Gonzalez"],
    assign_S["Heideck"],
    Not(assign_S["Knutson"]),
    Not(assign_S["Lai"]),
    Not(assign_S["Mays"])
)

opt_c_constr = And(
    Not(assign_S["Frost"]),
    assign_S["Gonzalez"],
    Not(assign_S["Heideck"]),
    assign_S["Knutson"],
    Not(assign_S["Lai"]),
    Not(assign_S["Mays"])
)

opt_d_constr = And(
    Not(assign_S["Frost"]),
    Not(assign_S["Gonzalez"]),
    assign_S["Heideck"],
    Not(assign_S["Knutson"]),
    assign_S["Lai"],
    Not(assign_S["Mays"])
)

opt_e_constr = And(
    Not(assign_S["Frost"]),
    Not(assign_S["Gonzalez"]),
    Not(assign_S["Heideck"]),
    assign_S["Knutson"],
    Not(assign_S["Lai"]),
    assign_S["Mays"]
)

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