from z3 import *

solver = Solver()

# Define the students
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']

# Define team assignment variables: 0 = green, 1 = red
team = {s: Int(f'team_{s}') for s in students}

# Define facilitator variables: 1 = facilitator, 0 = not
fac = {s: Int(f'fac_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(Or(team[s] == 0, team[s] == 1))
    solver.add(Or(fac[s] == 0, fac[s] == 1))

# Exactly one team has 2 members, the other has 3
green_count = Sum([If(team[s] == 0, 1, 0) for s in students])
red_count = Sum([If(team[s] == 1, 1, 0) for s in students])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
green_fac = Sum([If(And(team[s] == 0, fac[s] == 1), 1, 0) for s in students])
red_fac = Sum([If(And(team[s] == 1, fac[s] == 1), 1, 0) for s in students])
solver.add(green_fac == 1)
solver.add(red_fac == 1)

# Base constraints from problem
# Juana is assigned to a different team than Olga
solver.add(team['Juana'] != team['Olga'])

# Lateefah is assigned to the green team
solver.add(team['Lateefah'] == 0)

# Kelly is not a facilitator
solver.add(fac['Kelly'] == 0)

# Olga is a facilitator
solver.add(fac['Olga'] == 1)

# Define each option as a constraint
# Option A: green team: Juana, Lateefah, Olga (facilitator); red team: Kelly, Mei (facilitator)
opt_a_constr = And(
    team['Juana'] == 0,
    team['Lateefah'] == 0,
    team['Olga'] == 0,
    team['Kelly'] == 1,
    team['Mei'] == 1,
    fac['Olga'] == 1,
    fac['Mei'] == 1,
    fac['Juana'] == 0,
    fac['Lateefah'] == 0,
    fac['Kelly'] == 0
)

# Option B: green team: Kelly, Lateefah (facilitator), Olga; red team: Juana, Mei (facilitator)
opt_b_constr = And(
    team['Kelly'] == 0,
    team['Lateefah'] == 0,
    team['Olga'] == 0,
    team['Juana'] == 1,
    team['Mei'] == 1,
    fac['Lateefah'] == 1,
    fac['Mei'] == 1,
    fac['Kelly'] == 0,
    fac['Olga'] == 0,
    fac['Juana'] == 0
)

# Option C: green team: Kelly, Lateefah, Olga (facilitator); red team: Juana (facilitator), Mei
opt_c_constr = And(
    team['Kelly'] == 0,
    team['Lateefah'] == 0,
    team['Olga'] == 0,
    team['Juana'] == 1,
    team['Mei'] == 1,
    fac['Olga'] == 1,
    fac['Juana'] == 1,
    fac['Kelly'] == 0,
    fac['Lateefah'] == 0,
    fac['Mei'] == 0
)

# Option D: green team: Kelly, Mei, Olga (facilitator); red team: Juana (facilitator), Lateefah
opt_d_constr = And(
    team['Kelly'] == 0,
    team['Mei'] == 0,
    team['Olga'] == 0,
    team['Juana'] == 1,
    team['Lateefah'] == 1,
    fac['Olga'] == 1,
    fac['Juana'] == 1,
    fac['Kelly'] == 0,
    fac['Mei'] == 0,
    fac['Lateefah'] == 0
)

# Option E: green team: Lateefah, Olga (facilitator); red team: Juana, Kelly (facilitator), Mei
opt_e_constr = And(
    team['Lateefah'] == 0,
    team['Olga'] == 0,
    team['Juana'] == 1,
    team['Kelly'] == 1,
    team['Mei'] == 1,
    fac['Olga'] == 1,
    fac['Kelly'] == 1,
    fac['Lateefah'] == 0,
    fac['Juana'] == 0,
    fac['Mei'] == 0
)

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