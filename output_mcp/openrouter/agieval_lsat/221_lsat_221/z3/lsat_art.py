from z3 import *

solver = Solver()

students = ['Franz', 'Greene', 'Hidalgo', 'Isaacs']
types = ['oil', 'water']  # water for watercolor

# Create variables for each painting: wall (1-4) and position (True=upper, False=lower)
wall = {}
pos = {}
for s in students:
    for t in types:
        var_w = Int(f"w_{s}_{t}")
        var_p = Bool(f"p_{s}_{t}")
        wall[(s,t)] = var_w
        pos[(s,t)] = var_p
        solver.add(var_w >= 1, var_w <= 4)

# Uniqueness: no two paintings share same wall and same position
pairs = [(s1,t1,s2,t2) for s1 in students for t1 in types for s2 in students for t2 in types if (s1,t1) < (s2,t2)]
for s1,t1,s2,t2 in pairs:
    solver.add(Or(wall[(s1,t1)] != wall[(s2,t2)], pos[(s1,t1)] != pos[(s2,t2)]))

# Per wall constraints
for w in range(1,5):
    # exactly one upper and one lower
    upper_cnt = Sum([If(And(wall[(s,t)] == w, pos[(s,t)] == True), 1, 0) for s in students for t in types])
    lower_cnt = Sum([If(And(wall[(s,t)] == w, pos[(s,t)] == False), 1, 0) for s in students for t in types])
    solver.add(upper_cnt == 1)
    solver.add(lower_cnt == 1)
    # exactly two paintings per wall (redundant)
    total_cnt = Sum([If(wall[(s,t)] == w, 1, 0) for s in students for t in types])
    solver.add(total_cnt == 2)
    # at least one oil per wall
    oil_cnt = Sum([If(And(wall[(s,t)] == w, t == 'oil'), 1, 0) for s in students for t in types])
    solver.add(oil_cnt >= 1)
    # No wall has both Franz and Isaacs
    franz_on = Or(wall[('Franz','oil')] == w, wall[('Franz','water')] == w)
    isaacs_on = Or(wall[('Isaacs','oil')] == w, wall[('Isaacs','water')] == w)
    solver.add(Not(And(franz_on, isaacs_on)))
    # No student has both paintings on same wall (ensures two different students per wall)
    for s in students:
        solver.add(Not(And(wall[(s,'oil')] == w, wall[(s,'water')] == w)))

# Specific constraints
# Greene's watercolor is upper on same wall as Franz's oil (and Franz's oil must be lower)
solver.add(wall[('Greene','water')] == wall[('Franz','oil')])
solver.add(pos[('Greene','water')] == True)
solver.add(pos[('Franz','oil')] == False)
# Isaacs's oil lower on wall 4
solver.add(wall[('Isaacs','oil')] == 4)
solver.add(pos[('Isaacs','oil')] == False)
# Hidalgo's oil on wall 2 (given premise)
solver.add(wall[('Hidalgo','oil')] == 2)
# Position of Hidalgo's oil can be either; no constraint

# Define option constraints
options = []
# A: Franz's oil on wall 2
opt_a = wall[('Franz','oil')] == 2
options.append(("A", opt_a))
# B: Greene's watercolor on wall 2
opt_b = wall[('Greene','water')] == 2
options.append(("B", opt_b))
# C: Greene's oil on wall 2
opt_c = wall[('Greene','oil')] == 2
options.append(("C", opt_c))
# D: Hidalgo's watercolor on wall 2
opt_d = wall[('Hidalgo','water')] == 2
options.append(("D", opt_d))
# E: Isaacs's watercolor on wall 2
opt_e = wall[('Isaacs','water')] == 2
options.append(("E", opt_e))

found_options = []
for letter, constr in options:
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