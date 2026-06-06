from z3 import *

# Students: 0:Juana, 1:Kelly, 2:Lateefah, 3:Mei, 4:Olga
# Teams: 0:Green, 1:Red

solver = Solver()

team = [Int(f'team_{i}') for i in range(5)]
is_fac = [Bool(f'is_fac_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# Team sizes: one is 2, one is 3
count_g = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
count_r = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(count_g == 2, count_r == 3), And(count_g == 3, count_r == 2)))

# Facilitators: one per team
fac_g = Sum([If(And(team[i] == 0, is_fac[i]), 1, 0) for i in range(5)])
fac_r = Sum([If(And(team[i] == 1, is_fac[i]), 1, 0) for i in range(5)])
solver.add(fac_g == 1, fac_r == 1)

# Constraints
# 1. Juana is assigned to a different team than Olga is.
solver.add(team[0] != team[4])
# 2. Lateefah is assigned to the green team.
solver.add(team[2] == 0)
# 3. Kelly is not a facilitator.
solver.add(is_fac[1] == False)
# 4. Olga is a facilitator.
solver.add(is_fac[4] == True)

# Options
# (A) Lateefah is a facilitator, and she is assigned to the same team as Kelly is.
opt_a = And(is_fac[2] == True, team[2] == team[1])
# (B) Mei is a facilitator, and she is assigned to the same team as Kelly is.
opt_b = And(is_fac[3] == True, team[3] == team[1])
# (C) Olga is a facilitator, and she is assigned to the same team as Mei is.
opt_c = And(is_fac[4] == True, team[4] == team[3])
# (D) Lateefah is a facilitator, and she is assigned to a different team than Juana is.
opt_d = And(is_fac[2] == True, team[2] != team[0])
# (E) Mei is a facilitator, and she is assigned to a different team than Olga is.
opt_e = And(is_fac[3] == True, team[3] != team[4])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # This option is possible, so it's not the one that "must be false"
        pass
    else:
        # This option is impossible, so it "must be false"
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