from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# For each student, we have an oil and a watercolor.
# Each painting is assigned to a (wall, position).
# Let's use integer variables.

oil_wall = {s: Int(f'oil_wall_{s}') for s in students}
oil_pos = {s: Int(f'oil_pos_{s}') for s in students}
water_wall = {s: Int(f'water_wall_{s}') for s in students}
water_pos = {s: Int(f'water_pos_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(oil_wall[s] >= 1, oil_wall[s] <= 4)
    solver.add(water_wall[s] >= 1, water_wall[s] <= 4)
    solver.add(oil_pos[s] >= 0, oil_pos[s] <= 1)
    solver.add(water_pos[s] >= 0, water_pos[s] <= 1)

# Exactly two paintings per wall: one upper (pos 0), one lower (pos 1)
for w in walls:
    # Upper position count = 1
    solver.add(Sum([If(And(oil_wall[s] == w, oil_pos[s] == 0), 1, 0) for s in students] +
                   [If(And(water_wall[s] == w, water_pos[s] == 0), 1, 0) for s in students]) == 1)
    # Lower position count = 1
    solver.add(Sum([If(And(oil_wall[s] == w, oil_pos[s] == 1), 1, 0) for s in students] +
                   [If(And(water_wall[s] == w, water_pos[s] == 1), 1, 0) for s in students]) == 1)

# Condition 1: No wall has only watercolors. Each wall must have at least one oil.
for w in walls:
    solver.add(Or([oil_wall[s] == w for s in students]))

# Condition 2: No wall has the work of only one student. Each wall has >= 2 distinct students.
for w in walls:
    # Count distinct students on wall w
    # For each student, check if they have any painting on wall w
    solver.add(Sum([If(Or(oil_wall[s] == w, water_wall[s] == w), 1, 0) for s in students]) >= 2)

# Condition 3: No wall has both Franz and Isaacs.
for w in walls:
    solver.add(Not(And(
        Or(oil_wall['F'] == w, water_wall['F'] == w),
        Or(oil_wall['I'] == w, water_wall['I'] == w)
    )))

# Condition 4: Greene's watercolor is upper position of the wall where Franz's oil is.
solver.add(water_wall['G'] == oil_wall['F'])
solver.add(water_pos['G'] == 0)

# Condition 5: Isaacs's oil is lower position of wall 4.
solver.add(oil_wall['I'] == 4)
solver.add(oil_pos['I'] == 1)

# Given: Franz's oil is on wall 1.
solver.add(oil_wall['F'] == 1)

# From condition 4: Greene's watercolor is on wall 1, upper position.
# So wall 1 upper = Greene's watercolor.
# Wall 1 lower must be someone else's painting (not Franz, not Greene's watercolor already used).
# Let's check what we can deduce.

# Let's first check if the base constraints are satisfiable at all.
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")
if result == sat:
    m = solver.model()
    for s in students:
        print(f"{s}: oil=({m[oil_wall[s]]},{m[oil_pos[s]]}), water=({m[water_wall[s]]},{m[water_pos[s]]})")

# Now evaluate each option
solver.push()
solver.add(water_wall['F'] == 4)
print(f"\nOption A (Franz water on wall 4): {solver.check()}")
solver.pop()

solver.push()
solver.add(oil_wall['G'] == 2)
print(f"Option B (Greene oil on wall 2): {solver.check()}")
solver.pop()

solver.push()
solver.add(water_wall['G'] == 2)
print(f"Option C (Greene water on wall 2): {solver.check()}")
solver.pop()

solver.push()
solver.add(water_wall['H'] == 3)
print(f"Option D (Hidalgo water on wall 3): {solver.check()}")
solver.pop()

solver.push()
solver.add(oil_wall['I'] == 1)
print(f"Option E (Isaacs oil on wall 1): {solver.check()}")
solver.pop()