from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# For each student, we have an oil and a watercolor.
# Each painting is assigned to a (wall, position).
oil_wall = {s: Int(f'oil_wall_{s}') for s in students}
oil_pos = {s: Int(f'oil_pos_{s}') for s in students}
water_wall = {s: Int(f'water_wall_{s}') for s in students}
water_pos = {s: Int(f'water_pos_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(oil_wall[s] >= 1, oil_wall[s] <= 4)
    solver.add(water_wall[s] >= 1, water_wall[s] <= 4)
    solver.add(oil_pos[s] >= 0, oil_pos[s] <= 1)  # 0=upper, 1=lower
    solver.add(water_pos[s] >= 0, water_pos[s] <= 1)

# Exactly two paintings per wall: one upper (pos 0), one lower (pos 1)
for w in [1, 2, 3, 4]:
    # Upper position count = 1
    solver.add(Sum([If(And(oil_wall[s] == w, oil_pos[s] == 0), 1, 0) for s in students] +
                   [If(And(water_wall[s] == w, water_pos[s] == 0), 1, 0) for s in students]) == 1)
    # Lower position count = 1
    solver.add(Sum([If(And(oil_wall[s] == w, oil_pos[s] == 1), 1, 0) for s in students] +
                   [If(And(water_wall[s] == w, water_pos[s] == 1), 1, 0) for s in students]) == 1)

# Condition 1: No wall has only watercolors. Each wall must have at least one oil.
for w in [1, 2, 3, 4]:
    solver.add(Or([oil_wall[s] == w for s in students]))

# Condition 2: No wall has the work of only one student. Each wall has >= 2 distinct students.
for w in [1, 2, 3, 4]:
    solver.add(Sum([If(Or(oil_wall[s] == w, water_wall[s] == w), 1, 0) for s in students]) >= 2)

# Condition 3: No wall has both Franz and Isaacs.
for w in [1, 2, 3, 4]:
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
# So wall 1: upper = Greene's watercolor, lower = ? (must be someone else's oil, since no wall has only watercolors)

# Now evaluate each option using the LSAT skeleton
found_options = []

# Option A: Franz's watercolor is displayed on wall 4.
opt_a = water_wall['F'] == 4
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Greene's oil is displayed on wall 2.
opt_b = oil_wall['G'] == 2
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Greene's watercolor is displayed on wall 2.
opt_c = water_wall['G'] == 2
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Hidalgo's watercolor is displayed on wall 3.
opt_d = water_wall['H'] == 3
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Isaacs's oil is displayed on wall 1.
opt_e = oil_wall['I'] == 1
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
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