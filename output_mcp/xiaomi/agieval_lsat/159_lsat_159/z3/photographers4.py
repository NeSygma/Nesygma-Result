from z3 import *

# Define photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer, define which ceremony they are assigned to
# 0 = not assigned, 1 = Silva University, 2 = Thorne University
assign = {p: Int(f'assign_{p}') for p in photographers}

# Base constraints
def add_base_constraints(solver):
    # Domain constraints
    for p in photographers:
        solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))
    
    # Exactly four photographers are assigned (not 0)
    solver.add(Sum([If(assign[p] != 0, 1, 0) for p in photographers]) == 4)
    
    # At least two photographers assigned to Silva University
    solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
    
    # At least two photographers assigned to Thorne University
    solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)
    
    # Constraint 1: Frost must be assigned together with Heideck to one ceremony
    solver.add(Implies(assign['Frost'] != 0, And(assign['Heideck'] != 0, assign['Frost'] == assign['Heideck'])))
    solver.add(Implies(assign['Heideck'] != 0, And(assign['Frost'] != 0, assign['Frost'] == assign['Heideck'])))
    
    # Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
    solver.add(Implies(And(assign['Lai'] != 0, assign['Mays'] != 0), assign['Lai'] != assign['Mays']))
    
    # Constraint 3: If Gonzalez is assigned to Silva (1), then Lai must be assigned to Thorne (2)
    solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))
    
    # Constraint 4: If Knutson is not assigned to Thorne (2), then both Heideck and Mays must be assigned to Thorne (2)
    solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Check each option: which MUST be assigned to Silva
# Option A: Frost must be assigned to Silva
# Option B: Gonzalez must be assigned to Silva
# Option C: Knutson must be assigned to Silva
# Option D: Lai must be assigned to Silva
# Option E: Mays must be assigned to Silva

options = [
    ("A", assign['Frost'] == 1),
    ("B", assign['Gonzalez'] == 1),
    ("C", assign['Knutson'] == 1),
    ("D", assign['Lai'] == 1),
    ("E", assign['Mays'] == 1),
]

found_options = []
for letter, constr in options:
    s = Solver()
    add_base_constraints(s)
    # Check if it's possible that this photographer is NOT assigned to Silva
    s.add(Or(assign[letter_to_name(letter)] == 0, assign[letter_to_name(letter)] == 2))
    if s.check() == unsat:
        # It's impossible for them NOT to be at Silva, so they MUST be at Silva
        found_options.append(letter)

# Helper to map letter to name
def letter_to_name(letter):
    return {'A': 'Frost', 'B': 'Gonzalez', 'C': 'Knutson', 'D': 'Lai', 'E': 'Mays'}[letter]

# Redo with correct order
found_options = []
for letter, constr in options:
    s = Solver()
    add_base_constraints(s)
    name = letter_to_name(letter)
    # Check if it's possible that this photographer is NOT assigned to Silva
    s.add(Or(assign[name] == 0, assign[name] == 2))
    if s.check() == unsat:
        # It's impossible for them NOT to be at Silva, so they MUST be at Silva
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")