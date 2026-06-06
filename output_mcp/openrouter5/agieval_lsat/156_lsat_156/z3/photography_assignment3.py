from z3 import *

# Let's verify option D more carefully and also check if there are multiple valid options
# by using the exact skeleton required.

solver = Solver()

photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
assign = {p: Int(f'assign_{p}') for p in photographers}

# Domain: 0 = not assigned, 1 = Silva, 2 = Thorne
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two photographers at each ceremony
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Frost must be assigned together with Heideck to one of the ceremonies
solver.add(assign['Frost'] == assign['Heideck'])
solver.add(assign['Frost'] != 0)

# If Lai and Mays are both assigned, it must be to different ceremonies
solver.add(Not(And(assign['Lai'] != 0, assign['Mays'] != 0, assign['Lai'] == assign['Mays'])))

# If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Additional condition: Heideck is assigned to the same ceremony as Lai
solver.add(assign['Heideck'] == assign['Lai'])
solver.add(assign['Heideck'] != 0)

# Now test each option as "must be true" by checking if the option is forced
# Option A: Frost is assigned to Thorne
opt_a = (assign['Frost'] == 2)
# Option B: Gonzalez is assigned to Silva
opt_b = (assign['Gonzalez'] == 1)
# Option C: Gonzalez is assigned to neither
opt_c = (assign['Gonzalez'] == 0)
# Option D: Knutson is assigned to Thorne
opt_d = (assign['Knutson'] == 2)
# Option E: Lai is assigned to Thorne
opt_e = (assign['Lai'] == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    # Add all base constraints
    for p in photographers:
        s.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))
    s.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
    s.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)
    s.add(assign['Frost'] == assign['Heideck'])
    s.add(assign['Frost'] != 0)
    s.add(Not(And(assign['Lai'] != 0, assign['Mays'] != 0, assign['Lai'] == assign['Mays'])))
    s.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))
    s.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))
    s.add(assign['Heideck'] == assign['Lai'])
    s.add(assign['Heideck'] != 0)
    
    # Check if the option is consistent with the constraints
    s.add(constr)
    if s.check() == sat:
        found_options.append(letter)

print(f"Options consistent with constraints: {found_options}")

# Now check which option MUST be true (entailed) - the option is true in ALL models
# We check by seeing if the negation is unsatisfiable
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    for p in photographers:
        s.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))
    s.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
    s.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)
    s.add(assign['Frost'] == assign['Heideck'])
    s.add(assign['Frost'] != 0)
    s.add(Not(And(assign['Lai'] != 0, assign['Mays'] != 0, assign['Lai'] == assign['Mays'])))
    s.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))
    s.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))
    s.add(assign['Heideck'] == assign['Lai'])
    s.add(assign['Heideck'] != 0)
    
    # Add negation of the option
    s.add(Not(constr))
    if s.check() == unsat:
        must_be_true.append(letter)

print(f"Options that MUST be true (negation unsat): {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")