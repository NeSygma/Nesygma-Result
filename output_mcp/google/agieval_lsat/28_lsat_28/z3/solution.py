from z3 import *

# Define variables
scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
vars = {s: Bool(s) for s in scientists}

# Define groups
botanists = [vars['F'], vars['G'], vars['H']]
chemists = [vars['K'], vars['L'], vars['M']]
zoologists = [vars['P'], vars['Q'], vars['R']]

solver = Solver()

# 1. Panel size is 5
solver.add(Sum([If(vars[s], 1, 0) for s in scientists]) == 5)

# 2. At least one of each type
solver.add(Sum([If(b, 1, 0) for b in botanists]) >= 1)
solver.add(Sum([If(c, 1, 0) for c in chemists]) >= 1)
solver.add(Sum([If(z, 1, 0) for z in zoologists]) >= 1)

# 3. If more than one botanist, at most one zoologist
solver.add(Implies(Sum([If(b, 1, 0) for b in botanists]) > 1, Sum([If(z, 1, 0) for z in zoologists]) <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(vars['F'], vars['K'])))

# 5. K and M cannot both be selected
solver.add(Not(And(vars['K'], vars['M'])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(vars['M'], And(vars['P'], vars['R'])))

# Question condition: P is the only zoologist selected
# This means P=True, Q=False, R=False
solver.add(vars['P'] == True)
solver.add(vars['Q'] == False)
solver.add(vars['R'] == False)

# Define options
# (A) If K is selected, G cannot be selected.
opt_a = Implies(vars['K'], Not(vars['G']))
# (B) If L is selected, F cannot be selected.
opt_b = Implies(vars['L'], Not(vars['F']))
# (C) If exactly one chemist is selected, it must be K.
opt_c = Implies(Sum([If(c, 1, 0) for c in chemists]) == 1, vars['K'])
# (D) If exactly two chemists are selected, F cannot be selected.
opt_d = Implies(Sum([If(c, 1, 0) for c in chemists]) == 2, Not(vars['F']))
# (E) If exactly two chemists are selected, G cannot be selected.
opt_e = Implies(Sum([If(c, 1, 0) for c in chemists]) == 2, Not(vars['G']))

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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