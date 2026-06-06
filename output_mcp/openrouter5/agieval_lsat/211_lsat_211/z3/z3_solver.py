from z3 import *

# Students: Juana, Kelly, Lateefah, Mei, Olga
# Teams: 0 = green, 1 = red
# Facilitator: 1 = facilitator, 0 = not facilitator

# Variables
team = {name: Int(f'team_{name}') for name in ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']}
facil = {name: Int(f'facil_{name}') for name in ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']}

solver = Solver()

# Domain constraints: team is 0 (green) or 1 (red)
for name in team:
    solver.add(Or(team[name] == 0, team[name] == 1))

# Domain constraints: facil is 0 or 1
for name in facil:
    solver.add(Or(facil[name] == 0, facil[name] == 1))

# Exactly one team has 2 members, the other has 3 members
# Count members on green team (team == 0)
green_count = Sum([If(team[name] == 0, 1, 0) for name in team])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
# Count facilitators on green team
green_facil_count = Sum([If(And(team[name] == 0, facil[name] == 1), 1, 0) for name in team])
red_facil_count = Sum([If(And(team[name] == 1, facil[name] == 1), 1, 0) for name in team])
solver.add(green_facil_count == 1)
solver.add(red_facil_count == 1)

# Condition 1: Juana is assigned to a different team than Olga
solver.add(team['Juana'] != team['Olga'])

# Condition 2: Lateefah is assigned to the green team
solver.add(team['Lateefah'] == 0)

# Condition 3: Kelly is not a facilitator
solver.add(facil['Kelly'] == 0)

# Condition 4: Olga is a facilitator
solver.add(facil['Olga'] == 1)

# Additional condition from the question: Lateefah is a facilitator
solver.add(facil['Lateefah'] == 1)

# Now evaluate each option
# Option A: Juana and Kelly are both assigned to the red team
opt_a = And(team['Juana'] == 1, team['Kelly'] == 1)

# Option B: Juana and Mei are both assigned to the red team
opt_b = And(team['Juana'] == 1, team['Mei'] == 1)

# Option C: Lateefah and Olga are both assigned to the green team
opt_c = And(team['Lateefah'] == 0, team['Olga'] == 0)

# Option D: Mei and Olga are both assigned to the green team
opt_d = And(team['Mei'] == 0, team['Olga'] == 0)

# Option E: Mei and Olga are both assigned to the red team
opt_e = And(team['Mei'] == 1, team['Olga'] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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