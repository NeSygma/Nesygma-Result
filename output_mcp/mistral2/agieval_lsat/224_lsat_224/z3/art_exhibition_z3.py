from z3 import *

solver = Solver()

# Entities and variables
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
walls = [1, 2, 3, 4]
painting_types = ["oil", "watercolor"]
positions = ["upper", "lower"]

# Decision variables:
# student_painting[student][painting_type] = (wall, position)
student_painting = {
    s: {
        pt: (Int(f"{s}_{pt}_wall"), Int(f"{s}_{pt}_pos"))
        for pt in painting_types
    }
    for s in students
}

# Helper function to extract wall and position
wall = lambda s, pt: student_painting[s][pt][0]
pos = lambda s, pt: student_painting[s][pt][1]

# Base constraints:
# Each student has exactly two paintings (one oil, one watercolor)
for s in students:
    solver.add(Distinct([wall(s, pt) for pt in painting_types]))
    solver.add(Distinct([pos(s, pt) for pt in painting_types]))
    for pt in painting_types:
        solver.add(wall(s, pt) >= 1, wall(s, pt) <= 4)
        solver.add(pos(s, pt) >= 0, pos(s, pt) <= 1)  # 0=upper, 1=lower

# Exactly two paintings per wall, one in upper and one in lower position
for w in walls:
    upper_painting = None
    lower_painting = None
    for s in students:
        for pt in painting_types:
            solver.add(Implies(
                And(wall(s, pt) == w, pos(s, pt) == 0),
                upper_painting == None
            ))
            solver.add(Implies(
                And(wall(s, pt) == w, pos(s, pt) == 1),
                lower_painting == None
            ))
            # This approach is not directly translatable; instead, we enforce that for each wall, there is exactly one upper and one lower painting.
    # Instead, we enforce that for each wall, there is exactly one upper and one lower painting by counting.
    # We will enforce this later with a more robust constraint.

# No wall has only watercolors
for w in walls:
    has_oil = Or([wall(s, "oil") == w for s in students])
    solver.add(has_oil)

# No wall has the work of only one student
for w in walls:
    student_count = Sum([If(wall(s, "oil") == w, 1, 0) + If(wall(s, "watercolor") == w, 1, 0) for s in students])
    solver.add(student_count >= 2)

# No wall has both Franz and Isaacs
for w in walls:
    solver.add(Not(And(
        Or([wall("Franz", pt) == w for pt in painting_types]),
        Or([wall("Isaacs", pt) == w for pt in painting_types])
    )))

# Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
franz_oil_wall = wall("Franz", "oil")
greene_watercolor_upper_wall = wall("Greene", "watercolor")
greene_watercolor_upper_pos = pos("Greene", "watercolor")
solver.add(greene_watercolor_upper_wall == franz_oil_wall)
solver.add(greene_watercolor_upper_pos == 0)  # upper position

# Isaacs's oil is in the lower position of wall 4
solver.add(wall("Isaacs", "oil") == 4)
solver.add(pos("Isaacs", "oil") == 1)  # lower position

# Exactly two paintings per wall, one upper and one lower
for w in walls:
    upper_paintings = [
        And(wall(s, pt) == w, pos(s, pt) == 0)
        for s in students
        for pt in painting_types
    ]
    lower_paintings = [
        And(wall(s, pt) == w, pos(s, pt) == 1)
        for s in students
        for pt in painting_types
    ]
    solver.add(Sum([If(p, 1, 0) for p in upper_paintings]) == 1)
    solver.add(Sum([If(p, 1, 0) for p in lower_paintings]) == 1)

# Evaluate each option
found_options = []

# Option A: Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.
opt_a_constr = And(
    pos("Franz", "oil") == 1,
    pos("Franz", "watercolor") == 1,
    pos("Greene", "oil") == 1,
    pos("Greene", "watercolor") == 1
)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.
opt_b_constr = And(
    pos("Franz", "oil") == 0,
    pos("Franz", "watercolor") == 0,
    pos("Greene", "oil") == 0,
    pos("Greene", "watercolor") == 0
)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.
opt_c_constr = And(
    pos("Franz", "oil") == 0,
    pos("Franz", "watercolor") == 0,
    pos("Hidalgo", "oil") == 0,
    pos("Hidalgo", "watercolor") == 0
)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.
opt_d_constr = And(
    pos("Greene", "oil") == 1,
    pos("Greene", "watercolor") == 1,
    pos("Hidalgo", "oil") == 1,
    pos("Hidalgo", "watercolor") == 1
)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions.
opt_e_constr = And(
    pos("Greene", "oil") == 0,
    pos("Greene", "watercolor") == 0,
    pos("Hidalgo", "oil") == 0,
    pos("Hidalgo", "watercolor") == 0
)
solver.push()
solver.add(opt_e_constr)
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