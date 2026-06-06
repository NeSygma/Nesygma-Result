from z3 import *

solver = Solver()

students = ['F','G','H','I']
types = ['O','W']  # O=oil, W=watercolor

# Create variables for each painting
wall = {}
upper = {}
for s in students:
    for t in types:
        var_w = Int(f'wall_{s}{t}')
        var_u = Bool(f'upper_{s}{t}')
        wall[(s,t)] = var_w
        upper[(s,t)] = var_u
        solver.add(var_w >= 1, var_w <= 4)

# Helper: list of all paintings
paintings = [(s,t) for s in students for t in types]

# Constraint: each wall has exactly one upper and one lower painting
for w in range(1,5):
    upper_cnt = Sum([If(And(wall[p]==w, upper[p]), 1, 0) for p in paintings])
    lower_cnt = Sum([If(And(wall[p]==w, Not(upper[p])), 1, 0) for p in paintings])
    solver.add(upper_cnt == 1)
    solver.add(lower_cnt == 1)

# Constraint: No wall has only watercolors (i.e., at least one oil per wall)
oil_paintings = [(s,'O') for s in students]
for w in range(1,5):
    oil_cnt = Sum([If(And(wall[p]==w), 1, 0) for p in oil_paintings])
    solver.add(oil_cnt >= 1)

# Constraint: No wall has work of only one student (i.e., at most one painting per student per wall)
for s in students:
    for w in range(1,5):
        cnt = Sum([If(And(wall[p]==w), 1, 0) for p in paintings if p[0]==s])
        solver.add(cnt <= 1)

# Constraint: No wall has both Franz and Isaacs paintings
for w in range(1,5):
    f_cnt = Sum([If(And(wall[p]==w), 1, 0) for p in paintings if p[0]=='F'])
    i_cnt = Sum([If(And(wall[p]==w), 1, 0) for p in paintings if p[0]=='I'])
    solver.add(f_cnt * i_cnt == 0)

# Constraint: Greene's watercolor is upper on same wall as Franz's oil (lower)
solver.add(wall[('G','W')] == wall[('F','O')])
solver.add(upper[('G','W')] == True)
solver.add(upper[('F','O')] == False)

# Constraint: Isaacs's oil is lower on wall 4
solver.add(wall[('I','O')] == 4)
solver.add(upper[('I','O')] == False)

# Define option constraints
option_constraints = {}
# A: all F and G paintings lower
optA = And(upper[('F','O')]==False,
            upper[('F','W')]==False,
            upper[('G','O')]==False,
            upper[('G','W')]==False)
option_constraints['A'] = optA
# B: all F and G paintings upper
optB = And(upper[('F','O')]==True,
            upper[('F','W')]==True,
            upper[('G','O')]==True,
            upper[('G','W')]==True)
option_constraints['B'] = optB
# C: all F and H paintings upper
optC = And(upper[('F','O')]==True,
            upper[('F','W')]==True,
            upper[('H','O')]==True,
            upper[('H','W')]==True)
option_constraints['C'] = optC
# D: all G and H paintings lower
optD = And(upper[('G','O')]==False,
            upper[('G','W')]==False,
            upper[('H','O')]==False,
            upper[('H','W')]==False)
option_constraints['D'] = optD
# E: all G and H paintings upper
optE = And(upper[('G','O')]==True,
            upper[('G','W')]==True,
            upper[('H','O')]==True,
            upper[('H','W')]==True)
option_constraints['E'] = optE

found_options = []
for letter, constr in [('A', optA), ('B', optB), ('C', optC), ('D', optD), ('E', optE)]:
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