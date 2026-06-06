from z3 import *

# We will evaluate each option in isolation with all base constraints
found_options = []

# Base constraints (common to all options)
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Iterate over each option and check if it satisfies all constraints
for letter, opt_constr in [
    ("A", lambda s, t, f: And(
        t["Juana"] == 0, t["Lateefah"] == 0, t["Olga"] == 0,
        t["Kelly"] == 1, t["Mei"] == 1,
        f["Olga"] == True, f["Mei"] == True,
        Sum([f[s] for s in students]) == 2,
        Sum([t[s] == 0 for s in students]) == 3,
        Sum([t[s] == 1 for s in students]) == 2
    )),
    ("B", lambda s, t, f: And(
        t["Kelly"] == 0, t["Lateefah"] == 0, t["Olga"] == 0,
        t["Juana"] == 1, t["Mei"] == 1,
        f["Lateefah"] == True, f["Mei"] == True,
        Sum([f[s] for s in students]) == 2,
        Sum([t[s] == 0 for s in students]) == 3,
        Sum([t[s] == 1 for s in students]) == 2
    )),
    ("C", lambda s, t, f: And(
        t["Kelly"] == 0, t["Lateefah"] == 0, t["Olga"] == 0,
        t["Juana"] == 1, t["Mei"] == 1,
        f["Olga"] == True, f["Juana"] == True,
        Sum([f[s] for s in students]) == 2,
        Sum([t[s] == 0 for s in students]) == 3,
        Sum([t[s] == 1 for s in students]) == 2
    )),
    ("D", lambda s, t, f: And(
        t["Kelly"] == 0, t["Mei"] == 0, t["Olga"] == 0,
        t["Juana"] == 1, t["Lateefah"] == 1,
        f["Olga"] == True, f["Juana"] == True,
        Sum([f[s] for s in students]) == 2,
        Sum([t[s] == 0 for s in students]) == 3,
        Sum([t[s] == 1 for s in students]) == 2
    )),
    ("E", lambda s, t, f: And(
        t["Lateefah"] == 0, t["Olga"] == 0,
        t["Juana"] == 1, t["Kelly"] == 1, t["Mei"] == 1,
        f["Olga"] == True, f["Kelly"] == True,
        Sum([f[s] for s in students]) == 2,
        Sum([t[s] == 0 for s in students]) == 2,
        Sum([t[s] == 1 for s in students]) == 3
    ))
]:
    solver = Solver()
    
    # Declare team and facilitator variables
    team = {s: Int(f"team_{s}") for s in students}
    facilitator = {s: Bool(f"facilitator_{s}") for s in students}
    
    # Base constraints (not tied to any option)
    # Lateefah is on the green team
    solver.add(team["Lateefah"] == 0)
    # Kelly is not a facilitator
    solver.add(Not(facilitator["Kelly"]))
    # Olga is a facilitator
    solver.add(facilitator["Olga"])
    # Juana and Olga are on different teams
    solver.add(team["Juana"] != team["Olga"])
    # Team sizes: one team has 2 members, the other has 3
    solver.add(Or(
        And(Sum([team[s] == 0 for s in students]) == 2, Sum([team[s] == 1 for s in students]) == 3),
        And(Sum([team[s] == 0 for s in students]) == 3, Sum([team[s] == 1 for s in students]) == 2)
    ))
    # Exactly one facilitator per team
    solver.add(Or(
        And(Sum([facilitator[s] for s in students if team[s] == 0]) == 1,
            Sum([facilitator[s] for s in students if team[s] == 1]) == 1)
    ))
    
    # Add the option-specific constraints
    solver.add(opt_constr(students, team, facilitator))
    
    # Check if the option is valid
    if solver.check() == sat:
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