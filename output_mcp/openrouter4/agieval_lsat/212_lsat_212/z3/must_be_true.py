from z3 import *

# Students
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
idx = {name: i for i, name in enumerate(students)}

# Bool variables: True = green team, False = red team
team = [Bool(f"team_{name}") for name in students]
# Bool variables: True = facilitator
facilitator = [Bool(f"facilitator_{name}") for name in students]

solver = Solver()

# 1. Juana and Olga on different teams
solver.add(team[idx["Juana"]] != team[idx["Olga"]])

# 2. Lateefah on green team
solver.add(team[idx["Lateefah"]] == True)

# 3. Kelly is not a facilitator
solver.add(facilitator[idx["Kelly"]] == False)

# 4. Olga is a facilitator
solver.add(facilitator[idx["Olga"]] == True)

# 5. Exactly one facilitator per team
for target_team in [True, False]:
    count = Sum([If(And(team[i] == target_team, facilitator[i] == True), 1, 0) for i in range(5)])
    solver.add(count == 1)

# 6. Team sizes: one team has 2 members, the other has 3
green_count = Sum([If(team[i] == True, 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))

# 7. Additional condition: Mei is on green team
solver.add(team[idx["Mei"]] == True)

# --- Check each option: must be true if its negation is unsat ---
options = {
    "A": team[idx["Juana"]] == True,
    "B": team[idx["Kelly"]] == False,   # Kelly on red team
    "C": team[idx["Olga"]] == True,
    "D": facilitator[idx["Lateefah"]] == True,
    "E": facilitator[idx["Mei"]] == True,
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))  # Can the option be false?
    if solver.check() == unsat:  # If it cannot be false, it must be true
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