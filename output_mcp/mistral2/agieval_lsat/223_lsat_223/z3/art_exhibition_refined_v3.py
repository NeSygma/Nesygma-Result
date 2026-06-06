from z3 import *

solver = Solver()

# Students and media
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
media = ["oil", "watercolor"]

# Walls and positions
walls = [1, 2, 3, 4]
positions = ["upper", "lower"]

# We will model each painting as a unique entity with attributes
# Use a dictionary to track which painting is where: (wall, position) -> (student, medium)
wall_pos = {}
for w in walls:
    for p in positions:
        wall_pos[(w, p)] = (None, None)  # (student, medium)

# Franz's oil is displayed on wall 1, upper position (given in the question)
solver.add(wall_pos[(1, "upper")][0] == "Franz")
solver.add(wall_pos[(1, "upper")][1] == "oil")

# Isaacs's oil is displayed in the lower position of wall 4
solver.add(wall_pos[(4, "lower")][0] == "Isaacs")
solver.add(wall_pos[(4, "lower")][1] == "oil")

# Greene's watercolor is displayed in the lower position of the wall on which Franz's oil is displayed
# Franz's oil is on wall 1, upper position, so Greene's watercolor is on wall 1, lower position
solver.add(wall_pos[(1, "lower")][0] == "Greene")
solver.add(wall_pos[(1, "lower")][1] == "watercolor")

# No wall has only watercolors displayed on it
for w in walls:
    upper_student, upper_medium = wall_pos[(w, "upper")]
    lower_student, lower_medium = wall_pos[(w, "lower")]
    # At least one painting on the wall is oil
    solver.add(Or(
        upper_medium == "oil",
        lower_medium == "oil"
    ))

# No wall has the work of only one student displayed on it
for w in walls:
    upper_student, _ = wall_pos[(w, "upper")]
    lower_student, _ = wall_pos[(w, "lower")]
    # The two paintings on the wall must be by different students
    solver.add(upper_student != lower_student)

# No wall has both a painting by Franz and a painting by Isaacs displayed on it
for w in walls:
    upper_student, _ = wall_pos[(w, "upper")]
    lower_student, _ = wall_pos[(w, "lower")]
    solver.add(Not(And(upper_student == "Franz", lower_student == "Isaacs")))
    solver.add(Not(And(upper_student == "Isaacs", lower_student == "Franz")))

# Each student must have exactly one oil and one watercolor
# We will enforce this by ensuring that for each student, their oil and watercolor are assigned to some wall and position
for s in students:
    oil_positions = []
    watercolor_positions = []
    for w in walls:
        for p in positions:
            student, medium = wall_pos[(w, p)]
            if student == s:
                if medium == "oil":
                    oil_positions.append((w, p))
                elif medium == "watercolor":
                    watercolor_positions.append((w, p))
    solver.add(Sum([1 if oil_positions else 0]) == 1)
    solver.add(Sum([1 if watercolor_positions else 0]) == 1)

# Now, evaluate the multiple choice options
found_options = []

# Option A: Franz's watercolor is displayed on wall 4
solver.push()
solver.add(Or(
    And(wall_pos[(4, "upper")][0] == "Franz", wall_pos[(4, "upper")][1] == "watercolor"),
    And(wall_pos[(4, "lower")][0] == "Franz", wall_pos[(4, "lower")][1] == "watercolor")
))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Greene's oil is displayed on wall 2
solver.push()
solver.add(Or(
    And(wall_pos[(2, "upper")][0] == "Greene", wall_pos[(2, "upper")][1] == "oil"),
    And(wall_pos[(2, "lower")][0] == "Greene", wall_pos[(2, "lower")][1] == "oil")
))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's watercolor is displayed on wall 2
solver.push()
solver.add(Or(
    And(wall_pos[(2, "upper")][0] == "Greene", wall_pos[(2, "upper")][1] == "watercolor"),
    And(wall_pos[(2, "lower")][0] == "Greene", wall_pos[(2, "lower")][1] == "watercolor")
))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's watercolor is displayed on wall 3
solver.push()
solver.add(Or(
    And(wall_pos[(3, "upper")][0] == "Hidalgo", wall_pos[(3, "upper")][1] == "watercolor"),
    And(wall_pos[(3, "lower")][0] == "Hidalgo", wall_pos[(3, "lower")][1] == "watercolor")
))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Isaacs's oil is displayed on wall 1
solver.push()
solver.add(Or(
    And(wall_pos[(1, "upper")][0] == "Isaacs", wall_pos[(1, "upper")][1] == "oil"),
    And(wall_pos[(1, "lower")][0] == "Isaacs", wall_pos[(1, "lower")][1] == "oil")
))
if solver.check() == sat:
    found_options.append("E")
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