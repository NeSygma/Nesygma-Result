from z3 import *

# Countries: 0=V, 1=Y, 2=Z
# Candidates: J, K, L, N, O
# assigned_to[c] = 0, 1, 2 (country) or 3 (None)

candidates = ['J', 'K', 'L', 'N', 'O']
assigned_to = {c: Int(f'assigned_to_{c}') for c in candidates}
is_assigned = {c: Bool(f'is_assigned_{c}') for c in candidates}

solver = Solver()

# Domain constraints
for c in candidates:
    solver.add(assigned_to[c] >= 0, assigned_to[c] <= 3)
    solver.add(is_assigned[c] == (assigned_to[c] != 3))

# Exactly 3 candidates assigned
solver.add(Sum([If(is_assigned[c], 1, 0) for c in candidates]) == 3)

# Each country has exactly one ambassador
for country in range(3):
    solver.add(Sum([If(assigned_to[c] == country, 1, 0) for c in candidates]) == 1)

# Constraint 3: Either K or N, but not both, is assigned
solver.add(Xor(is_assigned['K'], is_assigned['N']))

# Constraint 4: If J is assigned, then K is assigned
solver.add(Implies(is_assigned['J'], is_assigned['K']))

# Constraint 5: If O is assigned to V (0), K is not assigned to Y (1)
solver.add(Implies(assigned_to['O'] == 0, assigned_to['K'] != 1))

# Constraint 6: If L is assigned, it is to Z (2)
solver.add(Implies(is_assigned['L'], assigned_to['L'] == 2))

# Options
# (A) J is assigned to Z (2)
# (B) K is assigned to Z (2)
# (C) N is assigned to Z (2)
# (D) L is not assigned
# (E) O is not assigned

options = [
    ("A", assigned_to['J'] == 2),
    ("B", assigned_to['K'] == 2),
    ("C", assigned_to['N'] == 2),
    ("D", Not(is_assigned['L'])),
    ("E", Not(is_assigned['O']))
]

# We want to find which one CANNOT be true.
# This means we check if adding the option to the solver makes it UNSAT.
# If it's UNSAT, then it CANNOT be true.

results = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        results.append(letter)
    solver.pop()

print(f"STATUS: sat")
print(f"Options that cannot be true: {results}")