from z3 import *

solver = Solver()

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# For each photographer: assigned to Silva or Thorne (or neither, but not both)
silva = {p: Bool(f'silva_{p}') for p in photographers}
thorne = {p: Bool(f'thorne_{p}') for p in photographers}

# No photographer can be assigned to both ceremonies
for p in photographers:
    solver.add(Not(And(silva[p], thorne[p])))

# Each ceremony must have at least 2 photographers
solver.add(Sum([If(silva[p], 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(thorne[p], 1, 0) for p in photographers]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
solver.add(Or(silva['Frost'], thorne['Frost']))
solver.add(Or(silva['Heideck'], thorne['Heideck']))
solver.add(silva['Frost'] == silva['Heideck'])
solver.add(thorne['Frost'] == thorne['Heideck'])

# Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies
both_assigned = And(Or(silva['Lai'], thorne['Lai']), Or(silva['Mays'], thorne['Mays']))
same_ceremony = Or(And(silva['Lai'], silva['Mays']), And(thorne['Lai'], thorne['Mays']))
solver.add(Implies(both_assigned, Not(same_ceremony)))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(silva['Gonzalez'], thorne['Lai']))

# Constraint 4: If Knutson is NOT assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(thorne['Knutson']), And(thorne['Heideck'], thorne['Mays'])))

# Define the options for Thorne University ceremony
options = {
    "A": ['Frost', 'Gonzalez', 'Heideck', 'Mays'],
    "B": ['Frost', 'Heideck', 'Knutson', 'Mays'],
    "C": ['Gonzalez', 'Knutson', 'Lai'],
    "D": ['Gonzalez', 'Knutson', 'Mays'],
    "E": ['Knutson', 'Mays'],
}

# Find which option CANNOT be valid (is UNSAT)
impossible_options = []
for letter, thorne_list in options.items():
    solver.push()
    for p in photographers:
        if p in thorne_list:
            solver.add(thorne[p] == True)
        else:
            solver.add(thorne[p] == False)
    
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")