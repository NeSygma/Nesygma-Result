from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Painting types: oil=0, watercolor=1
# Walls: 1,2,3,4
# Positions: upper=0, lower=1

# Each student has exactly one oil and one watercolor painting
# We need to assign each painting to a (wall, position) pair
# There are 8 paintings total, 4 walls * 2 positions = 8 slots

# Variables: for each student and type, which wall and position
wall = [[Int(f'wall_{s}_{t}') for t in range(2)] for s in range(4)]
pos = [[Int(f'pos_{s}_{t}') for t in range(2)] for s in range(4)]

# Domain constraints: walls 1-4, positions 0 (upper) or 1 (lower)
for s in range(4):
    for t in range(2):
        solver.add(And(wall[s][t] >= 1, wall[s][t] <= 4))
        solver.add(And(pos[s][t] >= 0, pos[s][t] <= 1))

# Each (wall, position) slot has exactly one painting
# All 8 paintings must be in distinct slots
slots = []
for s in range(4):
    for t in range(2):
        slots.append((wall[s][t], pos[s][t]))

# All slots must be distinct (each slot used at most once)
for i in range(8):
    for j in range(i+1, 8):
        solver.add(Or(slots[i][0] != slots[j][0], slots[i][1] != slots[j][1]))

# Condition 1: No wall has only watercolors displayed on it.
# For each wall, at least one painting on that wall must be oil (type=0)
for w in range(1, 5):
    # At least one oil painting on wall w
    solver.add(Or([And(wall[s][0] == w) for s in range(4)]))

# Condition 2: No wall has the work of only one student displayed on it.
# For each wall, the two paintings on it must be by different students
for w in range(1, 5):
    # Find all paintings on wall w
    for s1 in range(4):
        for s2 in range(s1+1, 4):
            for t1 in range(2):
                for t2 in range(2):
                    # If both paintings are on wall w, they must be by different students
                    # But we need to ensure the two paintings on wall w are by different students
                    pass

# Better approach: For each wall, the two slots (upper, lower) must have different students
for w in range(1, 5):
    # Get the student for upper position on wall w
    # upper_student = the student s where wall[s][t] == w and pos[s][t] == 0
    # lower_student = the student s where wall[s][t] == w and pos[s][t] == 1
    # They must be different
    upper_student = Int(f'upper_student_wall_{w}')
    lower_student = Int(f'lower_student_wall_{w}')
    
    # Define upper_student: the student whose painting is at (w, 0)
    solver.add(Or([And(wall[s][0] == w, pos[s][0] == 0, upper_student == s) for s in range(4)] +
                  [And(wall[s][1] == w, pos[s][1] == 0, upper_student == s) for s in range(4)]))
    
    # Define lower_student: the student whose painting is at (w, 1)
    solver.add(Or([And(wall[s][0] == w, pos[s][0] == 1, lower_student == s) for s in range(4)] +
                  [And(wall[s][1] == w, pos[s][1] == 1, lower_student == s) for s in range(4)]))
    
    solver.add(upper_student != lower_student)

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs.
for w in range(1, 5):
    # Franz (0) and Isaacs (3) cannot both be on wall w
    franz_on_w = Or([wall[0][t] == w for t in range(2)])
    isaacs_on_w = Or([wall[3][t] == w for t in range(2)])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# Franz's oil is student 0, type 0
# Greene's watercolor is student 1, type 1
# They must be on the same wall, and Greene's watercolor must be in upper position (pos=0)
solver.add(wall[1][1] == wall[0][0])  # Same wall
solver.add(pos[1][1] == 0)  # Greene's watercolor in upper position

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
# Isaacs's oil is student 3, type 0
solver.add(wall[3][0] == 4)  # Wall 4
solver.add(pos[3][0] == 1)  # Lower position

# Additional given conditions:
# Isaacs's watercolor is displayed on wall 2
solver.add(wall[3][1] == 2)

# Franz's oil is displayed on wall 3
solver.add(wall[0][0] == 3)

# Now we need to find what MUST be on wall 1
# Let's define what's on wall 1
# Wall 1 has two slots: upper (pos=0) and lower (pos=1)
# We need to find which painting MUST be on wall 1

# Define options
# (A) Franz's watercolor: student 0, type 1
opt_a = Or([And(wall[0][1] == 1, pos[0][1] == p) for p in range(2)])

# (B) Greene's oil: student 1, type 0
opt_b = Or([And(wall[1][0] == 1, pos[1][0] == p) for p in range(2)])

# (C) Greene's watercolor: student 1, type 1
opt_c = Or([And(wall[1][1] == 1, pos[1][1] == p) for p in range(2)])

# (D) Hidalgo's oil: student 2, type 0
opt_d = Or([And(wall[2][0] == 1, pos[2][0] == p) for p in range(2)])

# (E) Hidalgo's watercolor: student 2, type 1
opt_e = Or([And(wall[2][1] == 1, pos[2][1] == p) for p in range(2)])

# Test each option
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