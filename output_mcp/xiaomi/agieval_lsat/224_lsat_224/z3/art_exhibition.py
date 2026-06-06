from z3 import *

solver = Solver()

# Students: Franz(0), Greene(1), Hidalgo(2), Isaacs(3)
# Painting types: oil(0), watercolor(1)
# Walls: 1, 2, 3, 4
# Positions: upper(0), lower(1)

# Each student has exactly 2 paintings (one oil, one watercolor)
# Each wall has exactly 2 paintings (one upper, one lower)
# Total: 8 paintings, 4 walls × 2 positions = 8 slots

# Variables: for each painting, which wall and which position
# student_wall_type[student][type] = wall number (1-4)
# student_pos_type[student][type] = position (0=upper, 1=lower)

students = ['Franz', 'Greene', 'Hidalgo', 'Isaacs']
types = ['oil', 'watercolor']

# Wall assignment for each student's oil and watercolor
wall = {}
pos = {}
for s in range(4):
    for t in range(2):
        wall[s,t] = Int(f'wall_{students[s]}_{types[t]}')
        pos[s,t] = Int(f'pos_{students[s]}_{types[t]}')
        solver.add(wall[s,t] >= 1, wall[s,t] <= 4)
        solver.add(pos[s,t] >= 0, pos[s,t] <= 1)

# Each student's oil and watercolor are on different walls
for s in range(4):
    solver.add(wall[s,0] != wall[s,1])

# Each wall has exactly 2 paintings (one upper, one lower)
# Total paintings per wall = 2
for w in range(1, 5):
    solver.add(Sum([If(wall[s,t] == w, 1, 0) for s in range(4) for t in range(2)]) == 2)

# Each wall has exactly one upper and one lower
for w in range(1, 5):
    solver.add(Sum([If(And(wall[s,t] == w, pos[s,t] == 0), 1, 0) for s in range(4) for t in range(2)]) == 1)
    solver.add(Sum([If(And(wall[s,t] == w, pos[s,t] == 1), 1, 0) for s in range(4) for t in range(2)]) == 1)

# Condition 1: No wall has only watercolors displayed on it.
# This means each wall must have at least one oil painting.
for w in range(1, 5):
    solver.add(Sum([If(And(wall[s,0] == w), 1, 0) for s in range(4)]) >= 1)

# Condition 2: No wall has the work of only one student displayed on it.
# Each wall must have paintings from at least 2 different students.
for w in range(1, 5):
    for s in range(4):
        # Not both paintings of student s on wall w
        solver.add(Not(And(wall[s,0] == w, wall[s,1] == w)))

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs.
for w in range(1, 5):
    for t1 in range(2):
        for t2 in range(2):
            solver.add(Not(And(wall[0,t1] == w, wall[3,t2] == w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(wall[1,1] == wall[0,0])  # Same wall
solver.add(pos[1,1] == 0)  # Upper position

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[3,0] == 4)
solver.add(pos[3,0] == 1)

# Now evaluate each option
# (A) Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.
opt_a = And(pos[0,0] == 1, pos[0,1] == 1, pos[1,0] == 1, pos[1,1] == 1)

# (B) Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.
opt_b = And(pos[0,0] == 0, pos[0,1] == 0, pos[1,0] == 0, pos[1,1] == 0)

# (C) Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.
opt_c = And(pos[0,0] == 0, pos[0,1] == 0, pos[2,0] == 0, pos[2,1] == 0)

# (D) Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.
opt_d = And(pos[1,0] == 1, pos[1,1] == 1, pos[2,0] == 1, pos[2,1] == 1)

# (E) Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions.
opt_e = And(pos[1,0] == 0, pos[1,1] == 0, pos[2,0] == 0, pos[2,1] == 0)

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