from z3 import *

# Photographers
names = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
# Create Bool vars for assignment to Silva (S) and Thorne (T)
S = {n: Bool(f'S_{n}') for n in names}
T = {n: Bool(f'T_{n}') for n in names}

solver = Solver()

# Each photographer assigned to at most one ceremony
for n in names:
    solver.add(Not(And(S[n], T[n])))

# At least two photographers at each ceremony
solver.add(Sum([If(S[n], 1, 0) for n in names]) >= 2)
solver.add(Sum([If(T[n], 1, 0) for n in names]) >= 2)

# Frost and Heideck together at exactly one ceremony (both assigned together)
# They must be assigned, and same ceremony
solver.add(S['Frost'] == S['Heideck'])
solver.add(T['Frost'] == T['Heideck'])
solver.add(Or(S['Frost'], T['Frost']))  # at least one of them assigned (so both assigned)

# If Lai and Mays both assigned, they must be at different ceremonies
# Encode: If both assigned then not both at Silva and not both at Thorne
both_assigned_LM = And(Or(S['Lai'], T['Lai']), Or(S['Mays'], T['Mays']))
solver.add(Implies(both_assigned_LM, Or(Not(S['Lai']), Not(S['Mays']))))
solver.add(Implies(both_assigned_LM, Or(Not(T['Lai']), Not(T['Mays']))))

# If Gonzalez assigned to Silva then Lai assigned to Thorne
solver.add(Implies(S['Gonzalez'], T['Lai']))

# If Knutson not assigned to Thorne then Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(T['Knutson']), And(T['Heideck'], T['Mays'])))

# Define options for Silva assignment
options = {
    'A': ['Frost', 'Gonzalez', 'Heideck', 'Knutson'],
    'B': ['Frost', 'Gonzalez', 'Heideck'],
    'C': ['Gonzalez', 'Knutson'],
    'D': ['Heideck', 'Lai'],
    'E': ['Knutson', 'Mays']
}

found_options = []
for letter, silva_list in options.items():
    solver.push()
    # Fix Silva assignments according to option
    for n in names:
        if n in silva_list:
            solver.add(S[n] == True)
        else:
            solver.add(S[n] == False)
    # Check satisfiability (Thorne assignments free)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')