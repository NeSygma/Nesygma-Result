from z3 import *

# Photographers
photographers = ['F', 'G', 'H', 'K', 'L', 'M']
# Positions: 0: None, 1: Silva, 2: Thorne
pos = {p: Int(f'pos_{p}') for p in photographers}

solver = Solver()

# Domain constraints
for p in photographers:
    solver.add(pos[p] >= 0, pos[p] <= 2)

# Constraint 1: At least two photographers at Silva (1)
solver.add(Sum([If(pos[p] == 1, 1, 0) for p in photographers]) >= 2)

# Constraint 2: At least two photographers at Thorne (2)
solver.add(Sum([If(pos[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 4: Frost (F) and Heideck (H) must be together
solver.add(pos['F'] == pos['H'])

# Constraint 5: If Lai (L) and Mays (M) are both assigned, they must be in different ceremonies
solver.add(Implies(And(pos['L'] != 0, pos['M'] != 0), pos['L'] != pos['M']))

# Constraint 6: If Gonzalez (G) is in Silva (1), then Lai (L) must be in Thorne (2)
solver.add(Implies(pos['G'] == 1, pos['L'] == 2))

# Constraint 7: If Knutson (K) is NOT in Thorne (2), then both Heideck (H) and Mays (M) must be in Thorne (2)
solver.add(Implies(pos['K'] != 2, And(pos['H'] == 2, pos['M'] == 2)))

# Define options
options = {
    "A": ['F', 'G', 'H', 'M'],
    "B": ['F', 'H', 'K', 'M'],
    "C": ['G', 'K', 'L'],
    "D": ['G', 'K', 'M'],
    "E": ['K', 'M']
}

found_options = []
for letter, thorne_set in options.items():
    solver.push()
    # Thorne set constraints
    for p in photographers:
        if p in thorne_set:
            solver.add(pos[p] == 2)
        else:
            solver.add(pos[p] != 2)
    
    if solver.check() == sat:
        # This option IS possible
        pass
    else:
        # This option IS NOT possible
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