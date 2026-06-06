from z3 import *

# Define students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
# Map student names to indices for easier reference
idx = {s: i for i, s in enumerate(students)}

# Variables: team assignment (0 = green, 1 = red)
team = [Int(f"team_{s}") for s in students]
# Variables: facilitator status
fac = [Bool(f"fac_{s}") for s in students]

solver = Solver()

# Base constraints

# 1. Each student assigned to exactly one team (domain 0 or 1)
for t in team:
    solver.add(Or(t == 0, t == 1))

# 2. Team sizes: one team has 2 members, the other has 3
count_green = Sum([If(t == 0, 1, 0) for t in team])
count_red = Sum([If(t == 1, 1, 0) for t in team])
solver.add(Or(
    And(count_green == 2, count_red == 3),
    And(count_green == 3, count_red == 2)
))

# 3. Exactly one facilitator per team
for team_val in [0, 1]:
    facilitators_on_team = [If(team[i] == team_val, If(fac[i], 1, 0), 0) for i in range(len(students))]
    solver.add(Sum(facilitators_on_team) == 1)

# 4. Juana is assigned to a different team than Olga
solver.add(team[idx["Juana"]] != team[idx["Olga"]])

# 5. Lateefah is assigned to the green team
solver.add(team[idx["Lateefah"]] == 0)

# 6. Kelly is not a facilitator
solver.add(Not(fac[idx["Kelly"]]))

# 7. Olga is a facilitator
solver.add(fac[idx["Olga"]])

# Now define the options as constraints
opt_a_constr = (team[idx["Juana"]] == 1)  # Juana is assigned to the red team
opt_b_constr = fac[idx["Lateefah"]]       # Lateefah is a facilitator
opt_c_constr = (team[idx["Olga"]] == 0)   # Olga is assigned to the green team
opt_d_constr = Not(And(fac[idx["Juana"]], fac[idx["Mei"]]))  # Juana and Mei are not both facilitators
opt_e_constr = And(Not(fac[idx["Juana"]]), Not(fac[idx["Kelly"]]))  # Neither Juana nor Kelly is a facilitator

# Evaluate each option using the exact skeleton
found_options = []
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