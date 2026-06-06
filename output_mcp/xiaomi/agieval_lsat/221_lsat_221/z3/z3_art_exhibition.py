from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Painting types: Oil=0, Watercolor=1
# Walls: 1,2,3,4
# Positions: Upper=0, Lower=1

# Each student has exactly one oil and one watercolor painting
# We need to assign each painting to a (wall, position)

# Variables: for each student and painting type, which wall and position
wall = [[Int(f'wall_{s}_{t}') for t in range(2)] for s in range(4)]
pos = [[Int(f'pos_{s}_{t}') for t in range(2)] for s in range(4)]

# Domain constraints: walls 1-4, positions 0 (upper) or 1 (lower)
for s in range(4):
    for t in range(2):
        solver.add(And(wall[s][t] >= 1, wall[s][t] <= 4))
        solver.add(Or(pos[s][t] == 0, pos[s][t] == 1))

# Each wall has exactly 2 paintings (one upper, one lower)
# Total paintings = 8, 4 walls × 2 = 8, so each wall gets exactly 2
# Each (wall, position) pair is used exactly once
for s1 in range(4):
    for t1 in range(2):
        for s2 in range(4):
            for t2 in range(2):
                if (s1, t1) < (s2, t2):
                    # Either different wall or different position
                    solver.add(Or(
                        wall[s1][t1] != wall[s2][t2],
                        pos[s1][t1] != pos[s2][t2]
                    ))

# Condition 1: No wall has only watercolors displayed on it.
# For each wall, at least one painting on it must be oil (type=0)
for w in range(1, 5):
    solver.add(Or([And(wall[s][0] == w, pos[s][0] == p) 
                   for s in range(4) for p in range(2)] +
                  [And(wall[s][0] == w) for s in range(4)]))
    # Simpler: at least one oil painting on each wall
    solver.add(Or([wall[s][0] == w for s in range(4)]))

# Condition 2: No wall has the work of only one student displayed on it.
# For each wall, the two paintings must be from different students
for w in range(1, 5):
    # Find all paintings on wall w
    paintings_on_wall = []
    for s in range(4):
        for t in range(2):
            paintings_on_wall.append((s, t))
    
    # For each pair of paintings that could be on wall w, they must be from different students
    # Actually: the two paintings on wall w must be from different students
    # We need: for each wall, the set of students whose paintings are on that wall has size >= 2
    # Since each wall has exactly 2 paintings, they must be from 2 different students
    for s1 in range(4):
        for t1 in range(2):
            for s2 in range(4):
                for t2 in range(2):
                    if (s1, t1) < (s2, t2):
                        solver.add(Implies(
                            And(wall[s1][t1] == w, wall[s2][t2] == w),
                            s1 != s2
                        ))

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs.
# Franz=0, Isaacs=3
for w in range(1, 5):
    for t1 in range(2):
        for t2 in range(2):
            solver.add(Not(And(wall[0][t1] == w, wall[3][t2] == w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# Greene's watercolor: student=1, type=1
# Franz's oil: student=0, type=0
solver.add(wall[1][1] == wall[0][0])  # Same wall
solver.add(pos[1][1] == 0)  # Greene's watercolor is upper

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
# Isaacs's oil: student=3, type=0
solver.add(wall[3][0] == 4)
solver.add(pos[3][0] == 1)

# Additional condition: Hidalgo's oil is displayed on wall 2
# Hidalgo's oil: student=2, type=0
solver.add(wall[2][0] == 2)

# Now check each option for what else could be on wall 2
# Wall 2 has exactly 2 paintings: one upper, one lower
# Hidalgo's oil is already on wall 2 (position unknown yet)

# Option A: Franz's oil (student=0, type=0) on wall 2
opt_a = (wall[0][0] == 2)

# Option B: Greene's watercolor (student=1, type=1) on wall 2
opt_b = (wall[1][1] == 2)

# Option C: Greene's oil (student=1, type=0) on wall 2
opt_c = (wall[1][0] == 2)

# Option D: Hidalgo's watercolor (student=2, type=1) on wall 2
opt_d = (wall[2][1] == 2)

# Option E: Isaacs's watercolor (student=3, type=1) on wall 2
opt_e = (wall[3][1] == 2)

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