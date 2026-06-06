from z3 import *

# Students and painting types
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
painting_types = ["oil", "watercolor"]

# Walls and positions
walls = [1, 2, 3, 4]
positions = ["upper", "lower"]

# Create variables: for each student and painting type, which wall and position
# We'll use arrays indexed by student and painting type
# student_index: 0=F, 1=G, 2=H, 3=I
# painting_index: 0=oil, 1=watercolor

# Wall assignment for each student's painting
wall = [[Int(f"wall_{s}_{p}") for p in range(2)] for s in range(4)]
# Position assignment for each student's painting
position = [[Int(f"pos_{s}_{p}") for p in range(2)] for s in range(4)]

solver = Solver()

# Domain constraints: walls are 1-4, positions are 0=upper, 1=lower
for s in range(4):
    for p in range(2):
        solver.add(wall[s][p] >= 1, wall[s][p] <= 4)
        solver.add(position[s][p] >= 0, position[s][p] <= 1)

# Each wall has exactly 2 paintings (one upper, one lower)
# For each wall and position, exactly one student has a painting there
for w in walls:
    for pos in positions:
        pos_idx = 0 if pos == "upper" else 1
        # Exactly one student has a painting in this wall/position
        solver.add(Or([And(wall[s][p] == w, position[s][p] == pos_idx) 
                      for s in range(4) for p in range(2)]))

# Each student has exactly 2 paintings (one oil, one watercolor)
for s in range(4):
    # Oil and watercolor must be on different walls or different positions
    # Actually, they can be on same wall but different positions
    # But we need to ensure they are distinct paintings
    # We'll ensure they are not identical (same wall and position)
    solver.add(Or(wall[s][0] != wall[s][1], position[s][0] != position[s][1]))

# Constraint 1: No wall has only watercolors
# For each wall, at least one oil painting
for w in walls:
    solver.add(Or([And(wall[s][0] == w) for s in range(4)]))  # At least one oil on each wall

# Constraint 2: No wall has work of only one student
# For each wall, at least 2 different students
for w in walls:
    # Count distinct students on this wall
    student_on_wall = []
    for s in range(4):
        student_on_wall.append(Or(wall[s][0] == w, wall[s][1] == w))
    # At least 2 students on this wall
    solver.add(Sum([If(cond, 1, 0) for cond in student_on_wall]) >= 2)

# Constraint 3: No wall has both Franz and Isaacs
# For each wall, not both F and I have paintings there
for w in walls:
    f_on_wall = Or(wall[0][0] == w, wall[0][1] == w)  # Franz
    i_on_wall = Or(wall[3][0] == w, wall[3][1] == w)  # Isaacs
    solver.add(Not(And(f_on_wall, i_on_wall)))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is
# Franz's oil is on some wall W, Greene's watercolor is on wall W in upper position
# We need to find the wall where Franz's oil is
franz_oil_wall = wall[0][0]  # Franz's oil is index 0
greene_watercolor_wall = wall[1][1]  # Greene's watercolor is index 1
greene_watercolor_pos = position[1][1]  # Greene's watercolor position

solver.add(greene_watercolor_wall == franz_oil_wall)
solver.add(greene_watercolor_pos == 0)  # upper position

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(wall[3][0] == 4)  # Isaacs's oil on wall 4
solver.add(position[3][0] == 1)  # lower position

# Additional condition: Hidalgo's oil is on wall 2
solver.add(wall[2][0] == 2)  # Hidalgo's oil on wall 2

# Now evaluate answer choices for what could also be on wall 2
# We need to check which of the following could be on wall 2:
# (A) Franz's oil, (B) Greene's watercolor, (C) Greene's oil, (D) Hidalgo's watercolor, (E) Isaacs's watercolor

# For each option, we check if there exists a satisfying assignment where that option is true
found_options = []

# Option A: Franz's oil on wall 2
solver.push()
solver.add(wall[0][0] == 2)  # Franz's oil on wall 2
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Greene's watercolor on wall 2
solver.push()
solver.add(wall[1][1] == 2)  # Greene's watercolor on wall 2
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's oil on wall 2
solver.push()
solver.add(wall[1][0] == 2)  # Greene's oil on wall 2
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's watercolor on wall 2
solver.push()
solver.add(wall[2][1] == 2)  # Hidalgo's watercolor on wall 2
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Isaacs's watercolor on wall 2
solver.push()
solver.add(wall[3][1] == 2)  # Isaacs's watercolor on wall 2
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")