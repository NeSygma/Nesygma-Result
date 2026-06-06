from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# Positions: 0 = upper, 1 = lower
positions = [0, 1]

# Variables: wall[student][medium] and pos[student][medium]
wall = {s: [Int(f'wall_{s}_oil'), Int(f'wall_{s}_water')] for s in students}
pos = {s: [Int(f'pos_{s}_oil'), Int(f'pos_{s}_water')] for s in students}

# Domain constraints
for s in students:
    for m in [0, 1]:
        solver.add(wall[s][m] >= 1, wall[s][m] <= 4)
        solver.add(pos[s][m] >= 0, pos[s][m] <= 1)

# Exactly two paintings on each wall (one upper, one lower)
for w in walls:
    for p in positions:
        count = Sum([If(And(wall[s][m] == w, pos[s][m] == p), 1, 0) for s in students for m in [0, 1]])
        solver.add(count == 1)

# No wall has only watercolors displayed on it.
for w in walls:
    oils_on_w = Sum([If(wall[s][0] == w, 1, 0) for s in students])
    solver.add(oils_on_w >= 1)

# No wall has the work of only one student displayed on it.
for w in walls:
    students_on_w = Sum([If(Or(wall[s][0] == w, wall[s][1] == w), 1, 0) for s in students])
    solver.add(students_on_w >= 2)

# No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in walls:
    solver.add(Not(And(Or(wall['F'][0] == w, wall['F'][1] == w),
                       Or(wall['I'][0] == w, wall['I'][1] == w))))

# Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(pos['G'][1] == 0)
solver.add(wall['G'][1] == wall['F'][0])

# Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall['I'][0] == 4)
solver.add(pos['I'][0] == 1)

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    for s in students:
        for m_idx, m_name in enumerate(['oil', 'water']):
            print(f"  {s} {m_name}: wall={m[wall[s][m_idx]]}, pos={'upper' if m[pos[s][m_idx]] == 0 else 'lower'}")
else:
    print("Base constraints are UNSAT!")
    exit()

# Now let's check each option more carefully.
# The question asks: "Which one of the following CANNOT be true?"
# So we need to find which option is IMPOSSIBLE (unsat) under the base constraints.

# Let's check each option individually
solver.push()
solver.add(wall['F'][1] == wall['G'][0])
print(f"\nOption A (Franz water = Greene oil wall): {solver.check()}")
solver.pop()

solver.push()
solver.add(wall['F'][1] == wall['H'][0])
print(f"Option B (Franz water = Hidalgo oil wall): {solver.check()}")
solver.pop()

solver.push()
solver.add(pos['G'][0] == 0)
print(f"Option C (Greene oil upper): {solver.check()}")
solver.pop()

solver.push()
solver.add(pos['H'][1] == 1)
print(f"Option D (Hidalgo water lower): {solver.check()}")
solver.pop()

solver.push()
solver.add(wall['I'][1] == wall['H'][0])
print(f"Option E (Isaacs water = Hidalgo oil wall): {solver.check()}")
solver.pop()