from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare students and painting types
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
painting_types = ["oil", "watercolor"]

# Create a solver
solver = Solver()

# Declare variables for each student's oil and watercolor paintings
# Each variable is a tuple (wall, position) where wall is 1-4 and position is 0 (upper) or 1 (lower)
oil_wall = {s: Int(f"oil_wall_{s}") for s in students}
oil_pos = {s: Int(f"oil_pos_{s}") for s in students}
water_wall = {s: Int(f"water_wall_{s}") for s in students}
water_pos = {s: Int(f"water_pos_{s}") for s in students}

# Helper: Ensure wall is between 1 and 4
for s in students:
    solver.add(oil_wall[s] >= 1, oil_wall[s] <= 4)
    solver.add(water_wall[s] >= 1, water_wall[s] <= 4)
    solver.add(oil_pos[s] >= 0, oil_pos[s] <= 1)
    solver.add(water_pos[s] >= 0, water_pos[s] <= 1)

# Constraint 1: Each student has exactly one oil and one watercolor
# (Already enforced by variable declarations)

# Constraint 2: Each wall has exactly two paintings (one upper, one lower)
# We will enforce this by ensuring that for each wall, there is exactly one painting in upper and one in lower position
for w in range(1, 5):
    # Upper position (0) on wall w
    upper_paintings = []
    for s in students:
        # Oil in upper position
        upper_paintings.append(And(oil_wall[s] == w, oil_pos[s] == 0))
        # Watercolor in upper position
        upper_paintings.append(And(water_wall[s] == w, water_pos[s] == 0))
    # Exactly one painting in upper position on wall w
    solver.add(Sum([If(p, 1, 0) for p in upper_paintings]) == 1)
    
    # Lower position (1) on wall w
    lower_paintings = []
    for s in students:
        # Oil in lower position
        lower_paintings.append(And(oil_wall[s] == w, oil_pos[s] == 1))
        # Watercolor in lower position
        lower_paintings.append(And(water_wall[s] == w, water_pos[s] == 1))
    # Exactly one painting in lower position on wall w
    solver.add(Sum([If(p, 1, 0) for p in lower_paintings]) == 1)

# Constraint 3: No wall has only watercolors
# For each wall, at least one oil painting exists
for w in range(1, 5):
    has_oil = []
    for s in students:
        has_oil.append(Or(
            And(oil_wall[s] == w, oil_pos[s] == 0),
            And(oil_wall[s] == w, oil_pos[s] == 1)
        ))
    solver.add(Or(has_oil))

# Constraint 4: No wall has the work of only one student
# For each wall, at least two students have paintings
for w in range(1, 5):
    students_on_wall = []
    for s in students:
        students_on_wall.append(
            Or(
                And(oil_wall[s] == w, oil_pos[s] == 0),
                And(oil_wall[s] == w, oil_pos[s] == 1),
                And(water_wall[s] == w, water_pos[s] == 0),
                And(water_wall[s] == w, water_pos[s] == 1)
            )
        )
    # At least two students have paintings on wall w
    solver.add(Sum([If(s, 1, 0) for s in students_on_wall]) >= 2)

# Constraint 5: No wall has both Franz and Isaacs
for w in range(1, 5):
    franz_on_wall = Or(
        oil_wall["Franz"] == w,
        water_wall["Franz"] == w
    )
    isaacs_on_wall = Or(
        oil_wall["Isaacs"] == w,
        water_wall["Isaacs"] == w
    )
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Constraint 6: Greene's watercolor is in the upper position of the wall where Franz's oil is
franz_oil_wall = oil_wall["Franz"]
greene_water_wall = water_wall["Greene"]
greene_water_pos = water_pos["Greene"]
solver.add(greene_water_wall == franz_oil_wall)
solver.add(greene_water_pos == 0)

# Constraint 7: Isaacs's oil is in the lower position of wall 4
solver.add(oil_wall["Isaacs"] == 4)
solver.add(oil_pos["Isaacs"] == 1)

# Now, evaluate each option to see if it can be true
found_options = []

# Option A: Franz's watercolor is displayed on the same wall as Greene's oil
solver.push()
# Franz's watercolor wall == Greene's oil wall
solver.add(water_wall["Franz"] == oil_wall["Greene"])
result_A = solver.check()
solver.pop()

# Option B: Franz's watercolor is displayed on the same wall as Hidalgo's oil
solver.push()
# Franz's watercolor wall == Hidalgo's oil wall
solver.add(water_wall["Franz"] == oil_wall["Hidalgo"])
result_B = solver.check()
solver.pop()

# Option C: Greene's oil is displayed in an upper position
solver.push()
# Greene's oil position == 0 (upper)
solver.add(oil_pos["Greene"] == 0)
result_C = solver.check()
solver.pop()

# Option D: Hidalgo's watercolor is displayed in a lower position
solver.push()
# Hidalgo's watercolor position == 1 (lower)
solver.add(water_pos["Hidalgo"] == 1)
result_D = solver.check()
solver.pop()

# Option E: Isaacs's watercolor is displayed on the same wall as Hidalgo's oil
solver.push()
# Isaacs's watercolor wall == Hidalgo's oil wall
solver.add(water_wall["Isaacs"] == oil_wall["Hidalgo"])
result_E = solver.check()
solver.pop()

# Collect options that are satisfiable
if result_A == sat:
    found_options.append("A")
if result_B == sat:
    found_options.append("B")
if result_C == sat:
    found_options.append("C")
if result_D == sat:
    found_options.append("D")
if result_E == sat:
    found_options.append("E")

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")