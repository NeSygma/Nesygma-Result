from z3 import *

# Define students indices
J, K, L, M, O = 0, 1, 2, 3, 4
students = [J, K, L, M, O]

# Variables
team = [Int(f'team_{i}') for i in students]  # 0 = green, 1 = red
fac = [Bool(f'fac_{i}') for i in students]   # facilitator

solver = Solver()

# Team domain: each student assigned to exactly one team
for i in students:
    solver.add(Or(team[i] == 0, team[i] == 1))

# Team sizes: one team has 2, the other has 3
count_green = Sum([If(team[i] == 0, 1, 0) for i in students])
solver.add(Or(count_green == 2, count_green == 3))

# Facilitator: exactly one per team
for t in [0, 1]:
    solver.add(Sum([If(And(team[i] == t, fac[i]), 1, 0) for i in students]) == 1)

# Condition 1: Juana different team than Olga
solver.add(team[J] != team[O])

# Condition 2: Lateefah green
solver.add(team[L] == 0)

# Condition 3: Kelly not facilitator
solver.add(Not(fac[K]))

# Condition 4: Olga facilitator
solver.add(fac[O])

# Additional condition: Mei green
solver.add(team[M] == 0)

# Define options as expressions
opt_a = (team[J] == 0)   # Juana green
opt_b = (team[K] == 1)   # Kelly red
opt_c = (team[O] == 0)   # Olga green
opt_d = fac[L]           # Lateefah facilitator
opt_e = fac[M]           # Mei facilitator

# Evaluate each option for necessity: check if negation is unsatisfiable
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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