from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P
# Each house gets a position 1-7 (all different)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions are between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All positions are distinct
solver.add(Distinct([pos[h] for h in houses]))

# Time periods:
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

# Constraint 1: J must be shown in the evening
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Constraint 2: K cannot be shown in the morning
solver.add(And(pos['K'] != 1, pos['K'] != 2))

# Constraint 3: L must be shown after K and before M (K < L < M)
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Define helper functions for time periods
def is_morning(h):
    return Or(pos[h] == 1, pos[h] == 2)

def is_afternoon(h):
    return Or(pos[h] == 3, pos[h] == 4, pos[h] == 5)

def is_evening(h):
    return Or(pos[h] == 6, pos[h] == 7)

# Define answer options
opt_a = is_evening('K')          # K is shown in the evening
opt_b = is_afternoon('L')        # L is shown in the afternoon
opt_c = is_evening('L')          # L is shown in the evening
opt_d = is_morning('M')          # M is shown in the morning
opt_e = is_afternoon('M')        # M is shown in the afternoon

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For "must be true" questions, an option must hold in ALL valid models.
# An option "must be true" iff its negation is unsatisfiable given the constraints.
# We check: which options are such that adding NOT(option) makes the problem unsat?

must_be_true = []
for letter, constr in options:
    s = Solver()
    # Add all base constraints
    for c in solver.assertions():
        s.add(c)
    # Add negation of the option
    s.add(Not(constr))
    if s.check() == unsat:
        must_be_true.append(letter)

print(f"Options that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")