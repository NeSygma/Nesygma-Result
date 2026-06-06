from z3 import *

solver = Solver()

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}
N = 5

# team[i] = 0 (Green) or 1 (Red)
team = [Int(f'team_{i}') for i in range(N)]

# facilitator[i] = True if student i is a facilitator
fac = [Bool(f'fac_{i}') for i in range(N)]

# Domain constraints
for i in range(N):
    solver.add(Or(team[i] == 0, team[i] == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(N)])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
green_fac_count = Sum([If(And(team[i] == 0, fac[i]), 1, 0) for i in range(N)])
red_fac_count = Sum([If(And(team[i] == 1, fac[i]), 1, 0) for i in range(N)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Constraint 1: Juana (0) and Olga (4) on different teams
solver.add(team[0] != team[4])

# Constraint 2: Lateefah (2) on green team
solver.add(team[2] == 0)

# Constraint 3: Kelly (1) is not a facilitator
solver.add(fac[1] == False)

# Constraint 4: Olga (4) is a facilitator
solver.add(fac[4] == True)

# Given condition: Mei (3) is on green team
solver.add(team[3] == 0)

# Define answer choice constraints
# (A) Juana is assigned to the green team
opt_a = (team[0] == 0)
# (B) Kelly is assigned to the red team
opt_b = (team[1] == 1)
# (C) Olga is assigned to the green team
opt_c = (team[4] == 0)
# (D) Lateefah is a facilitator
opt_d = (fac[2] == True)
# (E) Mei is a facilitator
opt_e = (fac[3] == True)

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