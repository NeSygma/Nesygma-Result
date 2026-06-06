from z3 import *

solver = Solver()

# Students: Juana(0), Kelly(1), Lateefah(2), Mei(3), Olga(4)
names = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
J, K, L, M, O = 0, 1, 2, 3, 4

# team[i] = 0 (Green) or 1 (Red)
team = [Int(f'team_{names[i]}') for i in range(5)]
# facilitator[i] = Bool
fac = [Bool(f'fac_{names[i]}') for i in range(5)]

# Domain: each student on exactly one team
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# Constraint 1: Juana different team than Olga
solver.add(team[J] != team[O])

# Constraint 2: Lateefah on green team
solver.add(team[L] == 0)

# Constraint 3: Kelly is not a facilitator
solver.add(Not(fac[K]))

# Constraint 4: Olga is a facilitator
solver.add(fac[O])

# Team sizes: one team has 2, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3),
              And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
green_fac_count = Sum([If(And(team[i] == 0, fac[i]), 1, 0) for i in range(5)])
red_fac_count = Sum([If(And(team[i] == 1, fac[i]), 1, 0) for i in range(5)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Define answer choice constraints
# (A) Lateefah is a facilitator, and she is on the same team as Kelly
opt_a = And(fac[L], team[L] == team[K])

# (B) Mei is a facilitator, and she is on the same team as Kelly
opt_b = And(fac[M], team[M] == team[K])

# (C) Olga is a facilitator, and she is on the same team as Mei
opt_c = And(fac[O], team[O] == team[M])

# (D) Lateefah is a facilitator, and she is on a different team than Juana
opt_d = And(fac[L], team[L] != team[J])

# (E) Mei is a facilitator, and she is on a different team than Olga
opt_e = And(fac[M], team[M] != team[O])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# "Must be false" = the option is UNSATISFIABLE given the base constraints
# Find which options are impossible
impossible_options = []
possible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    else:
        possible_options.append(letter)
    solver.pop()

print(f"Possible (can be true): {possible_options}")
print(f"Impossible (must be false): {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")