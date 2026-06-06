from z3 import *

solver = Solver()

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
assign = {p: Int(f'assign_{p}') for p in photographers}

# Domain: 0 = unassigned, 1 = Silva, 2 = Thorne
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two assigned to each ceremony
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Exactly four assigned
solver.add(Sum([If(assign[p] != 0, 1, 0) for p in photographers]) == 4)

# Frost and Heideck together and assigned
solver.add(assign['Frost'] == assign['Heideck'])
solver.add(assign['Frost'] != 0)  # they must be assigned

# If Lai and Mays both assigned, they must be to different ceremonies
solver.add(Implies(And(assign['Lai'] != 0, assign['Mays'] != 0),
                   assign['Lai'] != assign['Mays']))

# If Gonzalez assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# If Knutson not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign['Knutson'] != 2,
                   And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Multiple choice evaluation
found_options = []
options = [
    ("A", assign['Frost'] == 1),
    ("B", assign['Gonzalez'] == 1),
    ("C", assign['Knutson'] == 1),
    ("D", assign['Lai'] == 1),
    ("E", assign['Mays'] == 1)
]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Print model for this option (optional)
        m = solver.model()
        print(f"Model for {letter}:")
        for p in photographers:
            val = m[assign[p]]
            if val is not None:
                print(f"  {p}: {val}")
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