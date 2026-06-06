from z3 import *

solver = Solver()

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# Each photographer is assigned to either 0 (not assigned), 1 (Silva), or 2 (Thorne)
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
solver.add(assign['Heideck'] != 0)  # they must be assigned somewhere

# Let's first check if the problem is satisfiable at all
print("Checking base problem with Heideck == Lai...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("SAT - found a model:")
    for p in photographers:
        val = m[assign[p]].as_long()
        loc = "not assigned" if val == 0 else ("Silva" if val == 1 else "Thorne")
        print(f"  {p}: {loc}")
else:
    print(f"Result: {result}")

# Now let's check each option more carefully.
# The question asks: "which one of the following MUST be true?"
# So we need to find which option is true in ALL possible models.
# We can check this by seeing if the negation of the option is unsatisfiable
# (i.e., the option is forced).

print("\n\nChecking which option MUST be true (is entailed):")
for letter, constr in [("A", assign['Frost'] == 2), 
                        ("B", assign['Gonzalez'] == 1), 
                        ("C", assign['Gonzalez'] == 0), 
                        ("D", assign['Knutson'] == 2), 
                        ("E", assign['Lai'] == 2)]:
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
    
    # Add the NEGATION of the option
    s.add(Not(constr))
    
    neg_result = s.check()
    if neg_result == unsat:
        print(f"  Option {letter}: MUST be true (negation is unsat)")
    elif neg_result == sat:
        print(f"  Option {letter}: NOT necessarily true (negation is sat)")
    else:
        print(f"  Option {letter}: unknown")