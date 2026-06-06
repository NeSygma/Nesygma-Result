from z3 import *

# Create solver
solver = Solver()

# Define students and teams
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
teams = ["green", "red"]

# Create team assignment variables (0 = green, 1 = red)
team = {s: Int(f"team_{s}") for s in students}
for s in students:
    solver.add(team[s] >= 0, team[s] <= 1)

# Create facilitator variables
facilitator = {s: Bool(f"facilitator_{s}") for s in students}

# Constraint 1: One team has 2 members, the other has 3 members
# Count members on green team
green_count = Sum([If(team[s] == 0, 1, 0) for s in students])
solver.add(Or(green_count == 2, green_count == 3))

# Constraint 2: One member of each team is a facilitator
# For each team, exactly one facilitator
for t in [0, 1]:  # 0 = green, 1 = red
    facilitator_count = Sum([If(And(team[s] == t, facilitator[s]), 1, 0) for s in students])
    solver.add(facilitator_count == 1)

# Constraint 3: Juana is assigned to a different team than Olga
solver.add(team["Juana"] != team["Olga"])

# Constraint 4: Lateefah is assigned to the green team
solver.add(team["Lateefah"] == 0)

# Constraint 5: Kelly is not a facilitator
solver.add(Not(facilitator["Kelly"]))

# Constraint 6: Olga is a facilitator
solver.add(facilitator["Olga"])

# Now evaluate each answer choice for MUST BE TRUE
# For each option, check if its negation is unsatisfiable
# If negation is unsat, then the option must be true in all models

# (A) Juana is assigned to the red team
opt_a = (team["Juana"] == 1)

# (B) Lateefah is a facilitator
opt_b = facilitator["Lateefah"]

# (C) Olga is assigned to the green team
opt_c = (team["Olga"] == 0)

# (D) Juana and Mei are not both facilitators
opt_d = Not(And(facilitator["Juana"], facilitator["Mei"]))

# (E) Neither Juana nor Kelly is a facilitator
opt_e = And(Not(facilitator["Juana"]), Not(facilitator["Kelly"]))

# Test each option's negation
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    # Create a new solver for each test
    test_solver = Solver()
    # Add all base constraints
    for s in students:
        test_solver.add(team[s] >= 0, team[s] <= 1)
    test_solver.add(Or(green_count == 2, green_count == 3))
    for t in [0, 1]:
        facilitator_count = Sum([If(And(team[s] == t, facilitator[s]), 1, 0) for s in students])
        test_solver.add(facilitator_count == 1)
    test_solver.add(team["Juana"] != team["Olga"])
    test_solver.add(team["Lateefah"] == 0)
    test_solver.add(Not(facilitator["Kelly"]))
    test_solver.add(facilitator["Olga"])
    
    # Add negation of the option
    test_solver.add(Not(constr))
    
    # Check if negation is unsatisfiable
    if test_solver.check() == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")