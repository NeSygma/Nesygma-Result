from z3 import *

# Define the photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer, we have three possible states:
# 0 = not assigned, 1 = assigned to Silva, 2 = assigned to Thorne
assign = {p: Int(f'assign_{p}') for p in photographers}

# Base constraints
base_constraints = []
for p in photographers:
    base_constraints.append(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two photographers assigned to Silva (value 1)
base_constraints.append(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)

# At least two photographers assigned to Thorne (value 2)
base_constraints.append(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one of the graduation ceremonies.
base_constraints.append(Or(
    And(assign['Frost'] == 1, assign['Heideck'] == 1),
    And(assign['Frost'] == 2, assign['Heideck'] == 2),
    And(assign['Frost'] == 0, assign['Heideck'] == 0)
))

# Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies.
base_constraints.append(Implies(
    And(assign['Lai'] != 0, assign['Mays'] != 0),
    Or(
        And(assign['Lai'] == 1, assign['Mays'] == 2),
        And(assign['Lai'] == 2, assign['Mays'] == 1)
    )
))

# Constraint 3: If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony.
base_constraints.append(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# Constraint 4: If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it.
base_constraints.append(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Now define the options as constraints
# Option A: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
opt_a_constr = And(
    assign['Gonzalez'] == 1, assign['Lai'] == 1,
    assign['Frost'] == 2, assign['Heideck'] == 2, assign['Mays'] == 2,
    assign['Knutson'] == 0
)

# Option B: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
opt_b_constr = And(
    assign['Gonzalez'] == 1, assign['Mays'] == 1,
    assign['Knutson'] == 2, assign['Lai'] == 2,
    assign['Frost'] == 0, assign['Heideck'] == 0
)

# Option C: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
opt_c_constr = And(
    assign['Frost'] == 1, assign['Gonzalez'] == 1, assign['Heideck'] == 1,
    assign['Knutson'] == 2, assign['Lai'] == 2, assign['Mays'] == 2
)

# Option D: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
opt_d_constr = And(
    assign['Frost'] == 1, assign['Heideck'] == 1, assign['Mays'] == 1,
    assign['Gonzalez'] == 2, assign['Lai'] == 2,
    assign['Knutson'] == 0
)

# Option E: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
opt_e_constr = And(
    assign['Frost'] == 1, assign['Heideck'] == 1, assign['Mays'] == 1,
    assign['Gonzalez'] == 2, assign['Knutson'] == 2, assign['Lai'] == 2
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver = Solver()
    solver.add(base_constraints)
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        for p in photographers:
            print(f"  {p} = {m[assign[p]]}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")