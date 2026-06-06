from z3 import *

# Define scientists
scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
botanists = ['F', 'G', 'H']
chemists = ['K', 'L', 'M']
zoologists = ['P', 'Q', 'R']

# Create boolean variables for each scientist
s = {name: Bool(name) for name in scientists}

# Solver
solver = Solver()

# 1. Panel size is 5
solver.add(Sum([If(s[name], 1, 0) for name in scientists]) == 5)

# 2. At least one of each type
solver.add(Sum([If(s[name], 1, 0) for name in botanists]) >= 1)
solver.add(Sum([If(s[name], 1, 0) for name in chemists]) >= 1)
solver.add(Sum([If(s[name], 1, 0) for name in zoologists]) >= 1)

# 3. If more than one botanist, at most one zoologist
solver.add(Implies(Sum([If(s[name], 1, 0) for name in botanists]) > 1, 
                   Sum([If(s[name], 1, 0) for name in zoologists]) <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(s['F'], s['K'])))

# 5. K and M cannot both be selected
solver.add(Not(And(s['K'], s['M'])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(s['M'], And(s['P'], s['R'])))

# Define options
options = {
    "A": ['F', 'G', 'K', 'P', 'Q'],
    "B": ['G', 'H', 'K', 'L', 'M'],
    "C": ['G', 'H', 'K', 'L', 'R'],
    "D": ['H', 'K', 'M', 'P', 'R'],
    "E": ['H', 'L', 'M', 'P', 'Q']
}

found_options = []
for letter, selected in options.items():
    solver.push()
    # Add constraints for this specific selection
    for name in scientists:
        if name in selected:
            solver.add(s[name] == True)
        else:
            solver.add(s[name] == False)
    
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