from z3 import *

solver = Solver()

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}

# team[i] = 0 (green) or 1 (red)
team = [Int(f'team_{i}') for i in range(5)]
# facilitator[i] = True/False
facil = [Bool(f'facil_{i}') for i in range(5)]

# Domain: each student on exactly one team
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3),
              And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
green_facil_count = Sum([If(And(team[i] == 0, facil[i]), 1, 0) for i in range(5)])
red_facil_count = Sum([If(And(team[i] == 1, facil[i]), 1, 0) for i in range(5)])
solver.add(green_facil_count == 1)
solver.add(red_facil_count == 1)

# Constraint 1: Juana different team than Olga
solver.add(team[0] != team[4])

# Constraint 2: Lateefah on green team
solver.add(team[2] == 0)

# Constraint 3: Kelly is not a facilitator
solver.add(facil[1] == False)

# Constraint 4: Olga is a facilitator
solver.add(facil[4] == True)

# Define answer choice constraints
# (A) Lateefah is a facilitator, and she is on the same team as Kelly
opt_a = And(facil[2] == True, team[2] == team[1])

# (B) Mei is a facilitator, and she is on the same team as Kelly
opt_b = And(facil[3] == True, team[3] == team[1])

# (C) Olga is a facilitator, and she is on the same team as Mei
opt_c = And(facil[4] == True, team[4] == team[3])

# (D) Lateefah is a facilitator, and she is on a different team than Juana
opt_d = And(facil[2] == True, team[2] != team[0])

# (E) Mei is a facilitator, and she is on a different team than Olga
opt_e = And(facil[3] == True, team[3] != team[4])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# The question asks "which must be false" — so we find options that are UNSAT
must_be_false = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        must_be_false.append(letter)
        print(f"Option {letter}: UNSAT (must be false)")
    elif result == sat:
        print(f"Option {letter}: SAT (can be true)")
        m = solver.model()
        for i in range(5):
            t = "Green" if m[team[i]] == 0 else "Red"
            f = "Yes" if m.evaluate(facil[i]) else "No"
            print(f"  {names[i]}: team={t}, facilitator={f}")
    else:
        print(f"Option {letter}: UNKNOWN")
    solver.pop()

print()
if len(must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false[0]}")
elif len(must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-false options found {must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-false options found")