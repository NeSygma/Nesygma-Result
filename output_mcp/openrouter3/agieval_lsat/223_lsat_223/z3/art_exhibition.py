from z3 import *

# Students and painting types
students = ['F', 'G', 'H', 'I']  # Franz, Greene, Hidalgo, Isaacs
painting_types = ['oil', 'watercolor']
walls = [1, 2, 3, 4]
positions = ['U', 'L']

# For each student and painting type, we need to know which wall and position
# We'll use arrays: wall[student][type] and position[student][type]
wall = {}
position = {}
for s in students:
    for pt in painting_types:
        wall[(s, pt)] = Int(f'wall_{s}_{pt}')
        position[(s, pt)] = Int(f'pos_{s}_{pt}')

solver = Solver()

# Domain constraints: walls are 1-4, positions are 0 for U, 1 for L (or use 0/1)
for s in students:
    for pt in painting_types:
        solver.add(wall[(s, pt)] >= 1, wall[(s, pt)] <= 4)
        solver.add(position[(s, pt)] >= 0, position[(s, pt)] <= 1)  # 0 = U, 1 = L

# Each student has exactly one oil and one watercolor (already by definition)

# Constraint 1: No wall has only watercolors
# For each wall, at least one oil painting
for w in walls:
    oil_on_wall = []
    for s in students:
        oil_on_wall.append(wall[(s, 'oil')] == w)
    solver.add(Or(oil_on_wall))

# Constraint 2: No wall has work of only one student
# For each wall, at least two different students
for w in walls:
    # Count distinct students on wall w
    students_on_wall = []
    for s in students:
        # Student s has a painting on wall w if either oil or watercolor is on w
        students_on_wall.append(Or(wall[(s, 'oil')] == w, wall[(s, 'watercolor')] == w))
    # At least two students must be true
    solver.add(Sum([If(students_on_wall[i], 1, 0) for i in range(len(students_on_wall))]) >= 2)

# Constraint 3: No wall has both Franz and Isaacs together
for w in walls:
    franz_on_wall = Or(wall[('F', 'oil')] == w, wall[('F', 'watercolor')] == w)
    isaacs_on_wall = Or(wall[('I', 'oil')] == w, wall[('I', 'watercolor')] == w)
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Constraint 4: Greene's watercolor is in the upper position of the wall on which Franz's oil is displayed
# That means: wall[('G', 'watercolor')] == wall[('F', 'oil')] AND position[('G', 'watercolor')] == 0 (U)
solver.add(wall[('G', 'watercolor')] == wall[('F', 'oil')])
solver.add(position[('G', 'watercolor')] == 0)

# Constraint 5: Isaacs's oil is in the lower position of wall 4
solver.add(wall[('I', 'oil')] == 4)
solver.add(position[('I', 'oil')] == 1)  # lower position

# Additional constraint from Q: Franz's oil is on wall 1
solver.add(wall[('F', 'oil')] == 1)

# Now test each option
found_options = []

# Option A: Franz's watercolor is displayed on wall 4
opt_a = wall[('F', 'watercolor')] == 4

# Option B: Greene's oil is displayed on wall 2
opt_b = wall[('G', 'oil')] == 2

# Option C: Greene's watercolor is displayed on wall 2
opt_c = wall[('G', 'watercolor')] == 2

# Option D: Hidalgo's watercolor is displayed on wall 3
opt_d = wall[('H', 'watercolor')] == 3

# Option E: Isaacs's oil is displayed on wall 1
opt_e = wall[('I', 'oil')] == 1

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