from z3 import *

# Create solver
solver = Solver()

# Define students and walls
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
walls = [1, 2, 3, 4]
positions = ["U", "L"]  # Upper, Lower

# Create variables: For each student, for each painting type (oil/watercolor), which wall and position
# We'll use arrays: student_painting[student][painting_type] = (wall, position)
# But since we need to track both wall and position, let's create separate variables

# For each student, oil and watercolor have wall and position
oil_wall = {s: Int(f"oil_wall_{s}") for s in students}
oil_pos = {s: Int(f"oil_pos_{s}") for s in students}  # 0 for U, 1 for L
watercolor_wall = {s: Int(f"watercolor_wall_{s}") for s in students}
watercolor_pos = {s: Int(f"watercolor_pos_{s}") for s in students}  # 0 for U, 1 for L

# Domain constraints: walls are 1-4, positions are 0 or 1
for s in students:
    solver.add(oil_wall[s] >= 1, oil_wall[s] <= 4)
    solver.add(watercolor_wall[s] >= 1, watercolor_wall[s] <= 4)
    solver.add(oil_pos[s] >= 0, oil_pos[s] <= 1)
    solver.add(watercolor_pos[s] >= 0, watercolor_pos[s] <= 1)

# Each wall has exactly 2 paintings (one upper, one lower)
# For each wall and position, exactly one painting
for w in walls:
    for p in positions:
        # Count how many paintings are on wall w in position p
        # We'll use a sum of indicators
        pos_val = 0 if p == "U" else 1
        count = Sum([If(oil_wall[s] == w, If(oil_pos[s] == pos_val, 1, 0), 0) +
                     If(watercolor_wall[s] == w, If(watercolor_pos[s] == pos_val, 1, 0), 0)
                     for s in students])
        solver.add(count == 1)

# Constraint 1: No wall has only watercolors
# For each wall, at least one oil painting
for w in walls:
    oil_count = Sum([If(oil_wall[s] == w, 1, 0) for s in students])
    solver.add(oil_count >= 1)

# Constraint 2: No wall has work of only one student
# For each wall, at least 2 different students
for w in walls:
    # Count distinct students on wall w
    # We need to check if there are at least 2 different students
    # We'll use a more direct approach: for each pair of students, they can't be the only ones
    # Actually, simpler: for each wall, there must be at least 2 students with paintings there
    students_on_wall = []
    for s in students:
        has_oil = oil_wall[s] == w
        has_water = watercolor_wall[s] == w
        students_on_wall.append(Or(has_oil, has_water))
    # At least 2 students must be True
    solver.add(Sum([If(students_on_wall[i], 1, 0) for i in range(len(students))]) >= 2)

# Constraint 3: No wall has both Franz and Isaacs
for w in walls:
    franz_on_wall = Or(oil_wall["Franz"] == w, watercolor_wall["Franz"] == w)
    isaacs_on_wall = Or(oil_wall["Isaacs"] == w, watercolor_wall["Isaacs"] == w)
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is
# So: watercolor_wall["Greene"] == oil_wall["Franz"] AND watercolor_pos["Greene"] == 0 (upper)
solver.add(watercolor_wall["Greene"] == oil_wall["Franz"])
solver.add(watercolor_pos["Greene"] == 0)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(oil_wall["Isaacs"] == 4)
solver.add(oil_pos["Isaacs"] == 1)  # lower

# Additional given: Isaacs's watercolor is on wall 2
solver.add(watercolor_wall["Isaacs"] == 2)

# Additional given: Franz's oil is on wall 3
solver.add(oil_wall["Franz"] == 3)

# Now, we need to find what must be on wall 1
# We'll test each option by adding it as a constraint and checking if it's always true

# First, let's find all possible models that satisfy the base constraints
# We'll use the multiple choice evaluation pattern

# Define options for what must be on wall 1
# Option A: Franz's watercolor on wall 1
opt_a = watercolor_wall["Franz"] == 1

# Option B: Greene's oil on wall 1
opt_b = oil_wall["Greene"] == 1

# Option C: Greene's watercolor on wall 1
opt_c = watercolor_wall["Greene"] == 1

# Option D: Hidalgo's oil on wall 1
opt_d = oil_wall["Hidalgo"] == 1

# Option E: Hidalgo's watercolor on wall 1
opt_e = watercolor_wall["Hidalgo"] == 1

# Now test each option
found_options = []

# Test A
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Test B
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Test C
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Test D
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Test E
solver.push()
solver.add(opt_e)
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