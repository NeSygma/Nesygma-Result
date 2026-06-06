from z3 import *

solver = Solver()

# Declare variables
I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

# Domain constraints: each target is 1, 2, or 3 days
domain = [And(1 <= var, var <= 3) for var in [I_w, I_v, S_w, S_v, T_w, T_v]]
solver.add(domain)

# Base constraints
# 1. Website target <= Voicemail target for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# 2. Image's voicemail target is shorter than the other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# 3. Solide's website target is shorter than Truvest's website target
solver.add(S_w < T_w)

# Helper to generate "at least two of these variables equal to value"
def at_least_two(vars_list, value):
    # Sum of indicators >= 2
    return Sum([If(var == value, 1, 0) for var in vars_list]) >= 2

# Define options
# For each option, we need to check if it's possible to have at least two clients with that target.
# If not possible, then that target cannot be set for more than one client.
options = [
    ("A", at_least_two([I_w, S_w, T_w], 1)),  # 1-day website target
    ("B", at_least_two([I_v, S_v, T_v], 2)),  # 2-day voicemail target
    ("C", at_least_two([I_w, S_w, T_w], 2)),  # 2-day website target
    ("D", at_least_two([I_v, S_v, T_v], 3)),  # 3-day voicemail target
    ("E", at_least_two([I_w, S_w, T_w], 3)),  # 3-day website target
]

found_unsat = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        found_unsat.append(letter)
    solver.pop()

if len(found_unsat) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat[0]}")
elif len(found_unsat) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_unsat}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")