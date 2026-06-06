from z3 import *

solver = Solver()

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
P = len(photographers)

# Each photographer is assigned to either 0 (not assigned), 1 (Silva), or 2 (Thorne)
assign = {p: Int(f'assign_{p}') for p in photographers}

# Domain: 0 = not assigned, 1 = Silva, 2 = Thorne
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two photographers at each ceremony
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# No photographer can be assigned to both ceremonies (already enforced by domain)

# Frost must be assigned together with Heideck to one of the ceremonies
# i.e., they are assigned to the same ceremony (and it's not 0)
solver.add(assign['Frost'] == assign['Heideck'])
solver.add(assign['Frost'] != 0)

# If Lai and Mays are both assigned, it must be to different ceremonies
# i.e., Not(assign[Lai] != 0 and assign[Mays] != 0 and assign[Lai] == assign[Mays])
solver.add(Not(And(assign['Lai'] != 0, assign['Mays'] != 0, assign['Lai'] == assign['Mays'])))

# If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
# i.e., If assign[Knutson] != 2, then assign[Heideck] == 2 and assign[Mays] == 2
solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Additional condition: Heideck is assigned to the same ceremony as Lai
solver.add(assign['Heideck'] == assign['Lai'])
solver.add(assign['Heideck'] != 0)  # they must be assigned somewhere

# Now evaluate each option
# Option A: Frost is assigned to the Thorne University ceremony.
opt_a = (assign['Frost'] == 2)

# Option B: Gonzalez is assigned to the Silva University ceremony.
opt_b = (assign['Gonzalez'] == 1)

# Option C: Gonzalez is assigned to neither graduation ceremony.
opt_c = (assign['Gonzalez'] == 0)

# Option D: Knutson is assigned to the Thorne University ceremony.
opt_d = (assign['Knutson'] == 2)

# Option E: Lai is assigned to the Thorne University ceremony.
opt_e = (assign['Lai'] == 2)

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