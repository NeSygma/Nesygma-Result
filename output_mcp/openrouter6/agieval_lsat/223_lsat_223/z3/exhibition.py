from z3 import *

solver = Solver()

# Define slot indices for each painting (0..7)
s_F_oil = Int('s_F_oil')
s_F_water = Int('s_F_water')
s_G_oil = Int('s_G_oil')
s_G_water = Int('s_G_water')
s_H_oil = Int('s_H_oil')
s_H_water = Int('s_H_water')
s_I_oil = Int('s_I_oil')
s_I_water = Int('s_I_water')

# All slot indices must be distinct and in range 0..7
all_slots = [s_F_oil, s_F_water, s_G_oil, s_G_water, s_H_oil, s_H_water, s_I_oil, s_I_water]
solver.add([And(s >= 0, s <= 7) for s in all_slots])
solver.add(Distinct(all_slots))

# Helper functions to get wall and position from slot
def wall(s):
    return s // 2 + 1

def position(s):
    return s % 2  # 0 = upper, 1 = lower

# Base constraints from problem statement

# 1. No wall has only watercolors: each wall must have at least one oil painting
for w in range(1, 5):
    solver.add(Or(
        wall(s_F_oil) == w,
        wall(s_G_oil) == w,
        wall(s_H_oil) == w,
        wall(s_I_oil) == w
    ))

# 2. No wall has the work of only one student: each wall must have paintings from at least two different students.
#    Since each wall has exactly two paintings, this means the two paintings on a wall must be from different students.
#    We enforce that for each student, at most one painting per wall.
for w in range(1, 5):
    # Franz
    solver.add(Sum([If(wall(s_F_oil) == w, 1, 0), If(wall(s_F_water) == w, 1, 0)]) <= 1)
    # Greene
    solver.add(Sum([If(wall(s_G_oil) == w, 1, 0), If(wall(s_G_water) == w, 1, 0)]) <= 1)
    # Hidalgo
    solver.add(Sum([If(wall(s_H_oil) == w, 1, 0), If(wall(s_H_water) == w, 1, 0)]) <= 1)
    # Isaacs
    solver.add(Sum([If(wall(s_I_oil) == w, 1, 0), If(wall(s_I_water) == w, 1, 0)]) <= 1)

# 3. No wall has both a painting by Franz and a painting by Isaacs
for w in range(1, 5):
    solver.add(Not(And(
        Or(wall(s_F_oil) == w, wall(s_F_water) == w),
        Or(wall(s_I_oil) == w, wall(s_I_water) == w)
    )))

# 4. Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(wall(s_G_water) == wall(s_F_oil))
solver.add(position(s_G_water) == 0)  # upper

# 5. Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall(s_I_oil) == 4)
solver.add(position(s_I_oil) == 1)  # lower

# Additional condition for the question: Franz's oil is on wall 1.
solver.add(wall(s_F_oil) == 1)

# Now test each option
found_options = []

# Option A: Franz's watercolor is displayed on wall 4.
opt_a = (wall(s_F_water) == 4)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Greene's oil is displayed on wall 2.
opt_b = (wall(s_G_oil) == 2)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's watercolor is displayed on wall 2.
opt_c = (wall(s_G_water) == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's watercolor is displayed on wall 3.
opt_d = (wall(s_H_water) == 3)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Isaacs's oil is displayed on wall 1.
opt_e = (wall(s_I_oil) == 1)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")