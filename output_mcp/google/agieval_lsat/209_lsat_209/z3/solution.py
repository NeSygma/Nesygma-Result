from z3 import *

# Students
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']
# Teams: 0 for Green, 1 for Red
# Facilitator: Bool

solver = Solver()

# Variables
team = {s: Int(f'team_{s}') for s in students}
is_fac = {s: Bool(f'is_fac_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(team[s] >= 0, team[s] <= 1)

# Team sizes: One team has 2, one has 3
# Count members in Green (0) and Red (1)
count_g = Sum([If(team[s] == 0, 1, 0) for s in students])
count_r = Sum([If(team[s] == 1, 1, 0) for s in students])
solver.add(Or(And(count_g == 2, count_r == 3), And(count_g == 3, count_r == 2)))

# Facilitators: One per team
fac_g = Sum([If(And(team[s] == 0, is_fac[s]), 1, 0) for s in students])
fac_r = Sum([If(And(team[s] == 1, is_fac[s]), 1, 0) for s in students])
solver.add(fac_g == 1)
solver.add(fac_r == 1)

# Conditions
# 1. Juana is assigned to a different team than Olga
solver.add(team['Juana'] != team['Olga'])
# 2. Lateefah is assigned to the green team
solver.add(team['Lateefah'] == 0)
# 3. Kelly is not a facilitator
solver.add(Not(is_fac['Kelly']))
# 4. Olga is a facilitator
solver.add(is_fac['Olga'])

# Options
options = {
    "A": team['Juana'] == 1,
    "B": is_fac['Lateefah'],
    "C": team['Olga'] == 0,
    "D": Not(And(is_fac['Juana'], is_fac['Mei'])),
    "E": And(Not(is_fac['Juana']), Not(is_fac['Kelly']))
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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