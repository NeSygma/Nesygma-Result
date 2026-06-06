from z3 import *

# Define variables
scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
s = {name: Bool(name) for name in scientists}

# Define types
botanists = [s['F'], s['G'], s['H']]
chemists = [s['K'], s['L'], s['M']]
zoologists = [s['P'], s['Q'], s['R']]

solver = Solver()

# 1. Panel size is 5
solver.add(Sum([If(s[name], 1, 0) for name in scientists]) == 5)

# 2. At least one of each type
solver.add(Sum([If(b, 1, 0) for b in botanists]) >= 1)
solver.add(Sum([If(c, 1, 0) for c in chemists]) >= 1)
solver.add(Sum([If(z, 1, 0) for z in zoologists]) >= 1)

# 3. If > 1 botanist, then <= 1 zoologist
solver.add(Implies(Sum([If(b, 1, 0) for b in botanists]) > 1, Sum([If(z, 1, 0) for z in zoologists]) <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(s['F'], s['K'])))

# 5. K and M cannot both be selected
solver.add(Not(And(s['K'], s['M'])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(s['M'], And(s['P'], s['R'])))

# Question: If F, L, Q, R are selected, who is the 5th?
# F, L, Q, R are True
solver.add(s['F'] == True)
solver.add(s['L'] == True)
solver.add(s['Q'] == True)
solver.add(s['R'] == True)

# Test each option
options = [('A', 'G'), ('B', 'H'), ('C', 'K'), ('D', 'M'), ('E', 'P')]
found_options = []

for letter, name in options:
    solver.push()
    solver.add(s[name] == True)
    # Ensure no other scientist is selected (total 5)
    # We already have F, L, Q, R (4) + name (1) = 5.
    # So all others must be False.
    for other in scientists:
        if other not in ['F', 'L', 'Q', 'R', name]:
            solver.add(s[other] == False)
            
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