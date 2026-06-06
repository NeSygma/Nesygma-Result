from z3 import *

# Create solver
solver = Solver()

# Define students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
student_to_idx = {s: i for i, s in enumerate(students)}

# Team assignment: 0 = Green, 1 = Red
team = [Int(f"team_{s}") for s in students]

# Facilitator status
facilitator = [Bool(f"fac_{s}") for s in students]

# Base constraints
# 1. Juana is assigned to a different team than Olga
solver.add(team[student_to_idx["Juana"]] != team[student_to_idx["Olga"]])

# 2. Lateefah is assigned to the green team (0)
solver.add(team[student_to_idx["Lateefah"]] == 0)

# 3. Kelly is not a facilitator
solver.add(Not(facilitator[student_to_idx["Kelly"]]))

# 4. Olga is a facilitator
solver.add(facilitator[student_to_idx["Olga"]])

# Additional condition for this question: Lateefah is a facilitator
solver.add(facilitator[student_to_idx["Lateefah"]])

# 5. Exactly one facilitator per team
# First, count facilitators on each team
green_facilitators = Sum([If(And(team[i] == 0, facilitator[i]), 1, 0) for i in range(5)])
red_facilitators = Sum([If(And(team[i] == 1, facilitator[i]), 1, 0) for i in range(5)])
solver.add(green_facilitators == 1)
solver.add(red_facilitators == 1)

# 6. Team sizes: one team has 2 members, other has 3 members
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# 7. All team assignments must be 0 or 1
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# Define answer choices as constraints
# (A) Juana and Kelly are both assigned to the red team
opt_a = And(team[student_to_idx["Juana"]] == 1, team[student_to_idx["Kelly"]] == 1)

# (B) Juana and Mei are both assigned to the red team
opt_b = And(team[student_to_idx["Juana"]] == 1, team[student_to_idx["Mei"]] == 1)

# (C) Lateefah and Olga are both assigned to the green team
opt_c = And(team[student_to_idx["Lateefah"]] == 0, team[student_to_idx["Olga"]] == 0)

# (D) Mei and Olga are both assigned to the green team
opt_d = And(team[student_to_idx["Mei"]] == 0, team[student_to_idx["Olga"]] == 0)

# (E) Mei and Olga are both assigned to the red team
opt_e = And(team[student_to_idx["Mei"]] == 1, team[student_to_idx["Olga"]] == 1)

# Test each option using the required skeleton
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")