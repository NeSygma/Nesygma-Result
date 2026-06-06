from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Medium: Oil=0, Watercolor=1
# Walls: 1,2,3,4
# Position: Upper=0, Lower=1

# Each student has exactly one oil and one watercolor painting
# Each wall has exactly 2 paintings (one upper, one lower)
# So 8 paintings total, 2 per wall

# Variables: painting[student][medium] = (wall, position)
# wall: 1-4, position: 0=upper, 1=lower

wall = [[Int(f'wall_{s}_{m}') for m in range(2)] for s in range(4)]
pos = [[Int(f'pos_{s}_{m}') for m in range(2)] for s in range(4)]

# Domain constraints
for s in range(4):
    for m in range(2):
        solver.add(Or([wall[s][m] == w for w in range(1, 5)]))
        solver.add(Or(pos[s][m] == 0, pos[s][m] == 1))

# Each wall has exactly 2 paintings (one upper, one lower)
for w in range(1, 5):
    # Count paintings on wall w
    on_wall = []
    for s in range(4):
        for m in range(2):
            on_wall.append(If(wall[s][m] == w, 1, 0))
    solver.add(Sum(on_wall) == 2)
    
    # Count upper positions on wall w
    upper_on_wall = []
    for s in range(4):
        for m in range(2):
            upper_on_wall.append(If(And(wall[s][m] == w, pos[s][m] == 0), 1, 0))
    solver.add(Sum(upper_on_wall) == 1)
    
    # Count lower positions on wall w
    lower_on_wall = []
    for s in range(4):
        for m in range(2):
            lower_on_wall.append(If(And(wall[s][m] == w, pos[s][m] == 1), 1, 0))
    solver.add(Sum(lower_on_wall) == 1)

# No wall has only watercolors displayed on it.
# This means for each wall, at least one painting is oil.
for w in range(1, 5):
    oil_on_wall = []
    for s in range(4):
        oil_on_wall.append(If(wall[s][0] == w, 1, 0))  # medium 0 = oil
    solver.add(Sum(oil_on_wall) >= 1)

# No wall has the work of only one student displayed on it.
# This means for each wall, the two paintings must be by different students.
for w in range(1, 5):
    for s in range(4):
        # At most one painting by student s on wall w
        paintings_by_s = []
        for m in range(2):
            paintings_by_s.append(If(wall[s][m] == w, 1, 0))
        solver.add(Sum(paintings_by_s) <= 1)

# No wall has both a painting by Franz and a painting by Isaacs.
for w in range(1, 5):
    franz_on_wall = []
    for m in range(2):
        franz_on_wall.append(If(wall[0][m] == w, 1, 0))
    isaacs_on_wall = []
    for m in range(2):
        isaacs_on_wall.append(If(wall[3][m] == w, 1, 0))
    solver.add(Not(And(Sum(franz_on_wall) >= 1, Sum(isaacs_on_wall) >= 1)))

# Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(wall[1][1] == wall[0][0])  # Greene's watercolor on same wall as Franz's oil
solver.add(pos[1][1] == 0)  # Greene's watercolor in upper position

# Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[3][0] == 4)  # Isaacs's oil on wall 4
solver.add(pos[3][0] == 1)  # Isaacs's oil in lower position

# Franz's oil is displayed on wall 1 (given condition)
solver.add(wall[0][0] == 1)

# Define option constraints
# (A) Franz's watercolor is displayed on wall 4.
opt_a = (wall[0][1] == 4)

# (B) Greene's oil is displayed on wall 2.
opt_b = (wall[1][0] == 2)

# (C) Greene's watercolor is displayed on wall 2.
opt_c = (wall[1][1] == 2)

# (D) Hidalgo's watercolor is displayed on wall 3.
opt_d = (wall[2][1] == 3)

# (E) Isaacs's oil is displayed on wall 1.
opt_e = (wall[3][0] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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