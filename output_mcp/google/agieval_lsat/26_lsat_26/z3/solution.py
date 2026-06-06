from z3 import *

# Define variables
scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
s = {name: Bool(name) for name in scientists}

solver = Solver()

# 1. Panel size is 5
solver.add(Sum([If(s[name], 1, 0) for name in scientists]) == 5)

# 2. At least one of each type
botanists = ['F', 'G', 'H']
chemists = ['K', 'L', 'M']
zoologists = ['P', 'Q', 'R']

solver.add(Sum([If(s[name], 1, 0) for name in botanists]) >= 1)
solver.add(Sum([If(s[name], 1, 0) for name in chemists]) >= 1)
solver.add(Sum([If(s[name], 1, 0) for name in zoologists]) >= 1)

# 3. If more than one botanist is selected, then at most one zoologist is selected
solver.add(Implies(Sum([If(s[name], 1, 0) for name in botanists]) > 1, 
                   Sum([If(s[name], 1, 0) for name in zoologists]) <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(s['F'], s['K'])))

# 5. K and M cannot both be selected
solver.add(Not(And(s['K'], s['M'])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(s['M'], And(s['P'], s['R'])))

# Question condition: M is the only chemist selected
# M is selected, K is not, L is not
solver.push()
solver.add(s['M'] == True)
solver.add(s['K'] == False)
solver.add(s['L'] == False)

# Options
options = {
    "A": And(s['F'], s['G']),
    "B": And(s['G'], s['H']),
    "C": And(s['H'], s['P']),
    "D": And(s['F'], s['G'], s['H']),
    "E": And(s['P'], s['Q'], s['R'])
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

print(f"STATUS: sat")
print(f"answer:{found_options[0] if len(found_options) == 1 else found_options}")
solver.pop()