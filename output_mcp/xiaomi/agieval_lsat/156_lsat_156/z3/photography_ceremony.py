from z3 import *

solver = Solver()

# Define photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer, we have:
# - assigned: Bool (whether they are assigned at all)
# - at_silva: Bool (whether assigned to Silva)
# - at_thorne: Bool (whether assigned to Thorne)
assigned = {p: Bool(f'assigned_{p}') for p in photographers}
at_silva = {p: Bool(f'at_silva_{p}') for p in photographers}
at_thorne = {p: Bool(f'at_thorne_{p}') for p in photographers}

# Basic constraints: if assigned, must be at exactly one ceremony; if not assigned, at neither
for p in photographers:
    # If assigned, exactly one of at_silva or at_thorne
    solver.add(Implies(assigned[p], And(at_silva[p], Not(at_thorne[p]))))
    solver.add(Implies(assigned[p], And(Not(at_silva[p]), at_thorne[p])))
    # Actually, let me redo this properly
    pass

# Clear and redo
solver = Solver()

# For each photographer: 0 = unassigned, 1 = Silva, 2 = Thorne
assignment = {p: Int(f'assign_{p}') for p in photographers}
for p in photographers:
    solver.add(Or(assignment[p] == 0, assignment[p] == 1, assignment[p] == 2))

# At least 2 photographers at Silva
solver.add(Sum([If(assignment[p] == 1, 1, 0) for p in photographers]) >= 2)

# At least 2 photographers at Thorne
solver.add(Sum([If(assignment[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 1: Frost and Heideck must be assigned together to the same ceremony
# If Frost is assigned, Heideck must be assigned to the same ceremony, and vice versa
solver.add(Implies(assignment['Frost'] != 0, assignment['Frost'] == assignment['Heideck']))
solver.add(Implies(assignment['Heideck'] != 0, assignment['Frost'] == assignment['Heideck']))

# Constraint 2: If Lai and Mays are both assigned, they must be at different ceremonies
solver.add(Implies(And(assignment['Lai'] != 0, assignment['Mays'] != 0), assignment['Lai'] != assignment['Mays']))

# Constraint 3: If Gonzalez is at Silva, then Lai must be at Thorne
solver.add(Implies(assignment['Gonzalez'] == 1, assignment['Lai'] == 2))

# Constraint 4: If Knutson is NOT at Thorne, then both Heideck and Mays must be at Thorne
solver.add(Implies(assignment['Knutson'] != 2, And(assignment['Heideck'] == 2, assignment['Mays'] == 2)))

# Additional condition: Heideck is assigned to the same ceremony as Lai
solver.add(assignment['Heideck'] == assignment['Lai'])
# Also both must be assigned (since they're "assigned to the same ceremony")
solver.add(assignment['Heideck'] != 0)
solver.add(assignment['Lai'] != 0)

# Now evaluate each answer choice
# (A) Frost is assigned to the Thorne University ceremony.
opt_a = (assignment['Frost'] == 2)

# (B) Gonzalez is assigned to the Silva University ceremony.
opt_b = (assignment['Gonzalez'] == 1)

# (C) Gonzalez is assigned to neither graduation ceremony.
opt_c = (assignment['Gonzalez'] == 0)

# (D) Knutson is assigned to the Thorne University ceremony.
opt_d = (assignment['Knutson'] == 2)

# (E) Lai is assigned to the Thorne University ceremony.
opt_e = (assignment['Lai'] == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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