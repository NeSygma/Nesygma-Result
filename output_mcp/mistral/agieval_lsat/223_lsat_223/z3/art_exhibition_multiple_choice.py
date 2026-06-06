from z3 import *

# Students: 0=Franz, 1=Greene, 2=Hidalgo, 3=Isaacs
# Walls: 0=Wall1, 1=Wall2, 2=Wall3, 3=Wall4
# Positions: 0=upper, 1=lower

solver = Solver()

# Wall assignments
upper_student = [Int(f'upper_student_{w}') for w in range(4)]
lower_student = [Int(f'lower_student_{w}') for w in range(4)]
upper_type = [Int(f'upper_type_{w}') for w in range(4)]  # 0=watercolor, 1=oil
lower_type = [Int(f'lower_type_{w}') for w in range(4)]  # 0=watercolor, 1=oil

# Each student has exactly one oil and one watercolor painting
for s in range(4):
    # Oil: exactly one painting of type oil for student s
    solver.add(Sum([If(And(upper_student[w] == s, upper_type[w] == 1), 1, 0) for w in range(4)] +
                   [If(And(lower_student[w] == s, lower_type[w] == 1), 1, 0) for w in range(4)]) == 1)
    # Watercolor: exactly one painting of type watercolor for student s
    solver.add(Sum([If(And(upper_student[w] == s, upper_type[w] == 0), 1, 0) for w in range(4)] +
                   [If(And(lower_student[w] == s, lower_type[w] == 0), 1, 0) for w in range(4)]) == 1)

# Each wall has two different students
for w in range(4):
    solver.add(upper_student[w] != lower_student[w])

# No wall has only watercolors
for w in range(4):
    solver.add(Or(upper_type[w] == 1, lower_type[w] == 1))

# No wall has both Franz (0) and Isaacs (3)
for w in range(4):
    solver.add(Not(And(upper_student[w] == 0, lower_student[w] == 3)))
    solver.add(Not(And(upper_student[w] == 3, lower_student[w] == 0)))

# Greene's watercolor is in upper position of wall where Franz's oil is
# For each wall w, if Franz's oil is in upper position, then Greene's watercolor must be in upper position of w
for w in range(4):
    solver.add(Implies(
        And(upper_student[w] == 0, upper_type[w] == 1),
        And(upper_student[w] == 1, upper_type[w] == 0)
    ))

# Isaacs's oil is in lower position of wall 4
solver.add(lower_student[3] == 3)
solver.add(lower_type[3] == 1)

# Franz's oil is on wall 1 (wall index 0) in upper position
solver.add(upper_student[0] == 0)
solver.add(upper_type[0] == 1)

# Domain constraints
for w in range(4):
    for var in [upper_student[w], lower_student[w]]:
        solver.add(var >= 0, var <= 3)  # students 0-3
    for var in [upper_type[w], lower_type[w]]:
        solver.add(var >= 0, var <= 1)  # 0=watercolor, 1=oil

# Now evaluate the multiple choice options
found_options = []

# Option A: Franz's watercolor is displayed on wall 4 (wall index 3)
# Franz's watercolor must be on a wall where Franz is in either upper or lower position with type watercolor
solver.push()
solver.add(Or(
    And(upper_student[3] == 0, upper_type[3] == 0),
    And(lower_student[3] == 0, lower_type[3] == 0)
))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Greene's oil is displayed on wall 2 (wall index 1)
solver.push()
solver.add(Or(
    And(upper_student[1] == 1, upper_type[1] == 1),
    And(lower_student[1] == 1, lower_type[1] == 1)
))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's watercolor is displayed on wall 2 (wall index 1)
solver.push()
solver.add(Or(
    And(upper_student[1] == 1, upper_type[1] == 0),
    And(lower_student[1] == 1, lower_type[1] == 0)
))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's watercolor is displayed on wall 3 (wall index 2)
solver.push()
solver.add(Or(
    And(upper_student[2] == 2, upper_type[2] == 0),
    And(lower_student[2] == 2, lower_type[2] == 0)
))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Isaacs's oil is displayed on wall 1 (wall index 0)
solver.push()
solver.add(Or(
    And(upper_student[0] == 3, upper_type[0] == 1),
    And(lower_student[0] == 3, lower_type[0] == 1)
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