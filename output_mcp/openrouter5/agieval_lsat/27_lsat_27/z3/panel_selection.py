from z3 import *

# We have 9 scientists: F,G,H (botanists), K,L,M (chemists), P,Q,R (zoologists)
# We need to select exactly 5 scientists (4 are given: F, L, Q, R, so we need the 5th)
# Let's model selection with boolean variables for each scientist

scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
selected = {s: Bool(f'selected_{s}') for s in scientists}

solver = Solver()

# Exactly 5 scientists selected
solver.add(Sum([If(selected[s], 1, 0) for s in scientists]) == 5)

# The four given scientists are selected
solver.add(selected['F'] == True)
solver.add(selected['L'] == True)
solver.add(selected['Q'] == True)
solver.add(selected['R'] == True)

# Condition 1: At least one of each type
botanists = ['F', 'G', 'H']
chemists = ['K', 'L', 'M']
zoologists = ['P', 'Q', 'R']

solver.add(Sum([If(selected[s], 1, 0) for s in botanists]) >= 1)
solver.add(Sum([If(selected[s], 1, 0) for s in chemists]) >= 1)
solver.add(Sum([If(selected[s], 1, 0) for s in zoologists]) >= 1)

# Condition 2: If more than one botanist is selected, then at most one zoologist is selected
num_botanists = Sum([If(selected[s], 1, 0) for s in botanists])
num_zoologists = Sum([If(selected[s], 1, 0) for s in zoologists])
solver.add(Implies(num_botanists > 1, num_zoologists <= 1))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(selected['F'], selected['K'])))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(selected['K'], selected['M'])))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(selected['M'], And(selected['P'], selected['R'])))

# Now evaluate each option for the 5th scientist
# Options: (A) G, (B) H, (C) K, (D) M, (E) P

options = [
    ("A", selected['G']),
    ("B", selected['H']),
    ("C", selected['K']),
    ("D", selected['M']),
    ("E", selected['P'])
]

found_options = []
for letter, constr in options:
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