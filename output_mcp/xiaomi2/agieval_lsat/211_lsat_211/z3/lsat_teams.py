from z3 import *

solver = Solver()

# Students: Juana(0), Kelly(1), Lateefah(2), Mei(3), Olga(4)
names = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
N = 5

# team[i] = 0 (green) or 1 (red)
team = [Int(f'team_{names[i]}') for i in range(N)]
# facilitator[i] = Bool
facil = [Bool(f'facil_{names[i]}') for i in range(N)]

# Domain: each student on exactly one team
for i in range(N):
    solver.add(Or(team[i] == 0, team[i] == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(N)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(N)])
solver.add(Or(And(green_count == 2, red_count == 3),
              And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
# Green team facilitator count == 1
solver.add(Sum([If(And(team[i] == 0, facil[i]), 1, 0) for i in range(N)]) == 1)
# Red team facilitator count == 1
solver.add(Sum([If(And(team[i] == 1, facil[i]), 1, 0) for i in range(N)]) == 1)

# Constraint 1: Juana different team than Olga
solver.add(team[0] != team[4])

# Constraint 2: Lateefah on green team
solver.add(team[2] == 0)

# Constraint 3: Kelly is not a facilitator
solver.add(Not(facil[1]))

# Constraint 4: Olga is a facilitator
solver.add(facil[4] == True)

# Additional condition: Lateefah is a facilitator
solver.add(facil[2] == True)

# Define answer choice constraints
# (A) Juana and Kelly are both on red team
opt_a = And(team[0] == 1, team[1] == 1)
# (B) Juana and Mei are both on red team
opt_b = And(team[0] == 1, team[3] == 1)
# (C) Lateefah and Olga are both on green team
opt_c = And(team[2] == 0, team[4] == 0)
# (D) Mei and Olga are both on green team
opt_d = And(team[3] == 0, team[4] == 0)
# (E) Mei and Olga are both on red team
opt_e = And(team[3] == 1, team[4] == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT:")
        for i in range(N):
            t = "Green" if m.evaluate(team[i]) == 0 else "Red"
            f = "Yes" if m.evaluate(facil[i]) else "No"
            print(f"  {names[i]}: team={t}, facilitator={f}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")