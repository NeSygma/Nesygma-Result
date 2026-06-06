from z3 import *

solver = Solver()

# Photographers: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
N = 6
assign = [Int(f'assign_{i}') for i in range(N)]

# Domain: 0=unassigned, 1=Silva, 2=Thorne
for i in range(N):
    solver.add(Or(assign[i] == 0, assign[i] == 1, assign[i] == 2))

# At least two photographers assigned to each ceremony
solver.add(Sum([If(assign[i] == 1, 1, 0) for i in range(N)]) >= 2)
solver.add(Sum([If(assign[i] == 2, 1, 0) for i in range(N)]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
solver.add(Or(And(assign[0] == 1, assign[2] == 1), And(assign[0] == 2, assign[2] == 2)))

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(And(assign[4] != 0, assign[5] != 0),
                   Or(And(assign[4] == 1, assign[5] == 2), And(assign[4] == 2, assign[5] == 1))))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign[1] == 1, assign[4] == 2))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign[3] != 2, And(assign[2] == 2, assign[5] == 2)))

# Additional condition: exactly four photographers are assigned
solver.add(Sum([If(assign[i] != 0, 1, 0) for i in range(N)]) == 4)

# Now test each option: which photographer MUST be assigned to Silva?
# For each option, test the negation: can we have a valid assignment where that photographer is NOT at Silva?
# If the negation is UNSAT, then the photographer must be at Silva.

options = [
    ("A", assign[0] != 1),  # Frost not at Silva
    ("B", assign[1] != 1),  # Gonzalez not at Silva
    ("C", assign[3] != 1),  # Knutson not at Silva
    ("D", assign[4] != 1),  # Lai not at Silva
    ("E", assign[5] != 1),  # Mays not at Silva
]

must_be_silva = []
for letter, constr in options:
    s = Solver()
    # Re-add all constraints
    for i in range(N):
        s.add(Or(assign[i] == 0, assign[i] == 1, assign[i] == 2))
    s.add(Sum([If(assign[i] == 1, 1, 0) for i in range(N)]) >= 2)
    s.add(Sum([If(assign[i] == 2, 1, 0) for i in range(N)]) >= 2)
    s.add(Or(And(assign[0] == 1, assign[2] == 1), And(assign[0] == 2, assign[2] == 2)))
    s.add(Implies(And(assign[4] != 0, assign[5] != 0),
                       Or(And(assign[4] == 1, assign[5] == 2), And(assign[4] == 2, assign[5] == 1))))
    s.add(Implies(assign[1] == 1, assign[4] == 2))
    s.add(Implies(assign[3] != 2, And(assign[2] == 2, assign[5] == 2)))
    s.add(Sum([If(assign[i] != 0, 1, 0) for i in range(N)]) == 4)
    # Add the negation constraint
    s.add(constr)
    
    result = s.check()
    if result == unsat:
        # Photographer must be at Silva
        must_be_silva.append(letter)

if len(must_be_silva) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_silva[0]}")
elif len(must_be_silva) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_silva}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")