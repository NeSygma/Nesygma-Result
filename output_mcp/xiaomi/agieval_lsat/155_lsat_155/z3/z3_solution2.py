from z3 import *

# Define the photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer, we have three possible states:
# 0 = not assigned, 1 = assigned to Silva, 2 = assigned to Thorne
assign = {p: Int(f'assign_{p}') for p in photographers}

solver = Solver()

# Domain constraints: each photographer is 0, 1, or 2
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two photographers assigned to Silva (value 1)
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)

# At least two photographers assigned to Thorne (value 2)
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one of the graduation ceremonies.
# This means either both are at Silva, or both are at Thorne, or both are unassigned.
solver.add(Or(
    And(assign['Frost'] == 1, assign['Heideck'] == 1),
    And(assign['Frost'] == 2, assign['Heideck'] == 2),
    And(assign['Frost'] == 0, assign['Heideck'] == 0)
))

# Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies.
# Both assigned means neither is 0. Different ceremonies means one is 1 and the other is 2.
solver.add(Implies(
    And(assign['Lai'] != 0, assign['Mays'] != 0),
    Or(
        And(assign['Lai'] == 1, assign['Mays'] == 2),
        And(assign['Lai'] == 2, assign['Mays'] == 1)
    )
))

# Constraint 3: If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony.
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# Constraint 4: If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it.
solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

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

# Let's debug each option individually
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    s = Solver()
    s.add(constr)
    # Add all base constraints
    for p in photographers:
        s.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))
    s.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
    s.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)
    s.add(Or(
        And(assign['Frost'] == 1, assign['Heideck'] == 1),
        And(assign['Frost'] == 2, assign['Heideck'] == 2),
        And(assign['Frost'] == 0, assign['Heideck'] == 0)
    ))
    s.add(Implies(
        And(assign['Lai'] != 0, assign['Mays'] != 0),
        Or(
            And(assign['Lai'] == 1, assign['Mays'] == 2),
            And(assign['Lai'] == 2, assign['Mays'] == 1)
        )
    ))
    s.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))
    s.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))
    
    result = s.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        m = s.model()
        for p in photographers:
            print(f"  {p} = {m[assign[p]]}")