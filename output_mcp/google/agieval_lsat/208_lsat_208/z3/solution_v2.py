from z3 import *

# Define variables
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']
team = {s: Int(f'team_{s}') for s in students} # 0: Green, 1: Red
is_fac = {s: Bool(f'fac_{s}') for s in students}

solver = Solver()

# Constraints
for s in students:
    solver.add(team[s] >= 0, team[s] <= 1)

# 1. Juana different team than Olga
solver.add(team['Juana'] != team['Olga'])

# 2. Lateefah on Green
solver.add(team['Lateefah'] == 0)

# 3. Kelly not a facilitator
solver.add(Not(is_fac['Kelly']))

# 4. Olga is a facilitator
solver.add(is_fac['Olga'])

# Team sizes: one 2, one 3
green_count = Sum([If(team[s] == 0, 1, 0) for s in students])
red_count = Sum([If(team[s] == 1, 1, 0) for s in students])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# One facilitator per team
green_facs = Sum([If(And(team[s] == 0, is_fac[s]), 1, 0) for s in students])
red_facs = Sum([If(And(team[s] == 1, is_fac[s]), 1, 0) for s in students])
solver.add(green_facs == 1)
solver.add(red_facs == 1)

# Check options
options = {
    "A": And(team['Juana']==0, team['Lateefah']==0, team['Olga']==0, team['Kelly']==1, team['Mei']==1,
             Not(is_fac['Juana']), Not(is_fac['Lateefah']), is_fac['Olga'], Not(is_fac['Kelly']), is_fac['Mei']),
    "B": And(team['Kelly']==0, team['Lateefah']==0, team['Olga']==0, team['Juana']==1, team['Mei']==1,
             Not(is_fac['Kelly']), is_fac['Lateefah'], Not(is_fac['Olga']), Not(is_fac['Juana']), is_fac['Mei']),
    "C": And(team['Kelly']==0, team['Lateefah']==0, team['Olga']==0, team['Juana']==1, team['Mei']==1,
             Not(is_fac['Kelly']), Not(is_fac['Lateefah']), is_fac['Olga'], is_fac['Juana'], Not(is_fac['Mei'])),
    "D": And(team['Kelly']==0, team['Mei']==0, team['Olga']==0, team['Juana']==1, team['Lateefah']==1,
             Not(is_fac['Kelly']), Not(is_fac['Mei']), is_fac['Olga'], is_fac['Juana'], Not(is_fac['Lateefah'])),
    "E": And(team['Lateefah']==0, team['Olga']==0, team['Juana']==1, team['Kelly']==1, team['Mei']==1,
             Not(is_fac['Lateefah']), is_fac['Olga'], Not(is_fac['Juana']), is_fac['Kelly'], Not(is_fac['Mei']))
}

for label, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        print(f"Option {label} is valid.")
    else:
        print(f"Option {label} is invalid.")
    solver.pop()