from z3 import *

# Candidates and Countries
candidates = ['J', 'K', 'L', 'N', 'O']
countries = ['V', 'Y', 'Z']

# Variables: Assign[c][country] is True if candidate c is assigned to country
Assign = [[Bool(f'Assign_{c}_{country}') for country in countries] for c in candidates]
# Helper: IsAssigned[c] is True if candidate c is assigned to any country
IsAssigned = [Or([Assign[i][j] for j in range(len(countries))]) for i in range(len(candidates))]

# Map names to indices
idx = {name: i for i, name in enumerate(candidates)}
V, Y, Z = 0, 1, 2

def get_constraints():
    c = []
    # 1. One ambassador per country
    for j in range(len(countries)):
        c.append(Sum([If(Assign[i][j], 1, 0) for i in range(len(candidates))]) == 1)
    
    # 2. Each candidate assigned to at most one country
    for i in range(len(candidates)):
        c.append(Sum([If(Assign[i][j], 1, 0) for j in range(len(countries))]) <= 1)
        
    # 3. Either K or N, but not both
    c.append(Xor(IsAssigned[idx['K']], IsAssigned[idx['N']]))
    
    # 4. If O is assigned to V, K is not assigned to Y
    c.append(Implies(Assign[idx['O']][V], Not(Assign[idx['K']][Y])))
    
    # 5. If L is assigned, it is to Z
    c.append(Implies(IsAssigned[idx['L']], Assign[idx['L']][Z]))
    
    return c

# Original constraint: If J is assigned, then K is assigned
orig_constraint = Implies(IsAssigned[idx['J']], IsAssigned[idx['K']])

# Options
options = {
    "A": Implies(IsAssigned[idx['K']], IsAssigned[idx['J']]),
    "B": Implies(And(IsAssigned[idx['L']], IsAssigned[idx['O']]), IsAssigned[idx['N']]),
    "C": Implies(Not(IsAssigned[idx['O']]), IsAssigned[idx['K']]),
    "D": Not(And(IsAssigned[idx['J']], IsAssigned[idx['N']])),
    "E": Not(And(IsAssigned[idx['N']], IsAssigned[idx['O']]))
}

base_constraints = get_constraints()

# Verify if D is indeed the only one
found_options = []
for label, opt_constraint in options.items():
    s = Solver()
    s.add(base_constraints)
    s.add(Xor(orig_constraint, opt_constraint))
    if s.check() == unsat:
        found_options.append(label)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")