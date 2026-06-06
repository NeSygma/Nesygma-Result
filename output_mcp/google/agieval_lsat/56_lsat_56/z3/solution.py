from z3 import *

# Candidates and Countries
candidates = ['J', 'K', 'L', 'N', 'O']
countries = ['V', 'Y', 'Z']

# Variables: is_assigned_to[candidate][country]
# Using a dictionary for easy access
is_assigned_to = {}
for c in candidates:
    for country in countries:
        is_assigned_to[(c, country)] = Bool(f"assign_{c}_{country}")

# Helper: is_assigned[candidate]
is_assigned = {}
for c in candidates:
    is_assigned[c] = Or([is_assigned_to[(c, country)] for country in countries])

solver = Solver()

# 1. Each country has exactly one ambassador
for country in countries:
    solver.add(Sum([If(is_assigned_to[(c, country)], 1, 0) for c in candidates]) == 1)

# 2. Each candidate has at most one country
for c in candidates:
    solver.add(Sum([If(is_assigned_to[(c, country)], 1, 0) for country in countries]) <= 1)

# 3. Either K or N, but not both, is assigned
solver.add(Xor(is_assigned['K'], is_assigned['N']))

# 4. If J is assigned, then K is assigned
solver.add(Implies(is_assigned['J'], is_assigned['K']))

# 5. If O is assigned to V, K is not assigned to Y
solver.add(Implies(is_assigned_to[('O', 'V')], Not(is_assigned_to[('K', 'Y')])))

# 6. If L is assigned, it is to Z
solver.add(Implies(is_assigned['L'], is_assigned_to[('L', 'Z')]))

# Question: If O is assigned to V, who are the other two?
solver.add(is_assigned_to[('O', 'V')])

# Define the options
# (A) J and L
# (B) J and N
# (C) K and L
# (D) K and N
# (E) L and N

def check_option(c1, c2):
    # Check if c1 and c2 are the other two assigned ambassadors
    # The other two countries are Y and Z.
    # So, {c1, c2} must be the set of candidates assigned to Y and Z.
    
    # Get the candidates assigned to Y and Z
    # We need to find which candidates are assigned to Y and Z
    # Let's use a temporary solver to check if this specific assignment is possible
    s = Solver()
    s.add(solver.assertions())
    
    # Add the condition that c1 and c2 are the ones assigned to Y and Z
    # Specifically, one of them is at Y, one is at Z.
    # And no one else is at Y or Z.
    
    # Candidates assigned to Y and Z
    # We don't know which is at Y and which is at Z, so we check both permutations
    cond = Or(
        And(is_assigned_to[(c1, 'Y')], is_assigned_to[(c2, 'Z')]),
        And(is_assigned_to[(c2, 'Y')], is_assigned_to[(c1, 'Z')])
    )
    s.add(cond)
    
    return s.check() == sat

options = [
    ("A", "J", "L"),
    ("B", "J", "N"),
    ("C", "K", "L"),
    ("D", "K", "N"),
    ("E", "L", "N")
]

found_options = []
for letter, c1, c2 in options:
    if check_option(c1, c2):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")