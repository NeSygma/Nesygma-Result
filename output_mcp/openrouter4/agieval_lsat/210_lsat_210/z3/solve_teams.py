from z3 import *

solver = Solver()

students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']

# Team: 1 = green, 0 = red
team = {s: Int(f'team_{s}') for s in students}
facilitator = {s: Bool(f'facilitator_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(Or(team[s] == 0, team[s] == 1))

# Condition 1: Juana and Olga different teams
solver.add(team['Juana'] != team['Olga'])

# Condition 2: Lateefah is on the green team
solver.add(team['Lateefah'] == 1)

# Condition 3: Kelly is not a facilitator
solver.add(facilitator['Kelly'] == False)

# Condition 4: Olga is a facilitator
solver.add(facilitator['Olga'] == True)

# Team sizes: one team has 2 members, the other has 3
green_count = Sum([team[s] for s in students])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
for t in [0, 1]:
    solver.add(Sum([If(And(team[s] == t, facilitator[s]), 1, 0) for s in students]) == 1)

# Now evaluate each option
options = [
    ("A", And(facilitator['Lateefah'] == True, team['Lateefah'] == team['Kelly'])),
    ("B", And(facilitator['Mei'] == True, team['Mei'] == team['Kelly'])),
    ("C", And(facilitator['Olga'] == True, team['Olga'] == team['Mei'])),
    ("D", And(facilitator['Lateefah'] == True, team['Lateefah'] != team['Juana'])),
    ("E", And(facilitator['Mei'] == True, team['Mei'] != team['Olga']))
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    # print(f"Option {letter}: {result}")
    if result == sat:
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