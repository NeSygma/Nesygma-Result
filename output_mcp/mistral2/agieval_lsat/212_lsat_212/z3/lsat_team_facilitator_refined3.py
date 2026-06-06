from z3 import *

solver = Solver()

# Declare team assignments: 0 = green, 1 = red
# Students: Juana, Kelly, Lateefah, Mei, Olga
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
team = {s: Int(f"team_{s}") for s in students}

# Facilitator assignments: 0 = not facilitator, 1 = facilitator
facilitator = {s: Int(f"facilitator_{s}") for s in students}

# Base constraints
# Each student is on exactly one team (0 or 1)
for s in students:
    solver.add(Or(team[s] == 0, team[s] == 1))
    solver.add(Or(facilitator[s] == 0, facilitator[s] == 1))

# Exactly one team has 2 members, the other has 3
solver.add(Or(
    And(Sum([If(team[s] == 0, 1, 0) for s in students]) == 2, Sum([If(team[s] == 1, 1, 0) for s in students]) == 3),
    And(Sum([If(team[s] == 0, 1, 0) for s in students]) == 3, Sum([If(team[s] == 1, 1, 0) for s in students]) == 2)
))

# Facilitator constraints
# Each team must have exactly one facilitator
solver.add(Sum([If(And(facilitator[s] == 1, team[s] == 0), 1, 0) for s in students]) == 1)  # Green team facilitator
solver.add(Sum([If(And(facilitator[s] == 1, team[s] == 1), 1, 0) for s in students]) == 1)  # Red team facilitator

# Problem-specific constraints
solver.add(team["Lateefah"] == 0)  # Lateefah is on the green team
solver.add(facilitator["Kelly"] == 0)  # Kelly is not a facilitator
solver.add(facilitator["Olga"] == 1)  # Olga is a facilitator
solver.add(team["Juana"] != team["Olga"])  # Juana and Olga are on different teams

# Additional constraint: Mei is on the green team (from the question)
solver.add(team["Mei"] == 0)

# Now evaluate the multiple choice options
found_options = []

# Option A: Juana is assigned to the green team
solver.push()
solver.add(team["Juana"] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Kelly is assigned to the red team
solver.push()
solver.add(team["Kelly"] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Olga is assigned to the green team
solver.push()
solver.add(team["Olga"] == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Lateefah is a facilitator
solver.push()
solver.add(facilitator["Lateefah"] == 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Mei is a facilitator
solver.push()
solver.add(facilitator["Mei"] == 1)
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