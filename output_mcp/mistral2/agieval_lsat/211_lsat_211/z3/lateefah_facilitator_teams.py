from z3 import *

solver = Solver()

# Declare students and teams
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
teams = ["green", "red"]

# Assign each student to a team (0: green, 1: red)
team_assignment = {s: Int(f"team_{s}") for s in students}
for s in students:
    solver.add(Or(team_assignment[s] == 0, team_assignment[s] == 1))

# Facilitator assignment (True if the student is a facilitator)
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Constraints from the problem statement
# 1. Juana is assigned to a different team than Olga
solver.add(team_assignment["Juana"] != team_assignment["Olga"])

# 2. Lateefah is assigned to the green team
solver.add(team_assignment["Lateefah"] == 0)

# 3. Kelly is not a facilitator
solver.add(Not(facilitator["Kelly"]))

# 4. Olga is a facilitator
solver.add(facilitator["Olga"])

# 5. Lateefah is a facilitator (additional condition for the question)
solver.add(facilitator["Lateefah"])

# 6. One team has 2 members, the other has 3
# Count the number of students in the green team
count_green = Sum([If(team_assignment[s] == 0, 1, 0) for s in students])
solver.add(Or(count_green == 2, count_green == 3))

# The other team must have the remaining members
# If green has 2, red has 3, and vice versa
solver.add(Not(And(count_green == 2, count_green == 3)))

# 7. Exactly one facilitator per team
# Count facilitators in green team
facilitators_green = Sum([If(And(team_assignment[s] == 0, facilitator[s]), 1, 0) for s in students])
solver.add(facilitators_green == 1)

# Count facilitators in red team
facilitators_red = Sum([If(And(team_assignment[s] == 1, facilitator[s]), 1, 0) for s in students])
solver.add(facilitators_red == 1)

# Evaluate each option
found_options = []

# Option A: Juana and Kelly are both assigned to the red team
opt_a_constr = And(
    team_assignment["Juana"] == 1,
    team_assignment["Kelly"] == 1
)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Juana and Mei are both assigned to the red team
opt_b_constr = And(
    team_assignment["Juana"] == 1,
    team_assignment["Mei"] == 1
)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Lateefah and Olga are both assigned to the green team
opt_c_constr = And(
    team_assignment["Lateefah"] == 0,
    team_assignment["Olga"] == 0
)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Mei and Olga are both assigned to the green team
opt_d_constr = And(
    team_assignment["Mei"] == 0,
    team_assignment["Olga"] == 0
)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Mei and Olga are both assigned to the red team
opt_e_constr = And(
    team_assignment["Mei"] == 1,
    team_assignment["Olga"] == 1
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