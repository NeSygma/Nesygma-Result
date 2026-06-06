from z3 import *

solver = Solver()

# Students
students = ['juana', 'kelly', 'lateefah', 'mei', 'olga']

# Boolean variables: team_green[s] = True means student s is on green team, False = red team
team_green = {s: Bool(f'team_green_{s}') for s in students}

# Boolean variables: is_facilitator[s] = True means student s is a facilitator
is_facilitator = {s: Bool(f'is_facilitator_{s}') for s in students}

# Constraint 4: Lateefah is assigned to green team
solver.add(team_green['lateefah'] == True)

# Constraint 1: Juana and Olga on different teams
solver.add(team_green['juana'] != team_green['olga'])

# Constraint 5: Kelly is not a facilitator
solver.add(is_facilitator['kelly'] == False)

# Constraint 6: Olga is a facilitator
solver.add(is_facilitator['olga'] == True)

# Conditional: Lateefah is a facilitator (given condition)
solver.add(is_facilitator['lateefah'] == True)

# Team sizes: one team has 2, the other has 3
# Number on green team is either 2 or 3
green_count = Sum([If(team_green[s], 1, 0) for s in students])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
# Green team facilitators
green_fac_count = Sum([If(And(team_green[s], is_facilitator[s]), 1, 0) for s in students])
solver.add(green_fac_count == 1)

# Red team facilitators
red_fac_count = Sum([If(And(Not(team_green[s]), is_facilitator[s]), 1, 0) for s in students])
solver.add(red_fac_count == 1)

# Now evaluate each option
options = {
    "A": And(team_green['juana'] == False, team_green['kelly'] == False),
    "B": And(team_green['juana'] == False, team_green['mei'] == False),
    "C": And(team_green['lateefah'] == True, team_green['olga'] == True),
    "D": And(team_green['mei'] == True, team_green['olga'] == True),
    "E": And(team_green['mei'] == False, team_green['olga'] == False)
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
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