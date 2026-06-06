from z3 import *

solver = Solver()

# Base constraints (not tied to any option)
# Students: Juana, Kelly, Lateefah, Mei, Olga
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Team assignments: 0 = green, 1 = red
team = {s: Int(f"team_{s}") for s in students}
for s in students:
    solver.add(Or(team[s] == 0, team[s] == 1))

# Facilitator assignments
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Constraints:
# 1. Lateefah is on the green team
solver.add(team["Lateefah"] == 0)

# 2. Juana and Olga are on different teams
solver.add(team["Juana"] != team["Olga"])

# 3. Kelly is not a facilitator
solver.add(Not(facilitator["Kelly"]))

# 4. Olga is a facilitator
solver.add(facilitator["Olga"])

# Team sizes: one team has 2 members, the other has 3
green_members = [s for s in students if team[s] == 0]
red_members = [s for s in students if team[s] == 1]
solver.add(Or(
    And(Sum([team[s] == 0 for s in students]) == 2, Sum([team[s] == 1 for s in students]) == 3),
    And(Sum([team[s] == 0 for s in students]) == 3, Sum([team[s] == 1 for s in students]) == 2)
))

# Facilitators: one per team
solver.add(Or(
    And(Sum([facilitator[s] for s in students if team[s] == 0]) == 1,
        Sum([facilitator[s] for s in students if team[s] == 1]) == 1)
))

# Now evaluate each option
found_options = []

# Option A: green team: Juana, Lateefah, Olga (facilitator); red team: Kelly, Mei (facilitator)
opt_a_constr = And(
    team["Juana"] == 0,
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Kelly"] == 1,
    team["Mei"] == 1,
    facilitator["Olga"] == True,
    facilitator["Mei"] == True,
    Sum([facilitator[s] for s in students]) == 2  # Only two facilitators (one per team)
)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: green team: Kelly, Lateefah (facilitator), Olga; red team: Juana, Mei (facilitator)
opt_b_constr = And(
    team["Kelly"] == 0,
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Mei"] == 1,
    facilitator["Lateefah"] == True,
    facilitator["Mei"] == True,
    Sum([facilitator[s] for s in students]) == 2
)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: green team: Kelly, Lateefah, Olga (facilitator); red team: Juana (facilitator), Mei
opt_c_constr = And(
    team["Kelly"] == 0,
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Mei"] == 1,
    facilitator["Olga"] == True,
    facilitator["Juana"] == True,
    Sum([facilitator[s] for s in students]) == 2
)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: green team: Kelly, Mei, Olga (facilitator); red team: Juana (facilitator), Lateefah
opt_d_constr = And(
    team["Kelly"] == 0,
    team["Mei"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Lateefah"] == 1,
    facilitator["Olga"] == True,
    facilitator["Juana"] == True,
    Sum([facilitator[s] for s in students]) == 2
)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: green team: Lateefah, Olga (facilitator); red team: Juana, Kelly (facilitator), Mei
opt_e_constr = And(
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Kelly"] == 1,
    team["Mei"] == 1,
    facilitator["Olga"] == True,
    facilitator["Kelly"] == True,
    Sum([facilitator[s] for s in students]) == 2
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