from z3 import *

# Create solver
solver = Solver()

# Define students and teams
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
team_green = 0
team_red = 1

# Create variables: team assignment for each student (0 = green, 1 = red)
team = {s: Int(f"team_{s}") for s in students}

# Create variables: facilitator status for each student (0 = not facilitator, 1 = facilitator)
facilitator = {s: Int(f"facilitator_{s}") for s in students}

# Add domain constraints: team assignments must be 0 or 1
for s in students:
    solver.add(Or(team[s] == team_green, team[s] == team_red))

# Add domain constraints: facilitator status must be 0 or 1
for s in students:
    solver.add(Or(facilitator[s] == 0, facilitator[s] == 1))

# Condition 1: Juana is assigned to a different team than Olga
solver.add(team["Juana"] != team["Olga"])

# Condition 2: Lateefah is assigned to the green team
solver.add(team["Lateefah"] == team_green)

# Condition 3: Kelly is not a facilitator
solver.add(facilitator["Kelly"] == 0)

# Condition 4: Olga is a facilitator
solver.add(facilitator["Olga"] == 1)

# Additional constraints:
# 1. One team has 2 members, the other has 3 members
team_sizes = [Sum([If(team[s] == t, 1, 0) for s in students]) for t in [team_green, team_red]]
solver.add(Or(
    And(team_sizes[0] == 2, team_sizes[1] == 3),
    And(team_sizes[0] == 3, team_sizes[1] == 2)
))

# 2. Each team has exactly one facilitator
facilitators_per_team = [Sum([If(And(team[s] == t, facilitator[s] == 1), 1, 0) for s in students]) for t in [team_green, team_red]]
solver.add(facilitators_per_team[0] == 1)
solver.add(facilitators_per_team[1] == 1)

# 3. Total facilitators = 2 (one per team)
solver.add(Sum([facilitator[s] for s in students]) == 2)

# Now test each option to see which one MUST be false
# For each option, we check if adding it makes the problem unsatisfiable
# If it does, then that option must be false

# Option A: Lateefah is a facilitator, and she is assigned to the same team as Kelly is
opt_a = And(facilitator["Lateefah"] == 1, team["Lateefah"] == team["Kelly"])

# Option B: Mei is a facilitator, and she is assigned to the same team as Kelly is
opt_b = And(facilitator["Mei"] == 1, team["Mei"] == team["Kelly"])

# Option C: Olga is a facilitator, and she is assigned to the same team as Mei is
opt_c = And(facilitator["Olga"] == 1, team["Olga"] == team["Mei"])

# Option D: Lateefah is a facilitator, and she is assigned to a different team than Juana is
opt_d = And(facilitator["Lateefah"] == 1, team["Lateefah"] != team["Juana"])

# Option E: Mei is a facilitator, and she is assigned to a different team than Olga is
opt_e = And(facilitator["Mei"] == 1, team["Mei"] != team["Olga"])

# Test each option
must_be_false = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    solver.pop()
    if result == unsat:
        must_be_false.append(letter)

# Print results
if len(must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false[0]}")
elif len(must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be false {must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be false")