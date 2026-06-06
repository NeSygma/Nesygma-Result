from z3 import *

solver = Solver()

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}

# team[i] = 0 (green) or 1 (red)
team = [Int(f'team_{i}') for i in range(5)]
# facilitator[i] = True if student i is facilitator
fac = [Bool(f'fac_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
green_fac = Sum([If(And(team[i] == 0, fac[i]), 1, 0) for i in range(5)])
red_fac = Sum([If(And(team[i] == 1, fac[i]), 1, 0) for i in range(5)])
solver.add(green_fac == 1)
solver.add(red_fac == 1)

# Condition 1: Juana is on a different team than Olga
solver.add(team[0] != team[4])

# Condition 2: Lateefah is on the green team
solver.add(team[2] == 0)

# Condition 3: Kelly is not a facilitator
solver.add(fac[1] == False)

# Condition 4: Olga is a facilitator
solver.add(fac[4] == True)

# Additional premise: Lateefah is a facilitator
solver.add(fac[2] == True)

# Define option constraints
# (A) Juana and Kelly are both assigned to the red team
opt_a = And(team[0] == 1, team[1] == 1)

# (B) Juana and Mei are both assigned to the red team
opt_b = And(team[0] == 1, team[3] == 1)

# (C) Lateefah and Olga are both assigned to the green team
opt_c = And(team[2] == 0, team[4] == 0)

# (D) Mei and Olga are both assigned to the green team
opt_d = And(team[3] == 0, team[4] == 0)

# (E) Mei and Olga are both assigned to the red team
opt_e = And(team[3] == 1, team[4] == 1)

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