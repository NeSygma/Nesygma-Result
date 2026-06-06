from z3 import *

# Employees
employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']
# Map names to indices 0-5
R, S, T, V, X, Y = Ints('R S T V X Y')
all_vars = [R, S, T, V, X, Y]

solver = Solver()

# Each employee assigned a unique space 1-6
for var in all_vars:
    solver.add(var >= 1, var <= 6)
solver.add(Distinct(all_vars))

# Rules
solver.add(Y > T)
solver.add(X > S)
solver.add(R > Y)
solver.add(Or(R == 1, R == 2, R == 3, R == 4))

# Condition: Y > S
solver.add(Y > S)

# Options
options = [
    ("A", T == 1),
    ("B", Y == 2),
    ("C", R == 3),
    ("D", S == 3),
    ("E", V == 4)
]

found_options = []
for letter, constr in options:
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