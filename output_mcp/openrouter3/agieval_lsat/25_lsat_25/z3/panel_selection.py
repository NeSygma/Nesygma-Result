from z3 import *

# Define all scientists
scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
# Create boolean variables for selection
selected = {s: Bool(f'selected_{s}') for s in scientists}

# Base constraints
solver = Solver()

# Constraint 1: Exactly 5 scientists selected
solver.add(Sum([If(selected[s], 1, 0) for s in scientists]) == 5)

# Constraint 2: At least one of each type
botanists = ['F', 'G', 'H']
chemists = ['K', 'L', 'M']
zoologists = ['P', 'Q', 'R']

solver.add(Or([selected[b] for b in botanists]))  # At least one botanist
solver.add(Or([selected[c] for c in chemists]))  # At least one chemist
solver.add(Or([selected[z] for z in zoologists]))  # At least one zoologist

# Constraint 3: If more than one botanist, then at most one zoologist
# More than one botanist means at least 2 botanists
botanist_count = Sum([If(selected[b], 1, 0) for b in botanists])
zoologist_count = Sum([If(selected[z], 1, 0) for z in zoologists])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# Constraint 4: F and K cannot both be selected
solver.add(Or(Not(selected['F']), Not(selected['K'])))

# Constraint 5: K and M cannot both be selected
solver.add(Or(Not(selected['K']), Not(selected['M'])))

# Constraint 6: If M is selected, both P and R must be selected
solver.add(Implies(selected['M'], And(selected['P'], selected['R'])))

# Now evaluate each option
found_options = []

# Option A: F, G, K, P, Q
opt_a_constr = And(
    selected['F'], selected['G'], selected['K'], selected['P'], selected['Q'],
    Not(selected['H']), Not(selected['L']), Not(selected['M']), Not(selected['R'])
)

# Option B: G, H, K, L, M
opt_b_constr = And(
    selected['G'], selected['H'], selected['K'], selected['L'], selected['M'],
    Not(selected['F']), Not(selected['P']), Not(selected['Q']), Not(selected['R'])
)

# Option C: G, H, K, L, R
opt_c_constr = And(
    selected['G'], selected['H'], selected['K'], selected['L'], selected['R'],
    Not(selected['F']), Not(selected['M']), Not(selected['P']), Not(selected['Q'])
)

# Option D: H, K, M, P, R
opt_d_constr = And(
    selected['H'], selected['K'], selected['M'], selected['P'], selected['R'],
    Not(selected['F']), Not(selected['G']), Not(selected['L']), Not(selected['Q'])
)

# Option E: H, L, M, P, Q
opt_e_constr = And(
    selected['H'], selected['L'], selected['M'], selected['P'], selected['Q'],
    Not(selected['F']), Not(selected['G']), Not(selected['K']), Not(selected['R'])
)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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