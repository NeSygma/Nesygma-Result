from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare students, painting types, walls, and positions
students = ['Franz', 'Greene', 'Hidalgo', 'Isaacs']
painting_types = ['Oil', 'Watercolor']
walls = [1, 2, 3, 4]
positions = ['Upper', 'Lower']

# Create a solver
solver = Solver()

# Decision variables:
# For each student, their oil and watercolor paintings are represented as:
# (student, painting_type, wall, position)
# We will use a dictionary to map each painting to its attributes.
painting_assign = {}
for s in students:
    painting_assign[s] = {}
    for pt in painting_types:
        painting_assign[s][pt] = (Int(f'{s}_{pt}_wall'), Int(f'{s}_{pt}_pos'))
        # pos: 0 for Upper, 1 for Lower

# Helper function to get wall and position for a painting
def get_wall_pos(student, pt):
    return painting_assign[student][pt]

# Constraints:

# 1. Each student has exactly one oil and one watercolor
for s in students:
    solver.add(get_wall_pos(s, 'Oil')[0] >= 1, get_wall_pos(s, 'Oil')[0] <= 4)
    solver.add(get_wall_pos(s, 'Watercolor')[0] >= 1, get_wall_pos(s, 'Watercolor')[0] <= 4)
    solver.add(get_wall_pos(s, 'Oil')[1] >= 0, get_wall_pos(s, 'Oil')[1] <= 1)
    solver.add(get_wall_pos(s, 'Watercolor')[1] >= 0, get_wall_pos(s, 'Watercolor')[1] <= 1)

# 2. Each wall has exactly one upper and one lower painting
# We will enforce this by ensuring that for each wall, there are exactly two paintings,
# one in upper and one in lower position.
for wall in walls:
    solver.add(Sum([If(And(get_wall_pos(s, pt)[0] == wall, get_wall_pos(s, pt)[1] == 0), 1, 0) for s in students for pt in painting_types]) == 1)
    solver.add(Sum([If(And(get_wall_pos(s, pt)[0] == wall, get_wall_pos(s, pt)[1] == 1), 1, 0) for s in students for pt in painting_types]) == 1)

# 3. No wall has only watercolors
for wall in walls:
    # At least one oil on this wall
    solver.add(Or([get_wall_pos(s, 'Oil')[0] == wall for s in students]))

# 4. No wall has the work of only one student
for wall in walls:
    # At least two students have paintings on this wall
    solver.add(Sum([If(get_wall_pos(s, pt)[0] == wall, 1, 0) for s in students for pt in painting_types]) >= 2)

# 5. No wall has both Franz and Isaacs
for wall in walls:
    solver.add(Not(And(Or([get_wall_pos('Franz', pt)[0] == wall for pt in painting_types]),
                       Or([get_wall_pos('Isaacs', pt)[0] == wall for pt in painting_types]))))

# 6. Greene's watercolor is in the upper position of the wall where Franz's oil is
franz_oil_wall, franz_oil_pos = get_wall_pos('Franz', 'Oil')
greene_water_wall, greene_water_pos = get_wall_pos('Greene', 'Watercolor')
solver.add(greene_water_wall == franz_oil_wall)
solver.add(greene_water_pos == 0)  # Upper position

# 7. Isaacs's oil is in the lower position of wall 4
isaacs_oil_wall, isaacs_oil_pos = get_wall_pos('Isaacs', 'Oil')
solver.add(isaacs_oil_wall == 4)
solver.add(isaacs_oil_pos == 1)  # Lower position

# 8. Greene's oil is on the same wall as Franz's watercolor
greene_oil_wall, _ = get_wall_pos('Greene', 'Oil')
franz_water_wall, _ = get_wall_pos('Franz', 'Watercolor')
solver.add(greene_oil_wall == franz_water_wall)

# 9. No two paintings share the same wall and position
for s1 in students:
    for pt1 in painting_types:
        for s2 in students:
            for pt2 in painting_types:
                if s1 != s2 or pt1 != pt2:
                    w1, p1 = get_wall_pos(s1, pt1)
                    w2, p2 = get_wall_pos(s2, pt2)
                    solver.add(Not(And(w1 == w2, p1 == p2)))

# Additional constraint: Ensure that the wall with Franz's oil and Greene's watercolor
# does not also have Isaacs's oil (since Isaacs's oil is on wall 4 and no wall has both Franz and Isaacs)
# This is already enforced by constraint 5, but we can add a more explicit constraint.
for wall in walls:
    solver.add(Not(And(Or([get_wall_pos('Franz', 'Oil')[0] == wall for pt in painting_types]),
                       get_wall_pos('Isaacs', 'Oil')[0] == wall)))

# Now, check each answer choice
found_options = []

# (A) Greene's oil is displayed in an upper position.
solver.push()
greene_oil_wall_a, greene_oil_pos_a = get_wall_pos('Greene', 'Oil')
solver.add(greene_oil_pos_a == 0)  # Upper position
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.
solver.push()
hidalgo_water_wall, _ = get_wall_pos('Hidalgo', 'Watercolor')
isaacs_water_wall, _ = get_wall_pos('Isaacs', 'Watercolor')
solver.add(hidalgo_water_wall == isaacs_water_wall)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Hidalgo's oil is displayed in an upper position.
solver.push()
hidalgo_oil_wall, hidalgo_oil_pos = get_wall_pos('Hidalgo', 'Oil')
solver.add(hidalgo_oil_pos == 0)  # Upper position
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.
solver.push()
hidalgo_oil_wall, _ = get_wall_pos('Hidalgo', 'Oil')
isaacs_water_wall, _ = get_wall_pos('Isaacs', 'Watercolor')
solver.add(hidalgo_oil_wall == isaacs_water_wall)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Isaacs's watercolor is displayed in a lower position.
solver.push()
_, isaacs_water_pos = get_wall_pos('Isaacs', 'Watercolor')
solver.add(isaacs_water_pos == 1)  # Lower position
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")