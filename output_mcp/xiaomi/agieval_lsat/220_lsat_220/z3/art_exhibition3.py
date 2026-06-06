from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Painting types: oil=0, watercolor=1
# Walls: 1,2,3,4
# Positions: upper=0, lower=1

# Variables: for each student and type, which wall and position
wall = [[Int(f'wall_{s}_{t}') for t in range(2)] for s in range(4)]
pos = [[Int(f'pos_{s}_{t}') for t in range(2)] for s in range(4)]

# Domain constraints: walls 1-4, positions 0 (upper) or 1 (lower)
for s in range(4):
    for t in range(2):
        solver.add(And(wall[s][t] >= 1, wall[s][t] <= 4))
        solver.add(And(pos[s][t] >= 0, pos[s][t] <= 1))

# All 8 paintings must be in distinct (wall, position) slots
for i_s in range(4):
    for i_t in range(2):
        for j_s in range(4):
            for j_t in range(2):
                if (i_s, i_t) < (j_s, j_t):
                    solver.add(Or(wall[i_s][i_t] != wall[j_s][j_t], 
                                  pos[i_s][i_t] != pos[j_s][j_t]))

# Condition 1: No wall has only watercolors displayed on it.
# For each wall, at least one painting on that wall must be oil (type=0)
for w in range(1, 5):
    solver.add(Or([wall[s][0] == w for s in range(4)]))

# Condition 2: No wall has the work of only one student displayed on it.
# For each wall, the two paintings on it must be by different students
# This means: for each student, at most one of their paintings can be on wall w
for w in range(1, 5):
    for s in range(4):
        # Student s can have at most one painting on wall w
        solver.add(Not(And(wall[s][0] == w, wall[s][1] == w)))

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs.
for w in range(1, 5):
    franz_on_w = Or([wall[0][t] == w for t in range(2)])
    isaacs_on_w = Or([wall[3][t] == w for t in range(2)])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(wall[1][1] == wall[0][0])  # Same wall
solver.add(pos[1][1] == 0)  # Greene's watercolor in upper position

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[3][0] == 4)  # Wall 4
solver.add(pos[3][0] == 1)  # Lower position

# Additional given conditions:
# Isaacs's watercolor is displayed on wall 2
solver.add(wall[3][1] == 2)

# Franz's oil is displayed on wall 3
solver.add(wall[0][0] == 3)

# Now we need to find what MUST be on wall 1
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