from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# Positions: 0 = upper, 1 = lower
positions = [0, 1]

# For each student, we have an oil and a watercolor.
# We need to assign each painting to a (wall, position).
# Let's use integer variables for wall and position for each painting.

# Variables: oil_wall[s], oil_pos[s], water_wall[s], water_pos[s]
oil_wall = {s: Int(f'oil_wall_{s}') for s in students}
oil_pos = {s: Int(f'oil_pos_{s}') for s in students}
water_wall = {s: Int(f'water_wall_{s}') for s in students}
water_pos = {s: Int(f'water_pos_{s}') for s in students}

# Domain constraints: walls 1-4, positions 0-1
for s in students:
    solver.add(oil_wall[s] >= 1, oil_wall[s] <= 4)
    solver.add(water_wall[s] >= 1, water_wall[s] <= 4)
    solver.add(oil_pos[s] >= 0, oil_pos[s] <= 1)
    solver.add(water_pos[s] >= 0, water_pos[s] <= 1)

# Exactly two paintings per wall (one upper, one lower)
# Each wall has exactly 2 paintings: one at position 0, one at position 1.
# We can encode: for each wall w, the number of paintings assigned to (w, 0) is 1,
# and the number assigned to (w, 1) is 1.

for w in walls:
    # Upper position: exactly one painting
    solver.add(Sum([If(oil_wall[s] == w and oil_pos[s] == 0, 1, 0) for s in students] +
                   [If(water_wall[s] == w and water_pos[s] == 0, 1, 0) for s in students]) == 1)
    # Lower position: exactly one painting
    solver.add(Sum([If(oil_wall[s] == w and oil_pos[s] == 1, 1, 0) for s in students] +
                   [If(water_wall[s] == w and water_pos[s] == 1, 1, 0) for s in students]) == 1)

# Condition 1: No wall has only watercolors displayed on it.
# i.e., each wall must have at least one oil painting.
for w in walls:
    solver.add(Or([oil_wall[s] == w for s in students]))

# Condition 2: No wall has the work of only one student displayed on it.
# i.e., each wall must have paintings from at least two different students.
for w in walls:
    # At least two distinct students have a painting on wall w
    solver.add(Sum([If(oil_wall[s] == w, 1, 0) for s in students] +
                   [If(water_wall[s] == w, 1, 0) for s in students]) >= 2)

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in walls:
    # Not (Franz has a painting on w AND Isaacs has a painting on w)
    solver.add(Not(And(
        Or(oil_wall['F'] == w, water_wall['F'] == w),
        Or(oil_wall['I'] == w, water_wall['I'] == w)
    )))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(water_wall['G'] == oil_wall['F'])
solver.add(water_pos['G'] == 0)

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(oil_wall['I'] == 4)
solver.add(oil_pos['I'] == 1)

# Additional condition from the question: Franz's oil is displayed on wall 1.
solver.add(oil_wall['F'] == 1)

# Now evaluate each option
# Option A: Franz's watercolor is displayed on wall 4.
opt_a = And(water_wall['F'] == 4)

# Option B: Greene's oil is displayed on wall 2.
opt_b = And(oil_wall['G'] == 2)

# Option C: Greene's watercolor is displayed on wall 2.
opt_c = And(water_wall['G'] == 2)

# Option D: Hidalgo's watercolor is displayed on wall 3.
opt_d = And(water_wall['H'] == 3)

# Option E: Isaacs's oil is displayed on wall 1.
opt_e = And(oil_wall['I'] == 1)

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