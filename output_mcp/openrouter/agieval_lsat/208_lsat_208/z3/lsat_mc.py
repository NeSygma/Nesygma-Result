from z3 import *

# Define students
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']
# Bool for team assignment: True = green, False = red
G = {s: Bool(f'G_{s}') for s in students}
# Bool for facilitator status
F = {s: Bool(f'F_{s}') for s in students}

solver = Solver()
# Base constraints
# Each team has exactly one facilitator
solver.add(Sum([If(F[s] & G[s], 1, 0) for s in students]) == 1)  # green facilitator count
solver.add(Sum([If(F[s] & Not(G[s]), 1, 0) for s in students]) == 1)  # red facilitator count
# Facilitator must be member of that team
for s in students:
    solver.add(Implies(F[s], Or(G[s], Not(G[s]))) )  # trivial, but we also need consistency later via option constraints
    # Actually ensure facilitator belongs to team: already accounted in counts using conjunction

# Team size: green team has 2 or 3 members
green_count = Sum([If(G[s], 1, 0) for s in students])
solver.add(Or(green_count == 2, green_count == 3))
# Juana different team than Olga
solver.add(G['Juana'] != G['Olga'])
# Lateefah green
solver.add(G['Lateefah'] == True)
# Kelly not facilitator
solver.add(F['Kelly'] == False)
# Olga is facilitator
solver.add(F['Olga'] == True)

# Helper to create option constraints
def option_constraints(opt):
    cons = []
    # opt is dict with keys: 'green', 'red', 'fac_green', 'fac_red'
    # assign team membership
    for s in students:
        if s in opt['green']:
            cons.append(G[s] == True)
        elif s in opt['red']:
            cons.append(G[s] == False)
        else:
            # student not listed -> impossible
            cons.append(False)
    # facilitator flags
    for s in students:
        if s == opt['fac_green'] or s == opt['fac_red']:
            cons.append(F[s] == True)
        else:
            cons.append(F[s] == False)
    return cons

# Define options
options = {}
# A
options['A'] = {
    'green': ['Juana', 'Lateefah', 'Olga'],
    'red': ['Kelly', 'Mei'],
    'fac_green': 'Olga',
    'fac_red': 'Mei'
}
# B
options['B'] = {
    'green': ['Kelly', 'Lateefah', 'Olga'],
    'red': ['Juana', 'Mei'],
    'fac_green': 'Lateefah',
    'fac_red': 'Mei'
}
# C
options['C'] = {
    'green': ['Kelly', 'Lateefah', 'Olga'],
    'red': ['Juana', 'Mei'],
    'fac_green': 'Olga',
    'fac_red': 'Juana'
}
# D
options['D'] = {
    'green': ['Kelly', 'Mei', 'Olga'],
    'red': ['Juana', 'Lateefah'],
    'fac_green': 'Olga',
    'fac_red': 'Juana'
}
# E
options['E'] = {
    'green': ['Lateefah', 'Olga'],
    'red': ['Juana', 'Kelly', 'Mei'],
    'fac_green': 'Olga',
    'fac_red': 'Kelly'
}

found_options = []
for letter, opt in options.items():
    solver.push()
    solver.add(option_constraints(opt))
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