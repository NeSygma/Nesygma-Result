from z3 import *

# Photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Create assignment variables: 0 = not assigned, 1 = Silva University, 2 = Thorne University
assign = {p: Int(f"assign_{p}") for p in photographers}

solver = Solver()

# Domain constraints: each photographer can be 0 (not assigned), 1 (Silva), or 2 (Thorne)
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# Constraint 1: At least two photographers to each ceremony
silva_count = Sum([If(assign[p] == 1, 1, 0) for p in photographers])
thorne_count = Sum([If(assign[p] == 2, 1, 0) for p in photographers])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 2: No photographer assigned to both ceremonies (already enforced by domain)

# Constraint 3: Frost must be assigned together with Heideck to one ceremony
solver.add(assign["Frost"] == assign["Heideck"])
solver.add(assign["Frost"] != 0)  # Both must be assigned

# Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(And(assign["Lai"] != 0, assign["Mays"] != 0), assign["Lai"] != assign["Mays"]))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign["Gonzalez"] == 1, assign["Lai"] == 2))

# Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign["Knutson"] != 2, And(assign["Heideck"] == 2, assign["Mays"] == 2)))

# Now test each answer choice
found_options = []

# Option A: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
opt_a = And(
    assign["Gonzalez"] == 1,
    assign["Lai"] == 1,
    assign["Frost"] == 2,
    assign["Heideck"] == 2,
    assign["Mays"] == 2,
    assign["Knutson"] == 0  # Not mentioned, so not assigned
)

# Option B: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
opt_b = And(
    assign["Gonzalez"] == 1,
    assign["Mays"] == 1,
    assign["Knutson"] == 2,
    assign["Lai"] == 2,
    assign["Frost"] == 0,  # Not mentioned
    assign["Heideck"] == 0  # Not mentioned
)

# Option C: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
opt_c = And(
    assign["Frost"] == 1,
    assign["Gonzalez"] == 1,
    assign["Heideck"] == 1,
    assign["Knutson"] == 2,
    assign["Lai"] == 2,
    assign["Mays"] == 2
)

# Option D: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
opt_d = And(
    assign["Frost"] == 1,
    assign["Heideck"] == 1,
    assign["Mays"] == 1,
    assign["Gonzalez"] == 2,
    assign["Lai"] == 2,
    assign["Knutson"] == 0  # Not mentioned
)

# Option E: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
opt_e = And(
    assign["Frost"] == 1,
    assign["Heideck"] == 1,
    assign["Mays"] == 1,
    assign["Gonzalez"] == 2,
    assign["Knutson"] == 2,
    assign["Lai"] == 2
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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