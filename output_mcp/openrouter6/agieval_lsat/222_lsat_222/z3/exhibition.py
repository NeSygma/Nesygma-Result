from z3 import *

solver = Solver()

# Students
students = ['F', 'G', 'H', 'I']

# Wall variables for each painting (oil and watercolor)
wall = { (s, t): Int(f'wall_{s}_{t}') for s in students for t in ['oil', 'water'] }
# Position variables: 0 = upper, 1 = lower
pos = { (s, t): Int(f'pos_{s}_{t}') for s in students for t in ['oil', 'water'] }

# Domain constraints: walls 1-4, positions 0 or 1
for s in students:
    for t in ['oil', 'water']:
        solver.add(wall[(s, t)] >= 1, wall[(s, t)] <= 4)
        solver.add(pos[(s, t)] >= 0, pos[(s, t)] <= 1)

# Each wall has exactly one oil and one watercolor
for w in range(1, 5):
    oil_count = Sum([If(wall[(s, 'oil')] == w, 1, 0) for s in students])
    water_count = Sum([If(wall[(s, 'water')] == w, 1, 0) for s in students])
    solver.add(oil_count == 1)
    solver.add(water_count == 1)

# Each student's two paintings on different walls
for s in students:
    solver.add(wall[(s, 'oil')] != wall[(s, 'water')])

# No wall has both Franz and Isaacs paintings
for w in range(1, 5):
    # Count Franz+Isaacs paintings on wall w
    franz_isaacs = Sum([
        If(wall[('F', 'oil')] == w, 1, 0),
        If(wall[('F', 'water')] == w, 1, 0),
        If(wall[('I', 'oil')] == w, 1, 0),
        If(wall[('I', 'water')] == w, 1, 0)
    ])
    solver.add(franz_isaacs <= 1)

# Greene's watercolor is upper on the wall where Franz's oil is displayed
solver.add(wall[('G', 'water')] == wall[('F', 'oil')])
solver.add(pos[('G', 'water')] == 0)

# Isaacs's oil is lower on wall 4
solver.add(wall[('I', 'oil')] == 4)
solver.add(pos[('I', 'oil')] == 1)

# Additional assumption: Greene's oil on same wall as Franz's watercolor
solver.add(wall[('G', 'oil')] == wall[('F', 'water')])

# Ensure opposite positions on each wall (one upper, one lower)
for w in range(1, 5):
    oil_pos = Sum([If(wall[(s, 'oil')] == w, pos[(s, 'oil')], 0) for s in students])
    water_pos = Sum([If(wall[(s, 'water')] == w, pos[(s, 'water')], 0) for s in students])
    solver.add(oil_pos != water_pos)

# Now evaluate answer choices
found_options = []

# Option A: Greene's oil is displayed in an upper position
opt_a = (pos[('G', 'oil')] == 0)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor
opt_b = (wall[('H', 'water')] == wall[('I', 'water')])
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Hidalgo's oil is displayed in an upper position
opt_c = (pos[('H', 'oil')] == 0)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Hidalgo's oil is displayed on the same wall as Isaacs's watercolor
opt_d = (wall[('H', 'oil')] == wall[('I', 'water')])
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Isaacs's watercolor is displayed in a lower position
opt_e = (pos[('I', 'water')] == 1)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")