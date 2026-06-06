from z3 import *

# Students
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']
# Team assignment: Bool is_green (True=green, False=red)
is_green = {s: Bool(f'{s}_green') for s in students}
# Facilitator status: Bool is_fac (True=facilitator)
is_fac = {s: Bool(f'{s}_fac') for s in students}

solver = Solver()

# Base constraints
# Exactly one facilitator per team
# Count members per team
green_members = Sum([If(is_green[s], 1, 0) for s in students])
red_members = Sum([If(Not(is_green[s]), 1, 0) for s in students])
# One team has 2 members, other 3
solver.add(Or(And(green_members == 2, red_members == 3),
           And(green_members == 3, red_members == 2)))
# Exactly one facilitator on each team
solver.add(Sum([If(And(is_green[s], is_fac[s]), 1, 0) for s in students]) == 1)
solver.add(Sum([If(And(Not(is_green[s]), is_fac[s]), 1, 0) for s in students]) == 1)
# Juana different team than Olga
solver.add(is_green['Juana'] != is_green['Olga'])
# Lateefah green
solver.add(is_green['Lateefah'] == True)
# Kelly not facilitator
solver.add(is_fac['Kelly'] == False)
# Olga is a facilitator
solver.add(is_fac['Olga'] == True)
# Mei green (condition of the question)
solver.add(is_green['Mei'] == True)

# Option constraints
opt_A = is_green['Juana'] == True   # Juana green
opt_B = is_green['Kelly'] == False  # Kelly red
opt_C = is_green['Olga'] == True    # Olga green
opt_D = is_fac['Lateefah'] == True  # Lateefah facilitator
opt_E = is_fac['Mei'] == True       # Mei facilitator

options = [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]

# Determine which option is forced by checking negation unsat
forced = []
for letter, opt in options:
    solver.push()
    solver.add(Not(opt))
    res = solver.check()
    if res == unsat:
        forced.append(letter)
    solver.pop()

if len(forced) == 1:
    print("STATUS: proved")
    print(f"answer:{forced[0]}")
else:
    print("STATUS: unknown")
    print(f"Forced candidates: {forced}")