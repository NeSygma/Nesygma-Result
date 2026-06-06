from z3 import *

solver = Solver()

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}
N = 5

# team[i] = 0 (Green) or 1 (Red)
team = [Int(f'team_{i}') for i in range(N)]
# facilitator[i] = Bool
fac = [Bool(f'fac_{i}') for i in range(N)]

# Domain: each student on exactly one team
for i in range(N):
    solver.add(Or(team[i] == 0, team[i] == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(N)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(N)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
green_fac_count = Sum([If(And(team[i] == 0, fac[i]), 1, 0) for i in range(N)])
red_fac_count = Sum([If(And(team[i] == 1, fac[i]), 1, 0) for i in range(N)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Constraint 1: Juana (0) is on a different team than Olga (4)
solver.add(team[0] != team[4])

# Constraint 2: Lateefah (2) is on the green team
solver.add(team[2] == 0)

# Constraint 3: Kelly (1) is not a facilitator
solver.add(fac[1] == False)

# Constraint 4: Olga (4) is a facilitator
solver.add(fac[4] == True)

# Added condition: Lateefah (2) is a facilitator
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

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(N):
            t = "Green" if m[team[i]] == 0 else "Red"
            f = "Yes" if m.evaluate(fac[i], model_completion=True) else "No"
            print(f"  {names[i]}: Team={t}, Facilitator={f}")
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