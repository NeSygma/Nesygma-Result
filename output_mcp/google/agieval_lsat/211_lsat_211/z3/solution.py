from z3 import *

# Students
students = ['J', 'K', 'L', 'M', 'O']
# Teams: 0 = Green, 1 = Red
# Facilitator: True/False

solver = Solver()

# Variables
team = {s: Int(f'team_{s}') for s in students}
is_facilitator = {s: Bool(f'is_facilitator_{s}') for s in students}

# Domains
for s in students:
    solver.add(team[s] >= 0, team[s] <= 1)

# Constraints
# 1. Juana is assigned to a different team than Olga is.
solver.add(team['J'] != team['O'])

# 2. Lateefah is assigned to the green team.
solver.add(team['L'] == 0)

# 3. Kelly is not a facilitator.
solver.add(is_facilitator['K'] == False)

# 4. Olga is a facilitator.
solver.add(is_facilitator['O'] == True)

# 5. If Lateefah is a facilitator (Given in the question)
solver.add(is_facilitator['L'] == True)

# 6. One team will have two members, and the other will have three members.
green_count = Sum([If(team[s] == 0, 1, 0) for s in students])
red_count = Sum([If(team[s] == 1, 1, 0) for s in students])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# 7. One member of each team will be designated as facilitator.
# Green team facilitator
solver.add(Sum([If(And(team[s] == 0, is_facilitator[s]), 1, 0) for s in students]) == 1)
# Red team facilitator
solver.add(Sum([If(And(team[s] == 1, is_facilitator[s]), 1, 0) for s in students]) == 1)

# Options
options = {
    "A": And(team['J'] == 1, team['K'] == 1),
    "B": And(team['J'] == 1, team['M'] == 1),
    "C": And(team['L'] == 0, team['O'] == 0),
    "D": And(team['M'] == 0, team['O'] == 0),
    "E": And(team['M'] == 1, team['O'] == 1)
}

found_options = []
for letter, constr in options.items():
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