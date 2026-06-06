from z3 import *

# Candidates
candidates = ['J', 'K', 'L', 'N', 'O']
# Countries
countries = ['V', 'Y', 'Z']

# Variables: assigned_to_country[country] = candidate
# We use an integer representation: 0:J, 1:K, 2:L, 3:N, 4:O
assigned_to_country = [Int(f'country_{c}') for c in countries]

solver = Solver()

# Each country gets a candidate
for c in assigned_to_country:
    solver.add(c >= 0, c < 5)

# No ambassador assigned to more than one country (all distinct)
solver.add(Distinct(assigned_to_country))

# Helper: is_assigned[p]
def is_assigned(p_idx):
    return Or([assigned_to_country[i] == p_idx for i in range(3)])

# Constraint 3: Either K or N, but not both, is assigned.
# K is 1, N is 3
solver.add(Xor(is_assigned(1), is_assigned(3)))

# Constraint 4: If J is assigned, then K is assigned.
# J is 0, K is 1
solver.add(Implies(is_assigned(0), is_assigned(1)))

# Constraint 5: If O is assigned to V, K is not assigned to Y.
# O is 4, V is 0, Y is 1
solver.add(Implies(assigned_to_country[0] == 4, assigned_to_country[1] != 1))

# Constraint 6: If L is assigned, it is to Z.
# L is 2, Z is 2
solver.add(Implies(is_assigned(2), assigned_to_country[2] == 2))

# Options
# (A) J and N (0, 3)
# (B) J and O (0, 4)
# (C) K and L (1, 2)
# (D) K and N (1, 3)
# (E) L and O (2, 4)

options = [
    ("A", [0, 3]),
    ("B", [0, 4]),
    ("C", [1, 2]),
    ("D", [1, 3]),
    ("E", [2, 4])
]

found_options = []
for letter, unassigned in options:
    solver.push()
    # Add constraint: these two are NOT assigned
    for p in unassigned:
        solver.add(Not(is_assigned(p)))
    # The other three MUST be assigned
    assigned = [p for p in range(5) if p not in unassigned]
    for p in assigned:
        solver.add(is_assigned(p))
    
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