from z3 import *

# Students
students = ['J', 'K', 'L', 'M', 'O']
# Teams: 0 = Green, 1 = Red
team = {s: Int(f'team_{s}') for s in students}
# Facilitator: True/False
is_fac = {s: Bool(f'is_fac_{s}') for s in students}

solver = Solver()

# Domain constraints
for s in students:
    solver.add(team[s] >= 0, team[s] <= 1)

# Team sizes: one team has 2, one has 3
count_G = Sum([If(team[s] == 0, 1, 0) for s in students])
count_R = Sum([If(team[s] == 1, 1, 0) for s in students])
solver.add(Or(And(count_G == 2, count_R == 3), And(count_G == 3, count_R == 2)))

# Facilitators: one per team
fac_G = Sum([If(And(team[s] == 0, is_fac[s]), 1, 0) for s in students])
fac_R = Sum([If(And(team[s] == 1, is_fac[s]), 1, 0) for s in students])
solver.add(fac_G == 1, fac_R == 1)

# Constraints
solver.add(team['J'] != team['O'])
solver.add(team['L'] == 0)
solver.add(is_fac['K'] == False)
solver.add(is_fac['O'] == True)

# Condition: Mei is assigned to the green team
solver.add(team['M'] == 0)

# Options
options = {
    "A": team['J'] == 0,
    "B": team['K'] == 1,
    "C": team['O'] == 0,
    "D": is_fac['L'] == True,
    "E": is_fac['M'] == True
}

# Check which option must be true
# An option must be true if Not(option) is unsatisfiable
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