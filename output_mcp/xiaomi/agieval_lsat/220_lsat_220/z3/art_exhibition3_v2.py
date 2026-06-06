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
for w in range(1, 5):
    for s in range(4):
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

# From condition 4: Greene's watercolor is on wall 3 (same as Franz's oil), upper position
# So wall 3 has: Franz's oil and Greene's watercolor (upper)
# This means Franz's watercolor cannot be on wall 3 (condition 2: no wall has only one student)
# Also, Isaacs cannot be on wall 3 (condition 3)

# Now let's check what MUST be on wall 1
# First, let's see what's already placed:
# Wall 3: Franz's oil, Greene's watercolor (upper)
# Wall 4: Isaacs's oil (lower)
# Wall 2: Isaacs's watercolor

# Remaining paintings to place:
# Franz's watercolor, Greene's oil, Hidalgo's oil, Hidalgo's watercolor

# Wall 1 needs exactly 2 paintings (one upper, one lower)
# Wall 4 needs one more painting (upper position)
# Wall 2 needs one more painting (upper or lower, but not where Isaacs's watercolor is)

# Let's add constraints for remaining placements
# Franz's watercolor: wall[0][1], pos[0][1]
# Greene's oil: wall[1][0], pos[1][0]
# Hidalgo's oil: wall[2][0], pos[2][0]
# Hidalgo's watercolor: wall[2][1], pos[2][1]

# Wall 3 already has 2 paintings (Franz's oil and Greene's watercolor)
# So no more paintings can be on wall 3
for s in range(4):
    for t in range(2):
        if not (s == 0 and t == 0) and not (s == 1 and t == 1):
            solver.add(wall[s][t] != 3)

# Wall 4 has Isaacs's oil (lower). Need one more painting (upper).
# Wall 2 has Isaacs's watercolor. Need one more painting.
# Wall 1 needs two paintings.

# Now test each option
# (A) Franz's watercolor on wall 1
opt_a = wall[0][1] == 1

# (B) Greene's oil on wall 1
opt_b = wall[1][0] == 1

# (C) Greene's watercolor on wall 1 - already on wall 3, so impossible
opt_c = wall[1][1] == 1

# (D) Hidalgo's oil on wall 1
opt_d = wall[2][0] == 1

# (E) Hidalgo's watercolor on wall 1
opt_e = wall[2][1] == 1

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