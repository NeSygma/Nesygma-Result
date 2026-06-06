from z3 import *

# Base constraints solver
solver = Solver()

# Students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Team assignment: 0 = green, 1 = red
team = {s: Int(f"team_{s}") for s in students}
# Facilitator assignment: True if facilitator
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Base constraints
# 1. Lateefah is on the green team
solver.add(team["Lateefah"] == 0)

# 2. Juana and Olga are on different teams
solver.add(team["Juana"] != team["Olga"])

# 3. Kelly is not a facilitator
solver.add(Not(facilitator["Kelly"]))

# 4. Olga is a facilitator
solver.add(facilitator["Olga"])

# 5. Exactly one facilitator per team
# Count facilitators per team
green_facilitators = Sum([If(And(team[s] == 0, facilitator[s]), 1, 0) for s in students])
red_facilitators = Sum([If(And(team[s] == 1, facilitator[s]), 1, 0) for s in students])
solver.add(green_facilitators == 1)
solver.add(red_facilitators == 1)

# 6. Team sizes: one team has 2 members, the other has 3
green_size = Sum([If(team[s] == 0, 1, 0) for s in students])
red_size = Sum([If(team[s] == 1, 1, 0) for s in students])
solver.add(Or(And(green_size == 2, red_size == 3), And(green_size == 3, red_size == 2)))

# 7. Each student is on exactly one team
for s in students:
    solver.add(team[s] >= 0, team[s] <= 1)

# Now evaluate each option
found_options = []

# Option A: green team: Juana, Lateefah, Olga (facilitator); red team: Kelly, Mei (facilitator)
opt_a_constr = And(
    team["Juana"] == 0,
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Kelly"] == 1,
    team["Mei"] == 1,
    facilitator["Juana"] == False,
    facilitator["Lateefah"] == False,
    facilitator["Olga"] == True,
    facilitator["Kelly"] == False,
    facilitator["Mei"] == True,
)

# Option B: green team: Kelly, Lateefah (facilitator), Olga; red team: Juana, Mei (facilitator)
opt_b_constr = And(
    team["Kelly"] == 0,
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Mei"] == 1,
    facilitator["Kelly"] == False,
    facilitator["Lateefah"] == True,
    facilitator["Olga"] == False,
    facilitator["Juana"] == False,
    facilitator["Mei"] == True,
)

# Option C: green team: Kelly, Lateefah, Olga (facilitator); red team: Juana (facilitator), Mei
opt_c_constr = And(
    team["Kelly"] == 0,
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Mei"] == 1,
    facilitator["Kelly"] == False,
    facilitator["Lateefah"] == False,
    facilitator["Olga"] == True,
    facilitator["Juana"] == True,
    facilitator["Mei"] == False,
)

# Option D: green team: Kelly, Mei, Olga (facilitator); red team: Juana (facilitator), Lateefah
opt_d_constr = And(
    team["Kelly"] == 0,
    team["Mei"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Lateefah"] == 1,
    facilitator["Kelly"] == False,
    facilitator["Mei"] == False,
    facilitator["Olga"] == True,
    facilitator["Juana"] == True,
    facilitator["Lateefah"] == False,
)

# Option E: green team: Lateefah, Olga (facilitator); red team: Juana, Kelly (facilitator), Mei
opt_e_constr = And(
    team["Lateefah"] == 0,
    team["Olga"] == 0,
    team["Juana"] == 1,
    team["Kelly"] == 1,
    team["Mei"] == 1,
    facilitator["Lateefah"] == False,
    facilitator["Olga"] == True,
    facilitator["Juana"] == False,
    facilitator["Kelly"] == False,
    facilitator["Mei"] == False,
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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