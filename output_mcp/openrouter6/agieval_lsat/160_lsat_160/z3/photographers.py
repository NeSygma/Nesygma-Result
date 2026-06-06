from z3 import *

# Define photographers
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Create Boolean variables for each photographer: assigned to Silva (S) and Thorne (T)
S = {p: Bool(f"S_{p}") for p in photographers}
T = {p: Bool(f"T_{p}") for p in photographers}

solver = Solver()

# Constraint 1: No photographer can be assigned to both ceremonies
for p in photographers:
    solver.add(Not(And(S[p], T[p])))

# Constraint 2: At least two photographers assigned to each ceremony
solver.add(Sum([If(S[p], 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(T[p], 1, 0) for p in photographers]) >= 2)

# Constraint 3: Frost must be assigned together with Heideck to one ceremony
solver.add(S["Frost"] == S["Heideck"])
solver.add(T["Frost"] == T["Heideck"])

# Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
assigned_Lai = Or(S["Lai"], T["Lai"])
assigned_Mays = Or(S["Mays"], T["Mays"])
solver.add(Implies(And(assigned_Lai, assigned_Mays),
                   And(Not(And(S["Lai"], S["Mays"])),
                       Not(And(T["Lai"], T["Mays"])))))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(S["Gonzalez"], T["Lai"]))

# Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(T["Knutson"]), And(T["Heideck"], T["Mays"])))

# Now evaluate each option
options = [
    ("A", ["Frost", "Gonzalez", "Heideck", "Mays"]),
    ("B", ["Frost", "Heideck", "Knutson", "Mays"]),
    ("C", ["Gonzalez", "Knutson", "Lai"]),
    ("D", ["Gonzalez", "Knutson", "Mays"]),
    ("E", ["Knutson", "Mays"])
]

found_impossible = []
for letter, thorne_list in options:
    solver.push()
    # Set Thorne assignment exactly as per option
    for p in photographers:
        if p in thorne_list:
            solver.add(T[p])
        else:
            solver.add(Not(T[p]))
    # Check satisfiability
    if solver.check() == unsat:
        found_impossible.append(letter)
    solver.pop()

# Output results
if len(found_impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{found_impossible[0]}")
elif len(found_impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {found_impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")