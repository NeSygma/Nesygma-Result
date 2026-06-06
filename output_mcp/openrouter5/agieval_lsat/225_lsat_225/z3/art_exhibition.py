from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# Positions: 0 = upper, 1 = lower
positions = [0, 1]

# Each student has exactly two paintings: an oil and a watercolor.
# We'll model each painting as a pair (wall, position).
# For each student s and each medium m (0=oil, 1=watercolor), we have variables:
# wall_s_m = which wall (1-4)
# pos_s_m = which position (0=upper, 1=lower)

# Variables: wall[student][medium] and pos[student][medium]
wall = {s: [Int(f'wall_{s}_oil'), Int(f'wall_{s}_water')] for s in students}
pos = {s: [Int(f'pos_{s}_oil'), Int(f'pos_{s}_water')] for s in students}

# Domain constraints
for s in students:
    for m in [0, 1]:
        solver.add(wall[s][m] >= 1, wall[s][m] <= 4)
        solver.add(pos[s][m] >= 0, pos[s][m] <= 1)

# Exactly two paintings on each wall (one upper, one lower)
# This means: for each wall w, exactly one oil and one watercolor are on that wall.
# Actually: exactly two paintings per wall, one upper and one lower.
# So each wall has exactly one painting in upper position and one in lower position.
# Across all 8 paintings (4 oils + 4 watercolors), they occupy 4 walls * 2 positions = 8 slots.

# Constraint: each wall has exactly one upper and one lower painting.
# We can encode: for each wall w and position p, exactly one painting is at (w, p).
for w in walls:
    for p in positions:
        # Count how many paintings are at (w, p)
        count = Sum([If(And(wall[s][m] == w, pos[s][m] == p), 1, 0) for s in students for m in [0, 1]])
        solver.add(count == 1)

# No wall has only watercolors displayed on it.
# i.e., each wall must have at least one oil.
for w in walls:
    oils_on_w = Sum([If(wall[s][0] == w, 1, 0) for s in students])
    solver.add(oils_on_w >= 1)

# No wall has the work of only one student displayed on it.
# i.e., each wall must have paintings by at least two different students.
for w in walls:
    students_on_w = Sum([If(Or(wall[s][0] == w, wall[s][1] == w), 1, 0) for s in students])
    solver.add(students_on_w >= 2)

# No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in walls:
    solver.add(Not(And(Or(wall['F'][0] == w, wall['F'][1] == w),
                       Or(wall['I'][0] == w, wall['I'][1] == w))))

# Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# So: pos['G'][1] == 0 (upper) and wall['G'][1] == wall['F'][0]
solver.add(pos['G'][1] == 0)
solver.add(wall['G'][1] == wall['F'][0])

# Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall['I'][0] == 4)
solver.add(pos['I'][0] == 1)

# Now evaluate each option

# Option A: Franz's watercolor is displayed on the same wall as Greene's oil.
opt_a = (wall['F'][1] == wall['G'][0])

# Option B: Franz's watercolor is displayed on the same wall as Hidalgo's oil.
opt_b = (wall['F'][1] == wall['H'][0])

# Option C: Greene's oil is displayed in an upper position.
opt_c = (pos['G'][0] == 0)

# Option D: Hidalgo's watercolor is displayed in a lower position.
opt_d = (pos['H'][1] == 1)

# Option E: Isaacs's watercolor is displayed on the same wall as Hidalgo's oil.
opt_e = (wall['I'][1] == wall['H'][0])

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