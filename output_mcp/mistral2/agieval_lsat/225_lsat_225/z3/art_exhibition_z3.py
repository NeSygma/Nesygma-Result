from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare students and walls
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
walls = [1, 2, 3, 4]

# Declare paintings: oil and watercolor for each student
# We represent paintings as tuples (student, medium, wall, position)
# where medium is "oil" or "watercolor", and position is "upper" or "lower"
paintings = {}
for s in students:
    for m in ["oil", "watercolor"]:
        paintings[(s, m)] = (Int(f"wall_{s}_{m}"), Int(f"pos_{s}_{m}"))

# Helper function to extract wall and position
wall = lambda s, m: paintings[(s, m)][0]
pos = lambda s, m: paintings[(s, m)][1]

# Position constants
UPPER = 0
LOWER = 1

# Constraints
solver = Solver()

# 1. Each wall has exactly two paintings: one upper, one lower
for w in walls:
    # Exactly one painting is upper on wall w
    solver.add(Sum([If(And(wall(s, m) == w, pos(s, m) == UPPER), 1, 0) for s in students for m in ["oil", "watercolor"]]) == 1)
    # Exactly one painting is lower on wall w
    solver.add(Sum([If(And(wall(s, m) == w, pos(s, m) == LOWER), 1, 0) for s in students for m in ["oil", "watercolor"]]) == 1)

# 2. No wall has only watercolors
for w in walls:
    # At least one oil painting on wall w
    solver.add(Sum([If(And(wall(s, "oil") == w, pos(s, "oil") == UPPER), 1, 0) for s in students]) + 
                Sum([If(And(wall(s, "oil") == w, pos(s, "oil") == LOWER), 1, 0) for s in students]) >= 1)

# 3. No wall has the work of only one student
for w in walls:
    # At least two distinct students have paintings on wall w
    # We use a list of student names for Distinct
    # Instead of using a list comprehension with symbolic expressions, we use a sum of bools
    has_painting = [
        Or(
            And(wall(s, "oil") == w, pos(s, "oil") == UPPER),
            And(wall(s, "oil") == w, pos(s, "oil") == LOWER),
            And(wall(s, "watercolor") == w, pos(s, "watercolor") == UPPER),
            And(wall(s, "watercolor") == w, pos(s, "watercolor") == LOWER)
        )
        for s in students
    ]
    # Ensure at least two students have paintings on wall w
    solver.add(Sum([If(h, 1, 0) for h in has_painting]) >= 2)

# 4. No wall has both Franz and Isaacs
for w in walls:
    solver.add(Not(And(Or(wall("Franz", "oil") == w, wall("Franz", "watercolor") == w),
                       Or(wall("Isaacs", "oil") == w, wall("Isaacs", "watercolor") == w))))

# 5. Greene's watercolor is in the upper position of the wall on which Franz's oil is displayed
solver.add(And(wall("Greene", "watercolor") == wall("Franz", "oil"),
               pos("Greene", "watercolor") == UPPER))

# 6. Isaacs's oil is in the lower position of wall 4
solver.add(And(wall("Isaacs", "oil") == 4, pos("Isaacs", "oil") == LOWER))

# Additional constraints to ensure each student has exactly two paintings (one oil, one watercolor)
for s in students:
    solver.add(wall(s, "oil") >= 1, wall(s, "oil") <= 4)
    solver.add(wall(s, "watercolor") >= 1, wall(s, "watercolor") <= 4)
    solver.add(Or(pos(s, "oil") == UPPER, pos(s, "oil") == LOWER))
    solver.add(Or(pos(s, "watercolor") == UPPER, pos(s, "watercolor") == LOWER))

# Now, evaluate each option to see which one CANNOT be true
found_options = []

# Option A: Franz's watercolor is displayed on the same wall as Greene's oil
opt_a_constr = (wall("Franz", "watercolor") == wall("Greene", "oil"))
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Franz's watercolor is displayed on the same wall as Hidalgo's oil
opt_b_constr = (wall("Franz", "watercolor") == wall("Hidalgo", "oil"))
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's oil is displayed in an upper position
opt_c_constr = (pos("Greene", "oil") == UPPER)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's watercolor is displayed in a lower position
opt_d_constr = (pos("Hidalgo", "watercolor") == LOWER)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Isaacs's watercolor is displayed on the same wall as Hidalgo's oil
opt_e_constr = (wall("Isaacs", "watercolor") == wall("Hidalgo", "oil"))
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")