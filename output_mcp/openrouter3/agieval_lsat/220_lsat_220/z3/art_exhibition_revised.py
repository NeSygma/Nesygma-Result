from z3 import *

# Create solver
solver = Solver()

# Define students and walls
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
walls = [1, 2, 3, 4]
positions = ["U", "L"]  # Upper, Lower

# Create variables: For each student, for each painting type (oil/watercolor), which wall and position
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
        pos_val = 0 if p == "U" else 1
        count = Sum([If(oil_wall[s] == w, If(oil_pos[s] == pos_val, 1, 0), 0) +
                     If(watercolor_wall[s] == w, If(watercolor_pos[s] == pos_val, 1, 0), 0)
                     for s in students])
        solver.add(count == 1)

# Constraint 1: No wall has only watercolors
for w in walls:
    oil_count = Sum([If(oil_wall[s] == w, 1, 0) for s in students])
    solver.add(oil_count >= 1)

# Constraint 2: No wall has work of only one student
for w in walls:
    students_on_wall = []
    for s in students:
        has_oil = oil_wall[s] == w
        has_water = watercolor_wall[s] == w
        students_on_wall.append(Or(has_oil, has_water))
    solver.add(Sum([If(students_on_wall[i], 1, 0) for i in range(len(students))]) >= 2)

# Constraint 3: No wall has both Franz and Isaacs
for w in walls:
    franz_on_wall = Or(oil_wall["Franz"] == w, watercolor_wall["Franz"] == w)
    isaacs_on_wall = Or(oil_wall["Isaacs"] == w, watercolor_wall["Isaacs"] == w)
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is
solver.add(watercolor_wall["Greene"] == oil_wall["Franz"])
solver.add(watercolor_pos["Greene"] == 0)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(oil_wall["Isaacs"] == 4)
solver.add(oil_pos["Isaacs"] == 1)

# Additional given: Isaacs's watercolor is on wall 2
solver.add(watercolor_wall["Isaacs"] == 2)

# Additional given: Franz's oil is on wall 3
solver.add(oil_wall["Franz"] == 3)

# Now, we need to find what MUST be on wall 1
# For each option, we check if its negation leads to unsatisfiability

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

# Test each option by checking if its negation is unsatisfiable
must_be_true = []

# Test A: If NOT(opt_a) is unsatisfiable, then opt_a must be true
solver.push()
solver.add(Not(opt_a))
result_a = solver.check()
solver.pop()
if result_a == unsat:
    must_be_true.append("A")

# Test B
solver.push()
solver.add(Not(opt_b))
result_b = solver.check()
solver.pop()
if result_b == unsat:
    must_be_true.append("B")

# Test C
solver.push()
solver.add(Not(opt_c))
result_c = solver.check()
solver.pop()
if result_c == unsat:
    must_be_true.append("C")

# Test D
solver.push()
solver.add(Not(opt_d))
result_d = solver.check()
solver.pop()
if result_d == unsat:
    must_be_true.append("D")

# Test E
solver.push()
solver.add(Not(opt_e))
result_e = solver.check()
solver.pop()
if result_e == unsat:
    must_be_true.append("E")

# Print results
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")