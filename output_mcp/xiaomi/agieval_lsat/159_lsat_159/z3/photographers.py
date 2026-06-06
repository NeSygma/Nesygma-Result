from z3 import *

# Create solver
solver = Solver()

# Define photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer, define which ceremony they are assigned to
# 0 = not assigned, 1 = Silva University, 2 = Thorne University
assign = {p: Int(f'assign_{p}') for p in photographers}

# Domain constraints: each photographer is assigned to 0, 1, or 2
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# Exactly four photographers are assigned (not 0)
solver.add(Sum([If(assign[p] != 0, 1, 0) for p in photographers]) == 4)

# At least two photographers assigned to Silva University
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)

# At least two photographers assigned to Thorne University
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
# Both must be assigned (not 0) and to the same ceremony
solver.add(Implies(assign['Frost'] != 0, And(assign['Heideck'] != 0, assign['Frost'] == assign['Heideck'])))
solver.add(Implies(assign['Heideck'] != 0, And(assign['Frost'] != 0, assign['Frost'] == assign['Heideck'])))

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(And(assign['Lai'] != 0, assign['Mays'] != 0), assign['Lai'] != assign['Mays']))

# Constraint 3: If Gonzalez is assigned to Silva (1), then Lai must be assigned to Thorne (2)
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# Constraint 4: If Knutson is not assigned to Thorne (2), then both Heideck and Mays must be assigned to Thorne (2)
solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Now check which photographer MUST be assigned to Silva University
# We test each option: the photographer is assigned to Silva (assign[p] == 1)
# If this is consistent with all constraints, it's a valid possibility

options = [
    ("A", assign['Frost'] == 1),
    ("B", assign['Gonzalez'] == 1),
    ("C", assign['Knutson'] == 1),
    ("D", assign['Lai'] == 1),
    ("E", assign['Mays'] == 1),
]

found_options = []
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