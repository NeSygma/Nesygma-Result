from z3 import *

solver = Solver()

# Variables for each painting: wall (1-4) and position (True=upper, False=lower)
paintings = {}
students = ['F', 'G', 'H', 'I']
types = ['oil', 'water']
for s in students:
    for t in types:
        var_w = Int(f'w_{s}_{t}')
        var_u = Bool(f'u_{s}_{t}')
        paintings[(s, t)] = (var_w, var_u)
        solver.add(var_w >= 1, var_w <= 4)
        # u is Bool, no need to bound

# Helper to get variables
def w(s, t):
    return paintings[(s, t)][0]
def u(s, t):
    return paintings[(s, t)][1]

# Base constraints
# Each wall has exactly one upper and one lower painting
for wall in range(1,5):
    upper_sum = Sum([If(And(w(s,t) == wall, u(s,t)), 1, 0) for s in students for t in types])
    lower_sum = Sum([If(And(w(s,t) == wall, Not(u(s,t))), 1, 0) for s in students for t in types])
    solver.add(upper_sum == 1)
    solver.add(lower_sum == 1)

# No wall has only watercolors: at least one oil per wall
oil_paintings = [(s,'oil') for s in students]
for wall in range(1,5):
    oil_count = Sum([If(w(s,'oil') == wall, 1, 0) for s in students])
    solver.add(oil_count >= 1)

# No wall has work of only one student: at most one painting per student per wall
for wall in range(1,5):
    for s in students:
        cnt = Sum([If(w(s,t) == wall, 1, 0) for t in types])
        solver.add(cnt <= 1)

# No wall has both Franz and Isaacs paintings
for wall in range(1,5):
    f_cnt = Sum([If(w('F',t) == wall, 1, 0) for t in types])
    i_cnt = Sum([If(w('I',t) == wall, 1, 0) for t in types])
    solver.add(f_cnt + i_cnt <= 1)

# Greene's watercolor is upper of wall where Franz's oil is displayed
solver.add(u('G','water') == True)
solver.add(w('G','water') == w('F','oil'))
solver.add(u('F','oil') == False)

# Isaacs's oil is lower of wall 4
solver.add(w('I','oil') == 4)
solver.add(u('I','oil') == False)

# Given condition: Franz's oil is on wall 1
solver.add(w('F','oil') == 1)
# This also forces Greene's watercolor wall 1 via above equality

# Define option constraints
opt_a_constr = (w('F','water') == 4)
opt_b_constr = (w('G','oil') == 2)
opt_c_constr = (w('G','water') == 2)
opt_d_constr = (w('H','water') == 3)
opt_e_constr = (w('I','oil') == 1)

found_options = []
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