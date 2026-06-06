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

# Find which options are satisfiable and which are not
unsat_options = []
sat_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        sat_options.append(letter)
    else:
        unsat_options.append(letter)
    solver.pop()

# The question asks "which one must be false?" i.e., which one is unsatisfiable
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) == 0:
    print("STATUS: unsat")
    print("Refine: No options are false (all are possible)")
else:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found false {unsat_options}")