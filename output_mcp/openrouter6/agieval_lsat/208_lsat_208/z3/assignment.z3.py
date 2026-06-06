from z3 import *

solver = Solver()

# Define students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
idx = {s: i for i, s in enumerate(students)}

# Variables: team[i] = True if green, False if red
team = [Bool(f"team_{s}") for s in students]
# Variables: facilitator[i] = True if facilitator
fac = [Bool(f"fac_{s}") for s in students]

# Base constraints
# 1. Lateefah is green
solver.add(team[idx["Lateefah"]] == True)
# 2. Kelly is not a facilitator
solver.add(fac[idx["Kelly"]] == False)
# 3. Olga is a facilitator
solver.add(fac[idx["Olga"]] == True)
# 4. Juana and Olga are on different teams
solver.add(team[idx["Juana"]] != team[idx["Olga"]])
# 5. Team size condition: green team has 2 or 3 members
green_count = Sum([If(team[i], 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))
# 6. Exactly one facilitator per team
green_fac_count = Sum([If(And(team[i], fac[i]), 1, 0) for i in range(5)])
red_fac_count = Sum([If(And(Not(team[i]), fac[i]), 1, 0) for i in range(5)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Define option constraints
def option_constraints(opt):
    # opt is a list of tuples (student, team_bool, fac_bool)
    constraints = []
    for s, t, f in opt:
        i = idx[s]
        constraints.append(team[i] == t)
        constraints.append(fac[i] == f)
    return constraints

# Option A
opt_a = [
    ("Juana", True, False),
    ("Lateefah", True, False),
    ("Olga", True, True),
    ("Kelly", False, False),
    ("Mei", False, True)
]

# Option B
opt_b = [
    ("Kelly", True, False),
    ("Lateefah", True, True),
    ("Olga", True, False),
    ("Juana", False, False),
    ("Mei", False, True)
]

# Option C
opt_c = [
    ("Kelly", True, False),
    ("Lateefah", True, False),
    ("Olga", True, True),
    ("Juana", False, True),
    ("Mei", False, False)
]

# Option D
opt_d = [
    ("Kelly", True, False),
    ("Mei", True, False),
    ("Olga", True, True),
    ("Juana", False, True),
    ("Lateefah", False, False)
]

# Option E
opt_e = [
    ("Lateefah", True, False),
    ("Olga", True, True),
    ("Juana", False, False),
    ("Kelly", False, True),
    ("Mei", False, False)
]

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(option_constraints(constr))
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