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
    solver.add(Implies(fac[i], Or(team[i] == 0, team[i] == 1)))  # redundant but explicit

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
fac_green = Sum([If(And(fac[i], team[i] == 0), 1, 0) for i in range(5)])
fac_red = Sum([If(And(fac[i], team[i] == 1), 1, 0) for i in range(5)])
solver.add(fac_green == 1)
solver.add(fac_red == 1)

# Juana is on a different team than Olga
solver.add(team[0] != team[4])

# Lateefah is on the green team
solver.add(team[2] == 0)

# Kelly is not a facilitator
solver.add(fac[1] == False)

# Olga is a facilitator
solver.add(fac[4] == True)

# Define option constraints
# (A) Lateefah is a facilitator, and she is on the same team as Kelly
opt_a = And(fac[2] == True, team[2] == team[1])

# (B) Mei is a facilitator, and she is on the same team as Kelly
opt_b = And(fac[3] == True, team[3] == team[1])

# (C) Olga is a facilitator, and she is on the same team as Mei
opt_c = And(fac[4] == True, team[4] == team[3])

# (D) Lateefah is a facilitator, and she is on a different team than Juana
opt_d = And(fac[2] == True, team[2] != team[0])

# (E) Mei is a facilitator, and she is on a different team than Olga
opt_e = And(fac[3] == True, team[3] != team[4])

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