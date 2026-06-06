from z3 import *

# Employees
employees = ['M', 'O', 'P', 'S', 'T', 'W', 'Y', 'Z']
vars = {e: Bool(e) for e in employees}

# Constraints
# 1. If Myers is on the team, neither Ortega nor Paine can be.
# M -> (not O and not P)
c1 = Implies(vars['M'], And(Not(vars['O']), Not(vars['P'])))

# 2. If Schmidt is on the team, both Paine and Thomson must also be.
# S -> (P and T)
c2 = Implies(vars['S'], And(vars['P'], vars['T']))

# 3. If Wong is on the team, both Myers and Yoder must also be.
# W -> (M and Y)
c3 = Implies(vars['W'], And(vars['M'], vars['Y']))

# Team size: at least four
team_size = Sum([If(vars[e], 1, 0) for e in employees])
c_size = team_size >= 4

# All constraints
all_constraints = And(c1, c2, c3, c_size)

# Options
options = [
    ("A", vars['O'], vars['S']),
    ("B", vars['O'], vars['W']),
    ("C", vars['P'], vars['S']),
    ("D", vars['T'], vars['Y']),
    ("E", vars['Y'], vars['Z'])
]

# We want to find the pair (X, Y) such that it is NOT possible to have a valid team
# where both X and Y are NOT on the team.
# i.e., For all valid teams, (X or Y) is true.
# i.e., There is no valid team where (not X and not Y).

found_options = []
for letter, x, y in options:
    solver = Solver()
    solver.add(all_constraints)
    # Add the condition that both are NOT on the team
    solver.add(Not(x), Not(y))
    
    # If this is UNSAT, then it's impossible to have a team without X or Y.
    # Therefore, at least one of them MUST be on the team.
    if solver.check() == unsat:
        found_options.append(letter)

print(f"STATUS: sat")
print(f"answer:{found_options[0]}")