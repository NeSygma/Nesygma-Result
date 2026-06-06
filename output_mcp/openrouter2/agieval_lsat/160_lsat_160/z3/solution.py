from z3 import *

solver = Solver()

# Photographers list
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# Boolean variables for assignment to Thorne (T) and Silva (S)
T = {p: Bool(p + '_T') for p in photographers}
S = {p: Bool(p + '_S') for p in photographers}

# Base constraints
# No photographer assigned to both ceremonies
for p in photographers:
    solver.add(Not(And(T[p], S[p])))

# At least two photographers per ceremony
solver.add(Sum([If(T[p], 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(S[p], 1, 0) for p in photographers]) >= 2)

# Frost and Heideck must be assigned together to one ceremony
solver.add(Or(T['Frost'], S['Frost']))
solver.add(Or(T['Heideck'], S['Heideck']))
solver.add(T['Frost'] == T['Heideck'])
solver.add(S['Frost'] == S['Heideck'])

# If Lai and Mays are both assigned, they must be in different ceremonies
solver.add(Not(And(T['Lai'], T['Mays'])))
solver.add(Not(And(S['Lai'], S['Mays'])))

# If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(S['Gonzalez'], T['Lai']))

# If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(Not(T['Knutson']), And(T['Heideck'], T['Mays'])))

# Define option constraints
options = {
    'A': {'Frost', 'Gonzalez', 'Heideck', 'Mays'},
    'B': {'Frost', 'Heideck', 'Knutson', 'Mays'},
    'C': {'Gonzalez', 'Knutson', 'Lai'},
    'D': {'Gonzalez', 'Knutson', 'Mays'},
    'E': {'Knutson', 'Mays'}
}

opt_constrs = {}
for letter, thorne_set in options.items():
    constrs = []
    for p in photographers:
        if p in thorne_set:
            constrs.append(T[p] == True)
            constrs.append(S[p] == False)
        else:
            constrs.append(T[p] == False)
    opt_constrs[letter] = And(*constrs)

# Evaluate options
found_options = []
for letter, constr in [('A', opt_constrs['A']), ('B', opt_constrs['B']), ('C', opt_constrs['C']), ('D', opt_constrs['D']), ('E', opt_constrs['E'])]:
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